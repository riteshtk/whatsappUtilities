# WhatsApp Messaging Utility - API Documentation

## 🚀 Complete API Reference for External Platforms

This documentation provides everything external platforms need to integrate with our WhatsApp Messaging Utility API. The API supports all message types including text, images, documents, audio, and video files.

## 📋 Quick Links

- **[Complete API Documentation](API_DOCUMENTATION.md)** - Detailed endpoint reference
- **[Interactive API Tester](api_test.html)** - Test all endpoints in your browser
- **[Python SDK](whatsapp_client.py)** - Ready-to-use Python client library
- **[Live API Docs](http://localhost:8000/docs)** - Interactive Swagger documentation

## 🔗 API Base URL

```
http://localhost:8000
```

For production, replace with your actual domain.

## 🚀 Quick Start

### 1. Test API Connection

```bash
curl -X GET "http://localhost:8000/health"
```

### 2. Send Your First Message

```bash
curl -X POST "http://localhost:8000/api/messages/send-text" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "to=1234567890&text=Hello from API!"
```

### 3. Use the Interactive Tester

Open `api_test.html` in your browser to test all endpoints with a user-friendly interface.

## 📱 Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/messages/send-text` | POST | Send text messages |
| `/api/messages/send-media` | POST | Send media files (images, docs, audio, video) |
| `/api/messages/media/upload` | POST | Upload files to server |
| `/api/messages/` | GET | Get received messages |
| `/api/messages/{id}` | GET | Get specific message |
| `/health` | GET | API health check |
| `/config` | GET | Configuration status |

## 🛠️ Integration Examples

### Python Integration

```python
import requests

# Send text message
def send_whatsapp_text(to, text):
    response = requests.post(
        "http://localhost:8000/api/messages/send-text",
        data={"to": to, "text": text}
    )
    return response.json()

# Send image
def send_whatsapp_image(to, image_url, caption=None):
    response = requests.post(
        "http://localhost:8000/api/messages/send-media",
        data={
            "to": to,
            "media_type": "image",
            "media_url": image_url,
            "caption": caption
        }
    )
    return response.json()

# Usage
send_whatsapp_text("1234567890", "Hello from Python!")
send_whatsapp_image("1234567890", "https://example.com/image.jpg", "Check this out!")
```

### JavaScript Integration

```javascript
// Send text message
async function sendWhatsAppText(to, text) {
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
async function sendWhatsAppMedia(to, mediaType, mediaUrl, caption = null) {
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

// Usage
sendWhatsAppText('1234567890', 'Hello from JavaScript!');
sendWhatsAppMedia('1234567890', 'image', 'https://example.com/image.jpg', 'Beautiful image!');
```

### PHP Integration

```php
<?php
// Send text message
function sendWhatsAppText($to, $text) {
    $url = 'http://localhost:8000/api/messages/send-text';
    $data = ['to' => $to, 'text' => $text];
    
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
function sendWhatsAppMedia($to, $mediaType, $mediaUrl, $caption = null) {
    $url = 'http://localhost:8000/api/messages/send-media';
    $data = [
        'to' => $to,
        'media_type' => $mediaType,
        'media_url' => $mediaUrl
    ];
    
    if ($caption) $data['caption'] = $caption;
    
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

// Usage
$result = sendWhatsAppText('1234567890', 'Hello from PHP!');
$result = sendWhatsAppMedia('1234567890', 'image', 'https://example.com/image.jpg', 'Check this out!');
?>
```

## 📁 Supported File Types

### Images
- **Formats:** JPG, JPEG, PNG, GIF
- **Max Size:** 5MB
- **Use Cases:** Profile pictures, screenshots, photos

### Documents
- **Formats:** PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, TXT
- **Max Size:** 100MB
- **Use Cases:** Contracts, reports, presentations

### Audio
- **Formats:** MP3, WAV, OGG, M4A
- **Max Size:** 16MB
- **Use Cases:** Voice messages, music files

### Video
- **Formats:** MP4, AVI, MOV, 3GP
- **Max Size:** 16MB
- **Use Cases:** Video messages, clips

## 🔄 Webhook Integration

### Webhook URL
```
POST https://your-domain.com/webhook
```

### Webhook Payload
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

## 🐍 Python SDK Usage

### Installation
```bash
# Copy the SDK file to your project
cp whatsapp_client.py /path/to/your/project/
```

### Basic Usage
```python
from whatsapp_client import WhatsAppClient

# Initialize client
client = WhatsAppClient("http://localhost:8000")

# Send text message
result = client.send_text("1234567890", "Hello from Python SDK!")

# Send image
result = client.send_image("1234567890", "https://example.com/image.jpg", "Check this out!")

# Upload and send file
result = client.upload_and_send_file("1234567890", "/path/to/document.pdf", "document", "Important document")

# Get received messages
messages = client.get_messages(limit=10)

# Check API health
health = client.health_check()
```

### Advanced Usage
```python
# Send different media types
client.send_document("1234567890", "https://example.com/file.pdf", "Important document")
client.send_audio("1234567890", "https://example.com/audio.mp3")
client.send_video("1234567890", "https://example.com/video.mp4", "Check this video!")

# Upload file first, then send
upload_result = client.upload_file("/path/to/local/file.jpg")
if "media_url" in upload_result:
    client.send_image("1234567890", upload_result["media_url"], "Uploaded image!")

# Get specific message
message = client.get_message("wamid.HBgLMTY4MjMxODQ5OTQVAgARGBI0QTAxOUMyQ0YyQUU1RUEzNzgA")

# Test media accessibility
test_result = client.test_media_access("filename.jpg")
```

## 🧪 Testing Tools

### 1. Interactive HTML Tester
Open `api_test.html` in your browser for a user-friendly interface to test all endpoints.

### 2. Command Line Testing
```bash
# Test health
curl -X GET "http://localhost:8000/health"

# Send text message
curl -X POST "http://localhost:8000/api/messages/send-text" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "to=1234567890&text=Hello World!"

# Send image
curl -X POST "http://localhost:8000/api/messages/send-media" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "to=1234567890&media_type=image&media_url=https://example.com/image.jpg&caption=Beautiful!"

# Upload file
curl -X POST "http://localhost:8000/api/messages/media/upload" \
  -F "file=@/path/to/your/file.jpg"

# Get messages
curl -X GET "http://localhost:8000/api/messages/?limit=10"
```

### 3. Python SDK Testing
```bash
# Run the SDK test
python whatsapp_client.py
```

## 📊 Response Codes

| Code | Description |
|------|-------------|
| 200  | Success |
| 400  | Bad Request - Invalid parameters |
| 404  | Not Found - Message not found |
| 500  | Internal Server Error |

## 🔧 Error Handling

### Common Errors
```json
{
  "detail": "Invalid phone number format"
}
```

```json
{
  "detail": "Failed to upload file: File too large"
}
```

```json
{
  "detail": "Failed to send message: Media upload error"
}
```

## 🚀 Production Considerations

### Security
- Implement API key authentication
- Use HTTPS for all requests
- Validate and sanitize all inputs
- Implement rate limiting

### Performance
- Use connection pooling
- Implement retry logic
- Cache frequently accessed data
- Monitor API usage

### Monitoring
- Log all API calls
- Monitor response times
- Track error rates
- Set up alerts for failures

## 📚 Additional Resources

- **Interactive API Docs:** `http://localhost:8000/docs`
- **Health Check:** `http://localhost:8000/health`
- **Configuration:** `http://localhost:8000/config`
- **Complete Documentation:** [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## 🆘 Support

For issues or questions:
1. Check the server logs for error details
2. Test with the interactive HTML tester
3. Verify your WhatsApp Business API configuration
4. Use the Python SDK for easier integration

---

**Ready to integrate?** Start with the [Interactive API Tester](api_test.html) or use the [Python SDK](whatsapp_client.py) for quick integration!