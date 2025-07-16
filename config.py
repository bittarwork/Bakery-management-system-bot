import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

# Import environment configuration if .env file doesn't exist
try:
    if not os.path.exists('.env'):
        import env_config
except ImportError:
    pass

class Config:
    """Configuration class for the Bakery Management Bot"""
    
    # AI Provider Configuration - Switch to Gemini for premium features
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "gemini")  # Changed to gemini for premium features
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # Google Gemini Configuration - Enhanced for premium API
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "AIzaSyD813Gu6WszqsjbEq-5MvO5GYlxj5By8fE")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-pro-latest")  # Upgraded to Pro model
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    DATABASE_TYPE: str = os.getenv("DATABASE_TYPE", "postgresql")
    
    # Bot Configuration - Enhanced for premium features
    BOT_NAME: str = os.getenv("BOT_NAME", "BakeryBot Pro")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2048"))  # Increased for detailed responses
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.4"))  # Balanced for creativity and accuracy
    
    # Advanced AI Configuration
    TOP_P: float = float(os.getenv("TOP_P", "0.95"))  # Nucleus sampling parameter
    TOP_K: int = int(os.getenv("TOP_K", "40"))  # Top-k sampling parameter
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Premium Features Configuration
    ENABLE_ADVANCED_ANALYTICS: bool = os.getenv("ENABLE_ADVANCED_ANALYTICS", "true").lower() == "true"
    ENABLE_SMART_CACHING: bool = os.getenv("ENABLE_SMART_CACHING", "true").lower() == "true"
    ENABLE_MULTI_LANGUAGE: bool = os.getenv("ENABLE_MULTI_LANGUAGE", "true").lower() == "true"
    ENABLE_VOICE_RESPONSES: bool = os.getenv("ENABLE_VOICE_RESPONSES", "false").lower() == "true"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that all required configuration is present"""
        if cls.AI_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when using OpenAI")
        if cls.AI_PROVIDER == "gemini" and not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required when using Google Gemini")
        if not cls.DATABASE_URL:
            raise ValueError("DATABASE_URL is required")
        return True

# Create global config instance
config = Config() 