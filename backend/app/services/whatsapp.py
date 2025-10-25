import httpx
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime

from ..config import settings
from ..models.message import MessageType, MessageStatus, SendMessageRequest, SendMessageResponse, ReceivedMessage

logger = logging.getLogger(__name__)

class WhatsAppService:
    """Service for interacting with WhatsApp Business API."""
    
    def __init__(self):
        self.base_url = settings.WHATSAPP_API_BASE_URL
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.access_token = settings.WHATSAPP_ACCESS_TOKEN
        self.headers = settings.get_whatsapp_headers()
        
    async def send_text_message(self, to: str, text: str) -> SendMessageResponse:
        """Send a text message via WhatsApp."""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {
                "body": text
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    headers=self.headers,
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                
                data = response.json()
                message_id = data["messages"][0]["id"]
                
                return SendMessageResponse(
                    message_id=message_id,
                    status=MessageStatus.SENT,
                    timestamp=datetime.now()
                )
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error sending text message: {e}")
            raise Exception(f"Failed to send message: {e.response.text}")
        except Exception as e:
            logger.error(f"Error sending text message: {e}")
            raise Exception(f"Failed to send message: {str(e)}")
    
    async def send_media_message(self, to: str, media_type: str, media_url: str, caption: Optional[str] = None) -> SendMessageResponse:
        """Send a media message (audio, document, image, video) via WhatsApp."""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": media_type,
            media_type: {
                "link": media_url
            }
        }
        
        # Add caption if provided
        if caption and media_type in ["document", "image", "video"]:
            payload[media_type]["caption"] = caption
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    headers=self.headers,
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                
                data = response.json()
                message_id = data["messages"][0]["id"]
                
                return SendMessageResponse(
                    message_id=message_id,
                    status=MessageStatus.SENT,
                    timestamp=datetime.now()
                )
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error sending media message: {e}")
            raise Exception(f"Failed to send media message: {e.response.text}")
        except Exception as e:
            logger.error(f"Error sending media message: {e}")
            raise Exception(f"Failed to send media message: {str(e)}")
    
    async def download_media(self, media_id: str) -> Optional[str]:
        """Download media file from WhatsApp."""
        try:
            # First, get media URL
            media_url = f"{self.base_url}/{media_id}"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    media_url,
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                
                media_data = response.json()
                download_url = media_data["url"]
                
                # Download the actual media file
                download_response = await client.get(
                    download_url,
                    headers=self.headers,
                    timeout=60.0
                )
                download_response.raise_for_status()
                
                # Save media file (you might want to save to a specific directory)
                # For now, return the URL
                return download_url
                
        except Exception as e:
            logger.error(f"Error downloading media {media_id}: {e}")
            return None
    
    async def get_media_info(self, media_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a media file."""
        try:
            url = f"{self.base_url}/{media_id}"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                
                return response.json()
                
        except Exception as e:
            logger.error(f"Error getting media info for {media_id}: {e}")
            return None
    
    def parse_webhook_message(self, webhook_data: Dict[str, Any]) -> Optional[ReceivedMessage]:
        """Parse incoming webhook message."""
        try:
            entry = webhook_data.get("entry", [])
            if not entry:
                return None
                
            changes = entry[0].get("changes", [])
            if not changes:
                return None
                
            value = changes[0].get("value", {})
            messages = value.get("messages", [])
            
            if not messages:
                return None
                
            message = messages[0]
            
            # Extract message details
            message_id = message.get("id", "")
            from_number = message.get("from", "")
            timestamp = message.get("timestamp", "")
            message_type = message.get("type", "text")
            
            # Parse timestamp
            try:
                dt = datetime.fromtimestamp(int(timestamp))
            except:
                dt = datetime.now()
            
            # Extract content based on message type
            text_content = None
            media_url = None
            media_id = None
            
            if message_type == "text":
                text_content = message.get("text", {}).get("body", "")
            elif message_type in ["audio", "document", "image", "video"]:
                media_data = message.get(message_type, {})
                media_id = media_data.get("id", "")
                media_url = media_data.get("link", "")
                text_content = media_data.get("caption", "")
            
            return ReceivedMessage(
                message_id=message_id,
                from_number=from_number,
                message_type=MessageType(message_type),
                text=text_content,
                media_url=media_url,
                media_id=media_id,
                timestamp=dt,
                status=MessageStatus.DELIVERED
            )
            
        except Exception as e:
            logger.error(f"Error parsing webhook message: {e}")
            return None

# Global service instance
whatsapp_service = WhatsAppService()