import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """
    Application settings loaded from environment variables.
    Provides default values and type conversion for configuration.
    """
    
    # MongoDB Configuration
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "todo_app")
    
    # Application Configuration
    APP_NAME: str = os.getenv("APP_NAME", "Todo App API")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Security Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    # CORS Configuration
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080").split(",")
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Database Configuration
    CONNECTION_TIMEOUT: int = int(os.getenv("CONNECTION_TIMEOUT", "10000"))
    SERVER_SELECTION_TIMEOUT: int = int(os.getenv("SERVER_SELECTION_TIMEOUT", "5000"))
    
    @classmethod
    def get_database_url(cls) -> str:
        """Get the complete MongoDB URL for database connection."""
        return cls.MONGODB_URL
    
    @classmethod
    def get_database_name(cls) -> str:
        """Get the database name."""
        return cls.DATABASE_NAME
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment."""
        return not cls.DEBUG
    
    @classmethod
    def get_cors_origins(cls) -> list:
        """Get CORS allowed origins as a list."""
        return [origin.strip() for origin in cls.ALLOWED_ORIGINS if origin.strip()]


# Global settings instance
settings = Settings()
