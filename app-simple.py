from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()}), 200

@app.route("/api/consultation/start", methods=["POST"])
def start():
    data = request.get_json()
    initial_query = data.get("initial_query", "")
    return jsonify({
        "status": "success",
        "consultation_id": "test-123",
        "message": f"Received: {initial_query[:50]}..."
    }), 201

@app.route("/api/metrics/evaluation", methods=["GET"])
def metrics():
    return jsonify({
        "status": "success",
        "metrics": {"agents": 6, "uptime": "100%"}
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
