# WhatsApp Messaging Utility

A comprehensive Python-based utility for sending and receiving WhatsApp messages using the WhatsApp Business API. This utility includes a FastAPI backend and a Streamlit web interface for easy testing and management.

## 🚀 Features

- **Send Text Messages**: Send text messages to any WhatsApp number
- **Send Media Messages**: Send audio, documents, images, and videos
- **Receive Messages**: Webhook-based message receiving with real-time updates
- **Media Support**: Upload and send various file types
- **Web Interface**: User-friendly Streamlit interface for testing
- **API Documentation**: Auto-generated API docs with FastAPI
- **Error Handling**: Comprehensive error handling and logging

## 📋 Prerequisites

- Python 3.9 or higher
- Meta (Facebook) Developer Account
- WhatsApp Business API access
- ngrok (for local webhook testing)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd CommsUtlities
```

### 2. Set Up Backend

```bash
cd backend
pip install -r requirements.txt
```

### 3. Set Up UI

```bash
cd ../ui
pip install -r requirements.txt
```

## 🔧 WhatsApp Business API Setup

### Step 1: Create Meta Developer Account

1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Sign up or log in with your Facebook account
3. Click "Create App" and select "Business" as the app type
4. Fill in your app details and create the app

### Step 2: Add WhatsApp Product

1. In your app dashboard, find "Add a Product"
2. Click "Set up" on the WhatsApp card
3. Follow the setup wizard

### Step 3: Get Your Credentials

1. **Phone Number ID**:
   - Go to WhatsApp > API Setup
   - Copy your Phone Number ID

2. **Access Token**:
   - In WhatsApp > API Setup
   - Copy your temporary access token
   - For production, create a permanent token

3. **Webhook Verify Token**:
   - Create a random string (e.g., "my_webhook_verify_token_123")
   - You'll use this when configuring the webhook

### Step 4: Configure Environment Variables

1. Copy the example environment file:
```bash
cp backend/.env.example backend/.env
```

2. Edit `backend/.env` with your credentials:
```env
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id_here
WHATSAPP_ACCESS_TOKEN=your_access_token_here
WHATSAPP_WEBHOOK_VERIFY_TOKEN=your_webhook_verify_token_here
WHATSAPP_API_BASE_URL=https://graph.facebook.com/v18.0
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### Step 5: Set Up Webhook (for receiving messages)

#### For Local Development:

1. **Install ngrok**:
```bash
# Download from https://ngrok.com/download
# Or use package manager:
brew install ngrok  # macOS
# or
sudo apt install ngrok  # Ubuntu
```

2. **Start your backend**:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

3. **Start ngrok** (in another terminal):
```bash
ngrok http 8000
```

4. **Configure webhook in Meta Developer Portal**:
   - Go to WhatsApp > Configuration
   - Set webhook URL: `https://your-ngrok-url.ngrok.io/webhook`
   - Set verify token: (same as WHATSAPP_WEBHOOK_VERIFY_TOKEN in your .env)
   - Subscribe to `messages` events

#### For Production:

- Use your production server URL instead of ngrok
- Ensure HTTPS is enabled
- Configure proper SSL certificates

## 🚀 Running the Application

### 1. Start the Backend

```bash
cd backend
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### 2. Start the UI

```bash
cd ui
streamlit run app.py
```

The UI will be available at `http://localhost:8501`

## 📱 Usage

### Using the Web Interface

1. **Send Messages Tab**:
   - Select message type (Text, Audio, Document, Image, Video)
   - Enter recipient's phone number (with country code, no +)
   - For text: Enter your message
   - For media: Upload file and add optional caption
   - Click "Send Message"

2. **Received Messages Tab**:
   - View all received messages
   - See message details, timestamps, and media URLs
   - Refresh to get latest messages

3. **Settings Tab**:
   - Check backend connection
   - View configuration status
   - Access setup instructions

### Using the API Directly

#### Send a Text Message

```bash
curl -X POST "http://localhost:8000/api/messages/send-text" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "to=1234567890&text=Hello from WhatsApp API!"
```

#### Send a Media Message

```bash
curl -X POST "http://localhost:8000/api/messages/send-media" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "to=1234567890&media_type=image&media_url=https://example.com/image.jpg&caption=Check this out!"
```

#### Get Received Messages

```bash
curl -X GET "http://localhost:8000/api/messages/"
```

## 🔧 API Endpoints

### Message Endpoints

- `POST /api/messages/send` - Send message (JSON)
- `POST /api/messages/send-text` - Send text message (form data)
- `POST /api/messages/send-media` - Send media message (form data)
- `GET /api/messages/` - Get received messages
- `GET /api/messages/{message_id}` - Get specific message
- `POST /api/messages/media/upload` - Upload media file

### Webhook Endpoints

- `GET /webhook` - Webhook verification
- `POST /webhook` - Receive incoming messages
- `GET /webhook/status` - Webhook status

### Utility Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /config` - Configuration status

## 📁 Project Structure

```
CommsUtlities/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration
│   │   ├── routes/
│   │   │   ├── messages.py      # Message endpoints
│   │   │   └── webhooks.py     # Webhook endpoints
│   │   ├── services/
│   │   │   └── whatsapp.py      # WhatsApp API client
│   │   └── models/
│   │       └── message.py       # Pydantic models
│   ├── requirements.txt
│   └── .env.example
├── ui/
│   ├── app.py                   # Streamlit UI
│   └── requirements.txt
├── README.md
└── .gitignore
```

## 🐛 Troubleshooting

### Common Issues

1. **"Backend not reachable" error**:
   - Ensure backend is running on port 8000
   - Check if backend URL is correct in UI

2. **WhatsApp API errors**:
   - Verify your credentials in `.env` file
   - Check if your access token is valid
   - Ensure phone number ID is correct

3. **Webhook not receiving messages**:
   - Verify ngrok is running and URL is accessible
   - Check webhook configuration in Meta Developer Portal
   - Ensure verify token matches your `.env` file

4. **Media upload issues**:
   - Check file size limits (WhatsApp has limits)
   - Verify file format is supported
   - Ensure media URL is accessible

### Debug Mode

Enable debug logging by setting `DEBUG=True` in your `.env` file.

## 🔒 Security Considerations

- Never commit your `.env` file to version control
- Use environment variables for production
- Implement proper authentication for production use
- Use HTTPS for webhook endpoints
- Regularly rotate your access tokens

## 📚 Additional Resources

- [WhatsApp Business API Documentation](https://developers.facebook.com/docs/whatsapp)
- [Meta for Developers](https://developers.facebook.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Review the API documentation at `/docs`
3. Check the logs for error messages
4. Ensure all prerequisites are met

For additional help, please open an issue in the repository.