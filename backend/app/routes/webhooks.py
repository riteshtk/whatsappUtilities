from fastapi import APIRouter, HTTPException, Request, Query
from fastapi.responses import PlainTextResponse
import logging
import json

from ..config import settings
from ..services.whatsapp import whatsapp_service
from .messages import add_received_message

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhook", tags=["webhooks"])

@router.get("/")
async def verify_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_challenge: str = Query(..., alias="hub.challenge"),
    hub_verify_token: str = Query(..., alias="hub.verify_token")
):
    """Verify webhook endpoint for WhatsApp."""
    try:
        # Verify the webhook
        if hub_mode == "subscribe" and hub_verify_token == settings.WHATSAPP_WEBHOOK_VERIFY_TOKEN:
            logger.info("Webhook verified successfully")
            return PlainTextResponse(content=hub_challenge)
        else:
            logger.error("Webhook verification failed")
            raise HTTPException(status_code=403, detail="Forbidden")
            
    except Exception as e:
        logger.error(f"Error verifying webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def receive_webhook(request: Request):
    """Receive webhook notifications from WhatsApp."""
    try:
        # Get the raw body
        body = await request.body()
        data = json.loads(body.decode('utf-8'))
        
        logger.info(f"Received webhook: {json.dumps(data, indent=2)}")
        
        # Parse the webhook data
        message = whatsapp_service.parse_webhook_message(data)
        
        if message:
            # Add to received messages storage
            add_received_message(message)
            logger.info(f"Processed message: {message.message_id} from {message.from_number}")
            
            # Handle different message types
            if message.message_type.value == "text":
                logger.info(f"Text message: {message.text}")
            elif message.message_type.value in ["audio", "document", "image", "video"]:
                logger.info(f"Media message: {message.message_type.value}")
                if message.media_id:
                    # Download media if needed
                    media_url = await whatsapp_service.download_media(message.media_id)
                    if media_url:
                        logger.info(f"Downloaded media: {media_url}")
        else:
            logger.info("No message data found in webhook")
        
        return {"status": "ok"}
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in webhook: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def webhook_status():
    """Get webhook status and configuration."""
    try:
        return {
            "webhook_configured": bool(settings.WHATSAPP_WEBHOOK_VERIFY_TOKEN),
            "phone_number_id": settings.WHATSAPP_PHONE_NUMBER_ID,
            "api_base_url": settings.WHATSAPP_API_BASE_URL,
            "verify_token_set": bool(settings.WHATSAPP_WEBHOOK_VERIFY_TOKEN)
        }
    except Exception as e:
        logger.error(f"Error getting webhook status: {e}")
        raise HTTPException(status_code=500, detail=str(e))