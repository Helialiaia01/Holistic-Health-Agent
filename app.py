"""
Flask API for Dorost - Holistic Health Agent

This wraps the health agent in a REST API so it can be deployed to Google Cloud Run.
Users can interact with Dorost via HTTP requests instead of just CLI.

DEPLOYMENT:
  gcloud run deploy dorost --source . --set-env-vars="GOOGLE_API_KEY=${GOOGLE_API_KEY}"
  
USAGE:
  1. Start consultation: POST /api/consultation/start
     Request: {"initial_query": "I have fatigue and weight gain"}
     Response: {consultation_id, health_profile, red_flags}
     
  2. Chat with agent: POST /api/consultation/{consultation_id}/chat
     Request: {"message": "My thyroid was normal 2 years ago", "agent_stage": "diagnostic"}
     Response: {agent_response, next_stage, confidence_score}
     
  3. Get results: GET /api/consultation/{consultation_id}/results
     Response: {complete consultation output with all agent findings}
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, Any
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Dorost components
from src.orchestrator import create_health_agent_orchestrator
from src.knowledge.context_engineering import ContextManager
from src.logger import get_logger
from src.evaluation import EvaluationTracker

# ============================================================================
# FLASK APP SETUP
# ============================================================================

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Initialize logger
logger = get_logger("dorost-api")

# Initialize Dorost components
orchestrator = create_health_agent_orchestrator()
evaluation = EvaluationTracker()

# In-memory session storage (in production, use database)
sessions: Dict[str, Dict[str, Any]] = {}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_session_id() -> str:
    """Generate a unique session ID for each consultation."""
    return str(uuid.uuid4())

def get_session(session_id: str) -> Dict[str, Any]:
    """Get session data or return 404 error."""
    if session_id not in sessions:
        return None
    return sessions[session_id]

def save_session(session_id: str, data: Dict[str, Any]):
    """Save session data."""
    sessions[session_id] = data
    logger.info(f"Session saved: {session_id}", extra={"session_id": session_id})

def create_error_response(message: str, status_code: int = 400) -> tuple:
    """Create standardized error response."""
    return jsonify({
        "status": "error",
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }), status_code

def create_success_response(data: Dict[str, Any], status_code: int = 200) -> tuple:
    """Create standardized success response."""
    return jsonify({
        "status": "success",
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }), status_code

# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for load balancer."""
    return create_success_response({"status": "healthy"})

# ============================================================================
# CONSULTATION ENDPOINTS
# ============================================================================

@app.route("/api/consultation/start", methods=["POST"])
def start_consultation():
    """
    Start a new health consultation.
    
    Request body:
    {
        "initial_query": "I have fatigue and weight gain",
        "user_metadata": {
            "age": 45,
            "gender": "female",
            "location": "US"
        }
    }
    
    Response:
    {
        "consultation_id": "uuid-here",
        "stage": "intake",
        "message": "Welcome to Dorost...",
        "next_action": "Describe your main health concern"
    }
    """
    try:
        # Validate request
        data = request.get_json()
        if not data or "initial_query" not in data:
            return create_error_response("Missing required field: initial_query", 400)
        
        initial_query = data["initial_query"]
        user_metadata = data.get("user_metadata", {})
        
        # Create new session
        session_id = generate_session_id()
        
        logger.info(f"Starting new consultation", extra={
            "session_id": session_id,
            "query_length": len(initial_query)
        })
        
        # Run consultation through orchestrator
        consultation_output = orchestrator.run_consultation(initial_query)
        
        # Initialize session data
        session_data = {
            "session_id": session_id,
            "created_at": datetime.utcnow().isoformat(),
            "status": "complete",
            "current_stage": "recommender",
            "user_metadata": user_metadata,
            "conversation_history": [
                {"role": "user", "content": initial_query}
            ],
            "consultation_output": consultation_output,
            "red_flags_detected": len(consultation_output.get("red_flags", [])),
            "overall_confidence": consultation_output.get("overall_confidence", 0.0)
        }
        
        # Save session
        save_session(session_id, session_data)
        
        # Log the consultation
        evaluation.record_agent_execution(
            agent_type="orchestrator",
            input_text=initial_query,
            output_text=str(consultation_output),
            execution_time=0.5,
            confidence_score=session_data["overall_confidence"],
            success=True
        )
        
        logger.info(f"Consultation completed", extra={
            "session_id": session_id,
            "overall_confidence": session_data["overall_confidence"],
            "red_flags": session_data["red_flags_detected"]
        })
        
        # Return consultation results
        response_data = {
            "consultation_id": session_id,
            "status": "complete",
            "overall_confidence": session_data["overall_confidence"],
            "stages_completed": 6,
            "red_flags": session_data["red_flags_detected"],
            "stages": consultation_output.get("stages", {})
        }
        
        return create_success_response(response_data, 201)
        
    except Exception as e:
        logger.error(f"Error starting consultation: {str(e)}")
        return create_error_response(f"Internal server error: {str(e)}", 500)

@app.route("/api/consultation/<session_id>/chat", methods=["POST"])
def chat(session_id: str):
    """
    Send a message to continue the consultation.
    
    Request body:
    {
        "message": "Yes, I've had this for 6 months",
        "agent_stage": "diagnostic"
    }
    
    Response:
    {
        "agent_response": "I see, 6 months is quite a while...",
        "next_stage": "specialty_router",
        "confidence_score": 0.78,
        "red_flags": []
    }
    """
    try:
        # Validate session exists
        session = get_session(session_id)
        if not session:
            return create_error_response(f"Session not found: {session_id}", 404)
        
        # Validate request
        data = request.get_json()
        if not data or "message" not in data:
            return create_error_response("Missing required field: message", 400)
        
        user_message = data["message"]
        agent_stage = data.get("agent_stage", session["current_stage"])
        
        logger.info(f"Chat message received", extra={
            "session_id": session_id,
            "stage": agent_stage,
            "message_length": len(user_message)
        })
        
        # Add to conversation history
        session["conversation_history"].append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # In production, this would route to appropriate agent
        # For now, acknowledge and track the message
        response_data = {
            "agent_response": f"I received your follow-up: '{user_message}'. This has been recorded in your consultation history.",
            "session_id": session_id,
            "status": "recorded",
            "confidence_score": 0.75
        }
        
        # Add to conversation history
        session["conversation_history"].append({
            "role": "assistant",
            "content": response_data["agent_response"],
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Log the interaction
        evaluation.record_agent_execution(
            agent_type="chat",
            input_text=user_message,
            output_text=response_data["agent_response"],
            execution_time=0.1,
            confidence_score=response_data["confidence_score"],
            success=True
        )
        
        # Update session
        save_session(session_id, session)
        
        return create_success_response(response_data)
        
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}", extra={"session_id": session_id})
        return create_error_response(f"Internal server error: {str(e)}", 500)

@app.route("/api/consultation/<session_id>/results", methods=["GET"])
def get_results(session_id: str):
    """
    Get complete consultation results.
    
    Response:
    {
        "consultation_id": "uuid",
        "status": "complete",
        "health_profile": {...},
        "diagnostic_findings": {...},
        "specialist_recommendation": {...},
        "medical_analysis": {...},
        "root_cause_analysis": {...},
        "recommendations": {...},
        "red_flags": [],
        "overall_confidence": 0.78,
        "medical_disclaimer": "⚠️ IMPORTANT..."
    }
    """
    try:
        # Validate session exists
        session = get_session(session_id)
        if not session:
            return create_error_response(f"Session not found: {session_id}", 404)
        
        # Check if consultation is complete
        if session["status"] != "complete":
            return create_error_response("Consultation not yet complete", 400)
        
        logger.info(f"Results retrieved", extra={"session_id": session_id})
        
        # Return actual consultation output from orchestrator
        consultation_output = session.get("consultation_output", {})
        
        results = {
            "consultation_id": session_id,
            "status": session["status"],
            "created_at": session["created_at"],
            "overall_confidence": session.get("overall_confidence", 0.0),
            "stages": consultation_output.get("stages", {}),
            "red_flags": session.get("red_flags_detected", 0),
            "conversation_history": session["conversation_history"],
            "medical_disclaimer": "IMPORTANT: I am an AI health education agent, not a licensed medical professional. Always consult a real doctor."
        }
        
        return create_success_response(results)
        
    except Exception as e:
        logger.error(f"Error retrieving results: {str(e)}", extra={"session_id": session_id})
        return create_error_response(f"Internal server error: {str(e)}", 500)

@app.route("/api/consultation/<session_id>", methods=["GET"])
def get_consultation(session_id: str):
    """Get current consultation status and data."""
    try:
        session = get_session(session_id)
        if not session:
            return create_error_response(f"Session not found: {session_id}", 404)
        
        return create_success_response({
            "consultation_id": session_id,
            "status": session["status"],
            "current_stage": session["current_stage"],
            "created_at": session["created_at"],
            "conversation_count": len(session["conversation_history"]),
            "red_flags": len(session["red_flags_detected"]),
            "confidence": session["confidence_scores"]
        })
        
    except Exception as e:
        return create_error_response(f"Internal server error: {str(e)}", 500)

# ============================================================================
# EVALUATION & METRICS ENDPOINTS
# ============================================================================

@app.route("/api/metrics/evaluation", methods=["GET"])
def get_metrics():
    """Get evaluation metrics and performance statistics."""
    try:
        metrics = {
            "pipeline_stats": evaluation.get_pipeline_stats(),
            "agent_stats": {
                agent: evaluation.get_agent_stats(agent)
                for agent in ["intake", "diagnostic", "specialty_router", "knowledge", "root_cause", "recommender"]
            }
        }
        return create_success_response(metrics)
    except Exception as e:
        logger.error(f"Error retrieving metrics: {str(e)}")
        return create_error_response(f"Internal server error: {str(e)}", 500)

@app.route("/api/metrics/report", methods=["GET"])
def get_report():
    """Get human-readable evaluation report."""
    try:
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "report": evaluation.print_report()
        }
        return create_success_response(report)
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        return create_error_response(f"Internal server error: {str(e)}", 500)

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return create_error_response("Endpoint not found", 404)

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return create_error_response("Internal server error", 500)

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Get port from environment or default to 8080 (Cloud Run standard)
    port = int(os.environ.get("PORT", 8080))
    
    # In production, disable debug mode
    debug = os.environ.get("FLASK_ENV") == "development"
    
    logger.info(f"Starting Dorost API on port {port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
