#!/usr/bin/env python3
"""
WhatsApp Messaging Utility - Python Client SDK

A simple Python client library for sending and receiving WhatsApp messages
through the WhatsApp Messaging Utility API.

Usage:
    from whatsapp_client import WhatsAppClient
    
    client = WhatsAppClient("http://localhost:8000")
    
    # Send text message
    result = client.send_text("1234567890", "Hello from Python!")
    
    # Send image
    result = client.send_image("1234567890", "https://example.com/image.jpg", "Check this out!")
    
    # Upload and send file
    result = client.upload_and_send_file("1234567890", "/path/to/file.pdf", "document")
    
    # Get received messages
    messages = client.get_messages(limit=10)
"""

import requests
import json
from typing import Optional, List, Dict, Any
from pathlib import Path


class WhatsAppClient:
    """Python client for WhatsApp Messaging Utility API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the WhatsApp client.
        
        Args:
            base_url: Base URL of the WhatsApp API server
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request and handle errors."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}
    
    def send_text(self, to: str, text: str) -> Dict[str, Any]:
        """
        Send a text message.
        
        Args:
            to: Phone number with country code (no +)
            text: Message text
            
        Returns:
            API response with message details
        """
        data = {"to": to, "text": text}
        return self._make_request("POST", "/api/messages/send-text", data=data)
    
    def send_media(self, to: str, media_type: str, media_url: str, caption: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a media message.
        
        Args:
            to: Phone number with country code (no +)
            media_type: Type of media (image, document, audio, video)
            media_url: URL of the media file
            caption: Optional caption for the media
            
        Returns:
            API response with message details
        """
        data = {
            "to": to,
            "media_type": media_type,
            "media_url": media_url
        }
        if caption:
            data["caption"] = caption
        
        return self._make_request("POST", "/api/messages/send-media", data=data)
    
    def send_image(self, to: str, image_url: str, caption: Optional[str] = None) -> Dict[str, Any]:
        """Send an image message."""
        return self.send_media(to, "image", image_url, caption)
    
    def send_document(self, to: str, document_url: str, caption: Optional[str] = None) -> Dict[str, Any]:
        """Send a document message."""
        return self.send_media(to, "document", document_url, caption)
    
    def send_audio(self, to: str, audio_url: str) -> Dict[str, Any]:
        """Send an audio message."""
        return self.send_media(to, "audio", audio_url)
    
    def send_video(self, to: str, video_url: str, caption: Optional[str] = None) -> Dict[str, Any]:
        """Send a video message."""
        return self.send_media(to, "video", video_url, caption)
    
    def upload_file(self, file_path: str) -> Dict[str, Any]:
        """
        Upload a file to the server.
        
        Args:
            file_path: Path to the file to upload
            
        Returns:
            API response with upload details and media URL
        """
        file_path = Path(file_path)
        if not file_path.exists():
            return {"error": f"File not found: {file_path}"}
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            return self._make_request("POST", "/api/messages/media/upload", files=files)
    
    def upload_and_send_file(self, to: str, file_path: str, media_type: str, caption: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a file and send it as a media message.
        
        Args:
            to: Phone number with country code (no +)
            file_path: Path to the file to upload
            media_type: Type of media (image, document, audio, video)
            caption: Optional caption for the media
            
        Returns:
            API response with message details
        """
        # First upload the file
        upload_result = self.upload_file(file_path)
        
        if "error" in upload_result:
            return upload_result
        
        media_url = upload_result.get("media_url")
        if not media_url:
            return {"error": "No media URL returned from upload"}
        
        # Then send the media
        return self.send_media(to, media_type, media_url, caption)
    
    def get_messages(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        Get received messages.
        
        Args:
            limit: Number of messages to return
            offset: Number of messages to skip
            
        Returns:
            API response with messages list
        """
        params = {"limit": limit, "offset": offset}
        return self._make_request("GET", "/api/messages/", params=params)
    
    def get_message(self, message_id: str) -> Dict[str, Any]:
        """
        Get a specific message by ID.
        
        Args:
            message_id: WhatsApp message ID
            
        Returns:
            API response with message details
        """
        return self._make_request("GET", f"/api/messages/{message_id}")
    
    def test_media_access(self, filename: str) -> Dict[str, Any]:
        """
        Test if a media file is accessible.
        
        Args:
            filename: Name of the file to test
            
        Returns:
            API response with accessibility status
        """
        return self._make_request("GET", f"/api/messages/media/test/{filename}")
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check API health status.
        
        Returns:
            API response with health status
        """
        return self._make_request("GET", "/health")
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get API configuration status.
        
        Returns:
            API response with configuration details
        """
        return self._make_request("GET", "/config")


# Example usage and testing
if __name__ == "__main__":
    # Initialize client
    client = WhatsAppClient("http://localhost:8000")
    
    print("🔧 WhatsApp API Client Test")
    print("=" * 40)
    
    # Test health check
    print("\n1. Health Check:")
    health = client.health_check()
    print(json.dumps(health, indent=2))
    
    # Test configuration
    print("\n2. Configuration:")
    config = client.get_config()
    print(json.dumps(config, indent=2))
    
    # Test sending text message
    print("\n3. Send Text Message:")
    text_result = client.send_text("1234567890", "Hello from Python SDK!")
    print(json.dumps(text_result, indent=2))
    
    # Test sending image
    print("\n4. Send Image:")
    image_result = client.send_image("1234567890", "https://picsum.photos/400/300", "Random image!")
    print(json.dumps(image_result, indent=2))
    
    # Test getting messages
    print("\n5. Get Messages:")
    messages = client.get_messages(limit=5)
    print(json.dumps(messages, indent=2))
    
    print("\n✅ Test completed!")
    print("\n📚 Usage Examples:")
    print("""
    # Basic usage
    from whatsapp_client import WhatsAppClient
    
    client = WhatsAppClient("http://localhost:8000")
    
    # Send text message
    result = client.send_text("1234567890", "Hello World!")
    
    # Send image
    result = client.send_image("1234567890", "https://example.com/image.jpg", "Check this out!")
    
    # Upload and send file
    result = client.upload_and_send_file("1234567890", "/path/to/file.pdf", "document", "Important document")
    
    # Get received messages
    messages = client.get_messages(limit=10)
    """)