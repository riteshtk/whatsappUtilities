from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class MessageType(str, Enum):
    """Types of messages supported."""
    TEXT = "text"
    AUDIO = "audio"
    DOCUMENT = "document"
    IMAGE = "image"
    VIDEO = "video"

class MessageStatus(str, Enum):
    """Message status."""
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    PENDING = "pending"

class SendMessageRequest(BaseModel):
    """Request model for sending a message."""
    to: str = Field(..., description="WhatsApp phone number (with country code, no +)")
    message_type: MessageType = Field(..., description="Type of message to send")
    text: Optional[str] = Field(None, description="Text content for text messages")
    media_url: Optional[str] = Field(None, description="URL of media file for media messages")
    media_caption: Optional[str] = Field(None, description="Caption for media messages")

class SendMessageResponse(BaseModel):
    """Response model for sent messages."""
    message_id: str = Field(..., description="WhatsApp message ID")
    status: MessageStatus = Field(..., description="Message status")
    timestamp: datetime = Field(..., description="Message timestamp")

class ReceivedMessage(BaseModel):
    """Model for received messages."""
    message_id: str = Field(..., description="WhatsApp message ID")
    from_number: str = Field(..., description="Sender's phone number")
    message_type: MessageType = Field(..., description="Type of message")
    text: Optional[str] = Field(None, description="Text content")
    media_url: Optional[str] = Field(None, description="URL of media file")
    media_id: Optional[str] = Field(None, description="WhatsApp media ID")
    timestamp: datetime = Field(..., description="Message timestamp")
    status: MessageStatus = Field(default=MessageStatus.DELIVERED, description="Message status")

class WebhookMessage(BaseModel):
    """Model for webhook message data."""
    id: str
    from_: str = Field(alias="from")
    timestamp: str
    type: str
    text: Optional[Dict[str, Any]] = None
    audio: Optional[Dict[str, Any]] = None
    document: Optional[Dict[str, Any]] = None
    image: Optional[Dict[str, Any]] = None
    video: Optional[Dict[str, Any]] = None

class WebhookEntry(BaseModel):
    """Model for webhook entry data."""
    id: str
    changes: List[Dict[str, Any]]

class WebhookData(BaseModel):
    """Model for webhook data."""
    object: str
    entry: List[WebhookEntry]

class MessageListResponse(BaseModel):
    """Response model for listing messages."""
    messages: List[ReceivedMessage] = Field(..., description="List of received messages")
    total: int = Field(..., description="Total number of messages")