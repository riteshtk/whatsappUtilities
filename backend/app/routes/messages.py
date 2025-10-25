from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Optional
import logging

from ..models.message import (
    SendMessageRequest, 
    SendMessageResponse, 
    MessageListResponse, 
    ReceivedMessage,
    MessageType
)
from ..services.whatsapp import whatsapp_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/messages", tags=["messages"])

# In-memory storage for received messages (in production, use a database)
received_messages: List[ReceivedMessage] = []

@router.post("/send", response_model=SendMessageResponse)
async def send_message(request: SendMessageRequest):
    """Send a message via WhatsApp."""
    try:
        if request.message_type == MessageType.TEXT:
            if not request.text:
                raise HTTPException(status_code=400, detail="Text content is required for text messages")
            
            response = await whatsapp_service.send_text_message(
                to=request.to,
                text=request.text
            )
            return response
            
        elif request.message_type in [MessageType.AUDIO, MessageType.DOCUMENT, MessageType.IMAGE, MessageType.VIDEO]:
            if not request.media_url:
                raise HTTPException(status_code=400, detail="Media URL is required for media messages")
            
            response = await whatsapp_service.send_media_message(
                to=request.to,
                media_type=request.message_type.value,
                media_url=request.media_url,
                caption=request.media_caption
            )
            return response
            
        else:
            raise HTTPException(status_code=400, detail="Unsupported message type")
            
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-text")
async def send_text_message(
    to: str = Form(..., description="WhatsApp phone number (with country code, no +)"),
    text: str = Form(..., description="Text message content")
):
    """Send a text message via WhatsApp (form data)."""
    try:
        response = await whatsapp_service.send_text_message(to=to, text=text)
        return response
    except Exception as e:
        logger.error(f"Error sending text message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-media")
async def send_media_message(
    to: str = Form(..., description="WhatsApp phone number (with country code, no +)"),
    media_type: str = Form(..., description="Media type: audio, document, image, video"),
    media_url: str = Form(..., description="URL of the media file"),
    caption: Optional[str] = Form(None, description="Caption for the media")
):
    """Send a media message via WhatsApp (form data)."""
    try:
        if media_type not in ["audio", "document", "image", "video"]:
            raise HTTPException(status_code=400, detail="Invalid media type")
        
        response = await whatsapp_service.send_media_message(
            to=to,
            media_type=media_type,
            media_url=media_url,
            caption=caption
        )
        return response
    except Exception as e:
        logger.error(f"Error sending media message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=MessageListResponse)
async def get_messages(limit: int = 50, offset: int = 0):
    """Get received messages."""
    try:
        # In production, you would query a database here
        messages = received_messages[offset:offset + limit]
        return MessageListResponse(
            messages=messages,
            total=len(received_messages)
        )
    except Exception as e:
        logger.error(f"Error getting messages: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{message_id}")
async def get_message(message_id: str):
    """Get a specific message by ID."""
    try:
        for message in received_messages:
            if message.message_id == message_id:
                return message
        raise HTTPException(status_code=404, detail="Message not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting message {message_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/media/test/{filename}")
async def test_media_access(filename: str):
    """Test if a media file is accessible."""
    import os
    file_path = os.path.join("uploads", filename)
    if os.path.exists(file_path):
        return {"status": "accessible", "file_path": file_path}
    else:
        return {"status": "not_found", "file_path": file_path}

@router.post("/media/upload")
async def upload_media(file: UploadFile = File(...)):
    """Upload a media file and return its URL."""
    try:
        import os
        import uuid
        from datetime import datetime
        
        # Create uploads directory if it doesn't exist
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else ''
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        # Save file to disk
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Generate accessible URL
        # For WhatsApp to access files, we need a public URL
        from ..config import settings
        
        # Use configured media base URL if available, otherwise fallback to localhost
        if settings.MEDIA_BASE_URL:
            base_url = settings.MEDIA_BASE_URL.rstrip('/')
            logger.info(f"Using configured media base URL: {base_url}")
        else:
            base_url = f"http://localhost:{settings.PORT}"
            logger.warning(f"Using localhost URL: {base_url}")
            logger.warning("IMPORTANT: Set MEDIA_BASE_URL in .env to your ngrok URL for WhatsApp to access files")
        
        media_url = f"{base_url}/uploads/{unique_filename}"
        
        # Log the URL for debugging
        logger.info(f"Generated media URL: {media_url}")
        
        logger.info(f"File uploaded successfully: {file_path}")
        
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "media_url": media_url,
            "file_size": len(content),
            "message": "File uploaded successfully to local storage.",
            "test_url": f"{media_url}?test=1"  # Add test parameter to verify accessibility
        }
        
    except Exception as e:
        logger.error(f"Error uploading media: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def add_received_message(message: ReceivedMessage):
    """Add a received message to storage."""
    received_messages.append(message)
    # In production, save to database
    logger.info(f"Added received message: {message.message_id}")

def get_received_messages() -> List[ReceivedMessage]:
    """Get all received messages."""
    return received_messages