"""
Centralized logging for Dorost health agent
Tracks all agent decisions, performance, and user interactions
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

# Create logs directory
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Create logger
logger = logging.getLogger("dorost")
logger.setLevel(logging.DEBUG)

# File handler - detailed logs
file_handler = logging.FileHandler(
    LOG_DIR / f"dorost_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
)
file_handler.setLevel(logging.DEBUG)

# Console handler - important info only
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_agent_input(agent_name: str, user_input: str):
    """Log user input to an agent"""
    logger.info(f"AGENT INPUT: {agent_name} received message ({len(user_input)} chars)")
    logger.debug(f"AGENT INPUT CONTENT: {user_input[:200]}..." if len(user_input) > 200 else f"AGENT INPUT CONTENT: {user_input}")

def log_agent_output(agent_name: str, output: str, confidence: float = None):
    """Log agent output"""
    logger.info(f"AGENT OUTPUT: {agent_name} generated response ({len(output)} chars)" + 
                (f", confidence: {confidence:.2f}" if confidence else ""))
    logger.debug(f"AGENT OUTPUT CONTENT: {output[:300]}..." if len(output) > 300 else f"AGENT OUTPUT CONTENT: {output}")

def log_specialty_routing(symptoms: list, recommended_specialist: str, confidence: float):
    """Log specialty routing decision"""
    logger.info(f"SPECIALTY ROUTING: {symptoms} → {recommended_specialist} (confidence: {confidence:.2f})")

def log_red_flag_detected(symptom: str, urgency: str):
    """Log when a red flag is detected"""
    logger.warning(f"🚨 RED FLAG DETECTED: {symptom} (urgency: {urgency})")

def log_session_start(session_id: str):
    """Log start of user session"""
    logger.info(f"SESSION START: {session_id}")

def log_session_end(session_id: str, num_messages: int, duration: float):
    """Log end of user session"""
    logger.info(f"SESSION END: {session_id} - {num_messages} messages in {duration:.2f}s")

def log_error(agent_name: str, error: Exception):
    """Log agent error"""
    logger.error(f"AGENT ERROR in {agent_name}: {str(error)}", exc_info=True)

def get_logger():
    """Get the dorost logger"""
    return logger
