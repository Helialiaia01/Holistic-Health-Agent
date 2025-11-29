import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Central configuration for Health Agent"""
    
    # Google Cloud
    GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
    GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_GENAI_USE_VERTEXAI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "0") == "1"
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///health_agent.db")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/health_agent.log")
    
    # Health Agent
    MAX_PATTERN_MATCHES = int(os.getenv("MAX_PATTERN_MATCHES", "5"))
    CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))
    
    # Model
    MODEL_NAME = "gemini-2.5-flash-lite"
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        if not Config.GOOGLE_API_KEY and not Config.GOOGLE_GENAI_USE_VERTEXAI:
            raise ValueError(
                "Either GOOGLE_API_KEY must be set or GOOGLE_GENAI_USE_VERTEXAI must be True. "
                "Set in .env file (copy from .env.template)"
            )
        print("✅ Configuration loaded successfully")

# Create config instance
config = Config()
