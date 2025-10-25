# WhatsApp Messaging Utility - API Documentation

## 🚀 Overview

This API allows external platforms to send and receive WhatsApp messages through our WhatsApp Business API integration. It supports all message types including text, images, documents, audio, and video files.

## 🔗 Base URL

```
http://localhost:8000
```

For production, replace with your actual domain.

## 🔑 Authentication

Currently, no authentication is required for local development. For production, implement proper API key authentication.

## 📱 API Endpoints

### 1. Send Text Message

**Endpoint:** `POST /api/messages/send-text`

Send a text message to a WhatsApp number.

**Request Body (Form Data):**
```
to: 1234567890          # Phone number with country code (no +)
text: Hello World!      # Message content
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/messages/send-text" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "to=1234567890&text=Hello from API!"
```

**Response:**
```json
{
  "message_id": "wamid.HBgLMTY4MjMxODQ5OTQVAgARGBI0QTAxOUMyQ0YyQUU1RUEzNzgA",
  "status": "sent",
  "timestamp": "2025-01-25T14:00:00Z"
}
```

### 2. Send Media Message

**Endpoint:** `POST /api/messages/send-media`

Send media files (images, documents, audio, video) to a WhatsApp number.

**Request Body (Form Data):**
```
to: 1234567890                    # Phone number with country code (no +)
media_type: image                 # Type: image, document, audio, video
media_url: https://example.com/file.jpg  # Publicly accessible URL
caption: Check this out!          # Optional caption
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/messages/send-media" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "to=1234567890&media_type=image&media_url=https://example.com/image.jpg&caption=Beautiful sunset!"
```

**Response:**
```json
{
  "message_id": "wamid.HBgLMTY4MjMxODQ5OTQVAgARGBI0QTAxOUMyQ0YyQUU1RUEzNzgA",
  "status": "sent",
  "timestamp": "2025-01-25T14:00:00Z"
}
```

### 3. Upload Media File

**Endpoint:** `POST /api/messages/media/upload`

Upload a media file to our server and get a publicly accessible URL.

**Request Body (Multipart Form):**
```
file: [binary file data]  # The actual file to upload
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/messages/media/upload" \
  -F "file=@/path/to/your/image.jpg"
```

**Response:**
```json
{
  "filename": "image.jpg",
  "content_type": "image/jpeg",
  "media_url": "http://localhost:8000/uploads/uuid-filename.jpg",
  "file_size": 12345,
  "message": "File uploaded successfully to local storage."
}
```

### 4. Send Message (JSON Format)

**Endpoint:** `POST /api/messages/send`

Send a message using JSON format (supports both text and media).

**Request Body (JSON):**
```json
{
  "to": "1234567890",
  "message_type": "text",
  "text": "Hello World!",
  "media_url": null,
  "media_caption": null
}
```

**For Media Messages:**
```json
{
  "to": "1234567890",
  "message_type": "image",
  "text": null,
  "media_url": "https://example.com/image.jpg",
  "media_caption": "Check this out!"
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/messages/send" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "1234567890",
    "message_type": "text",
    "text": "Hello from JSON API!"
  }'
```

### 5. Get Received Messages

**Endpoint:** `GET /api/messages/`

Retrieve all received messages.

**Query Parameters:**
```
limit: 50    # Number of messages to return (default: 50)
offset: 0    # Number of messages to skip (default: 0)
```

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/messages/?limit=10&offset=0"
```

**Response:**
```json
{
  "messages": [
    {
      "message_id": "wamid.HBgLMTY4MjMxODQ5OTQVAgARGBI0QTAxOUMyQ0YyQUU1RUEzNzgA",
      "from_number": "1234567890",
      "message_type": "text",
      "text": "Hello from WhatsApp!",
      "media_url": null,
      "media_id": null,
      "timestamp": "2025-01-25T14:00:00Z",
      "status": "delivered"
    }
  ],
  "total": 1
}
```

### 6. Get Specific Message

**Endpoint:** `GET /api/messages/{message_id}`

Get details of a specific message.

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/messages/wamid.HBgLMTY4MjMxODQ5OTQVAgARGBI0QTAxOUMyQ0YyQUU1RUEzNzgA"
```

### 7. Test Media Access

**Endpoint:** `GET /api/messages/media/test/{filename}`

Test if a media file is accessible.

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/messages/media/test/uuid-filename.jpg"
```

## 📁 Supported File Types

### Images
- **Formats:** JPG, JPEG, PNG, GIF
- **Max Size:** 5MB
- **Example:** Profile pictures, screenshots, photos

### Documents
- **Formats:** PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, TXT
- **Max Size:** 100MB
- **Example:** Contracts, reports, presentations

### Audio
- **Formats:** MP3, WAV, OGG, M4A
- **Max Size:** 16MB
- **Example:** Voice messages, music files

### Video
- **Formats:** MP4, AVI, MOV, 3GP
- **Max Size:** 16MB
- **Example:** Video messages, clips

## 🔄 Webhook Integration

### Webhook URL
```
POST https://your-domain.com/webhook
```

### Webhook Payload Example
```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "1549967299509011",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "15556360344",
              "phone_number_id": "875934978931928"
            },
            "messages": [
              {
                "id": "wamid.HBgLMTY4MjMxODQ5OTQVAgARGBI0QTAxOUMyQ0YyQUU1RUEzNzgA",
                "from": "1234567890",
                "timestamp": "1761418841",
                "type": "text",
                "text": {
                  "body": "Hello from WhatsApp!"
                }
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}
```

## 🛠️ Integration Examples

### Python Example
```python
import requests

# Send text message
def send_text_message(to, text):
    url = "http://localhost:8000/api/messages/send-text"
    data = {"to": to, "text": text}
    response = requests.post(url, data=data)
    return response.json()

# Send image
def send_image(to, image_url, caption=None):
    url = "http://localhost:8000/api/messages/send-media"
    data = {
        "to": to,
        "media_type": "image",
        "media_url": image_url,
        "caption": caption
    }
    response = requests.post(url, data=data)
    return response.json()

# Upload and send file
def upload_and_send_file(to, file_path, media_type, caption=None):
    # First upload the file
    upload_url = "http://localhost:8000/api/messages/media/upload"
    with open(file_path, 'rb') as f:
        files = {'file': f}
        upload_response = requests.post(upload_url, files=files)
    
    if upload_response.status_code == 200:
        media_url = upload_response.json()['media_url']
        
        # Then send the media
        send_url = "http://localhost:8000/api/messages/send-media"
        data = {
            "to": to,
            "media_type": media_type,
            "media_url": media_url,
            "caption": caption
        }
        response = requests.post(send_url, data=data)
        return response.json()
    else:
        return {"error": "Upload failed"}

# Usage examples
send_text_message("1234567890", "Hello from Python!")
send_image("1234567890", "https://example.com/image.jpg", "Check this out!")
upload_and_send_file("1234567890", "/path/to/document.pdf", "document", "Important document")
```

### JavaScript Example
```javascript
// Send text message
async function sendTextMessage(to, text) {
    const response = await fetch('http://localhost:8000/api/messages/send-text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `to=${to}&text=${encodeURIComponent(text)}`
    });
    return await response.json();
}

// Send media message
async function sendMediaMessage(to, mediaType, mediaUrl, caption = null) {
    const formData = new FormData();
    formData.append('to', to);
    formData.append('media_type', mediaType);
    formData.append('media_url', mediaUrl);
    if (caption) formData.append('caption', caption);
    
    const response = await fetch('http://localhost:8000/api/messages/send-media', {
        method: 'POST',
        body: formData
    });
    return await response.json();
}

// Upload file
async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch('http://localhost:8000/api/messages/media/upload', {
        method: 'POST',
        body: formData
    });
    return await response.json();
}

// Usage examples
sendTextMessage('1234567890', 'Hello from JavaScript!');
sendMediaMessage('1234567890', 'image', 'https://example.com/image.jpg', 'Beautiful image!');
```

### PHP Example
```php
<?php
// Send text message
function sendTextMessage($to, $text) {
    $url = 'http://localhost:8000/api/messages/send-text';
    $data = [
        'to' => $to,
        'text' => $text
    ];
    
    $options = [
        'http' => [
            'header' => "Content-type: application/x-www-form-urlencoded\r\n",
            'method' => 'POST',
            'content' => http_build_query($data)
        ]
    ];
    
    $context = stream_context_create($options);
    $result = file_get_contents($url, false, $context);
    return json_decode($result, true);
}

// Send media message
function sendMediaMessage($to, $mediaType, $mediaUrl, $caption = null) {
    $url = 'http://localhost:8000/api/messages/send-media';
    $data = [
        'to' => $to,
        'media_type' => $mediaType,
        'media_url' => $mediaUrl
    ];
    
    if ($caption) {
        $data['caption'] = $caption;
    }
    
    $options = [
        'http' => [
            'header' => "Content-type: application/x-www-form-urlencoded\r\n",
            'method' => 'POST',
            'content' => http_build_query($data)
        ]
    ];
    
    $context = stream_context_create($options);
    $result = file_get_contents($url, false, $context);
    return json_decode($result, true);
}

// Usage examples
$result = sendTextMessage('1234567890', 'Hello from PHP!');
$result = sendMediaMessage('1234567890', 'image', 'https://example.com/image.jpg', 'Check this out!');
?>
```

## 📊 Response Codes

| Code | Description |
|------|-------------|
| 200  | Success |
| 400  | Bad Request - Invalid parameters |
| 404  | Not Found - Message not found |
| 500  | Internal Server Error |

## 🔧 Error Handling

### Common Error Responses

**Invalid Phone Number:**
```json
{
  "detail": "Invalid phone number format"
}
```

**File Upload Error:**
```json
{
  "detail": "Failed to upload file: File too large"
}
```

**WhatsApp API Error:**
```json
{
  "detail": "Failed to send message: Media upload error"
}
```

## 🚀 Quick Start Guide

1. **Start the server:**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload
   ```

2. **Test the API:**
   ```bash
   curl -X GET "http://localhost:8000/health"
   ```

3. **Send your first message:**
   ```bash
   curl -X POST "http://localhost:8000/api/messages/send-text" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "to=1234567890&text=Hello World!"
   ```

## 📚 Additional Resources

- **API Documentation:** `http://localhost:8000/docs` (Interactive Swagger UI)
- **Health Check:** `http://localhost:8000/health`
- **Configuration:** `http://localhost:8000/config`

## 🆘 Support

For issues or questions:
1. Check the server logs for error details
2. Verify your WhatsApp Business API configuration
3. Ensure all required environment variables are set
4. Test with the interactive API documentation at `/docs`

---

**Note:** This API is designed for development and testing. For production use, implement proper authentication, rate limiting, and security measures.