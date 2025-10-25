import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings loaded from environment variables."""
    
    # WhatsApp Business API Configuration
    WHATSAPP_PHONE_NUMBER_ID: str = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
    WHATSAPP_ACCESS_TOKEN: str = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
    WHATSAPP_WEBHOOK_VERIFY_TOKEN: str = os.getenv("WHATSAPP_WEBHOOK_VERIFY_TOKEN", "")
    WHATSAPP_API_BASE_URL: str = os.getenv("WHATSAPP_API_BASE_URL", "https://graph.facebook.com/v18.0")
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Media Configuration
    MEDIA_BASE_URL: str = os.getenv("MEDIA_BASE_URL", "")
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    
    def validate_whatsapp_config(self) -> bool:
        """Validate that all required WhatsApp configuration is present."""
        required_fields = [
            self.WHATSAPP_PHONE_NUMBER_ID,
            self.WHATSAPP_ACCESS_TOKEN,
            self.WHATSAPP_WEBHOOK_VERIFY_TOKEN
        ]
        return all(field for field in required_fields)
    
    def get_whatsapp_headers(self) -> dict:
        """Get headers for WhatsApp API requests."""
        return {
            "Authorization": f"Bearer {self.WHATSAPP_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

# Global settings instance
settings = Settings()