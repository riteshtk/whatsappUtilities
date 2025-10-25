import streamlit as st
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="WhatsApp Messaging Utility",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #25D366;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-message {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.375rem;
        margin: 1rem 0;
    }
    .error-message {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.375rem;
        margin: 1rem 0;
    }
    .message-card {
        border: 1px solid #dee2e6;
        border-radius: 0.375rem;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

def check_backend_connection():
    """Check if backend is running."""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def send_text_message(to, text):
    """Send a text message."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/messages/send-text",
            data={"to": to, "text": text},
            timeout=30
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def send_media_message(to, media_type, media_url, caption=None):
    """Send a media message."""
    try:
        data = {"to": to, "media_type": media_type, "media_url": media_url}
        if caption:
            data["caption"] = caption
        
        response = requests.post(
            f"{BACKEND_URL}/api/messages/send-media",
            data=data,
            timeout=30
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def get_messages():
    """Get received messages."""
    try:
        response = requests.get(f"{BACKEND_URL}/api/messages/", timeout=10)
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def upload_media(file):
    """Upload a media file."""
    try:
        files = {"file": file}
        response = requests.post(
            f"{BACKEND_URL}/api/messages/media/upload",
            files=files,
            timeout=30
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def main():
    # Header
    st.markdown('<h1 class="main-header">📱 WhatsApp Messaging Utility</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Backend URL configuration
        backend_url = st.text_input(
            "Backend URL",
            value=BACKEND_URL,
            help="URL of the FastAPI backend"
        )
        
        # Check backend connection
        if st.button("Check Connection"):
            if check_backend_connection():
                st.success("✅ Backend connected")
            else:
                st.error("❌ Backend not reachable")
        
        st.markdown("---")
        st.markdown("### 📋 Quick Setup")
        st.markdown("""
        1. **Start Backend**: `cd backend && python -m uvicorn app.main:app --reload`
        2. **Configure WhatsApp**: Set up your `.env` file
        3. **Test Connection**: Use the button above
        """)
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📤 Send Messages", "📥 Received Messages", "⚙️ Settings"])
    
    with tab1:
        st.header("Send WhatsApp Messages")
        
        # Message type selection
        message_type = st.radio(
            "Message Type",
            ["Text", "Audio", "Document", "Image", "Video"],
            horizontal=True
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Recipient phone number
            phone_number = st.text_input(
                "Phone Number",
                placeholder="1234567890 (with country code, no +)",
                help="Enter the recipient's WhatsApp number with country code (no + sign)"
            )
            
            # Message content based on type
            if message_type == "Text":
                message_text = st.text_area(
                    "Message Text",
                    placeholder="Enter your message here...",
                    height=100
                )
            else:
                # Media upload
                uploaded_file = st.file_uploader(
                    f"Upload {message_type}",
                    type=["mp3", "wav", "ogg", "pdf", "doc", "docx", "jpg", "jpeg", "png", "gif", "mp4", "avi", "mov"],
                    help=f"Upload a {message_type.lower()} file"
                )
                
                caption = st.text_area(
                    "Caption (Optional)",
                    placeholder="Add a caption for your media...",
                    height=80
                )
        
        with col2:
            # Send button and status
            if st.button("🚀 Send Message", type="primary", use_container_width=True):
                if not phone_number:
                    st.error("Please enter a phone number")
                elif message_type == "Text" and not message_text:
                    st.error("Please enter a message")
                elif message_type != "Text" and not uploaded_file:
                    st.error(f"Please upload a {message_type.lower()} file")
                else:
                    with st.spinner("Sending message..."):
                        if message_type == "Text":
                            result, status_code = send_text_message(phone_number, message_text)
                        else:
                            # Upload file first
                            upload_result, upload_status = upload_media(uploaded_file)
                            if upload_status == 200:
                                media_url = upload_result.get("media_url")
                                result, status_code = send_media_message(
                                    phone_number, 
                                    message_type.lower(), 
                                    media_url, 
                                    caption if caption else None
                                )
                            else:
                                result = upload_result
                                status_code = upload_status
                        
                        if status_code == 200:
                            st.success("✅ Message sent successfully!")
                            st.json(result)
                        else:
                            st.error(f"❌ Failed to send message: {result.get('detail', 'Unknown error')}")
    
    with tab2:
        st.header("Received Messages")
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            if st.button("🔄 Refresh Messages"):
                st.rerun()
        
        # Get and display messages
        with st.spinner("Loading messages..."):
            messages_data, status_code = get_messages()
            
            if status_code == 200:
                messages = messages_data.get("messages", [])
                total = messages_data.get("total", 0)
                
                st.info(f"📊 Total messages: {total}")
                
                # Debug: Show raw message data
                if st.checkbox("🔍 Show Debug Info"):
                    st.json(messages_data)
                
                if messages:
                    for i, message in enumerate(messages):
                        # Create expandable message cards
                        try:
                            from_number = message.get('from_number', 'Unknown')
                            timestamp = message.get('timestamp', 'Unknown')
                            message_type = message.get('message_type', 'Unknown')
                            text_content = message.get('text', '')
                            
                            with st.expander(f"📱 Message {i+1} from {from_number}", expanded=True):
                                col1, col2 = st.columns([2, 1])
                                
                                with col1:
                                    st.write(f"**📱 From:** {from_number}")
                                    st.write(f"**📅 Time:** {timestamp}")
                                    st.write(f"**📝 Type:** {message_type}")
                                    
                                    # Display message content
                                    if text_content:
                                        st.write(f"**💬 Content:** {text_content}")
                                    else:
                                        st.write("**💬 Content:** Media message")
                                    
                                    # Display media information
                                    if message.get('media_url'):
                                        st.write(f"**🔗 Media URL:** {message.get('media_url')}")
                                    
                                    if message.get('media_id'):
                                        st.write(f"**🆔 Media ID:** {message.get('media_id')}")
                                
                                with col2:
                                    # Message status
                                    status = message.get('status', 'Unknown')
                                    if status == 'delivered':
                                        st.success("✅ Delivered")
                                    elif status == 'sent':
                                        st.info("📤 Sent")
                                    elif status == 'read':
                                        st.success("👁️ Read")
                                    else:
                                        st.warning(f"❓ {status}")
                                
                                st.markdown("---")
                        except Exception as e:
                            st.error(f"Error displaying message {i+1}: {e}")
                            st.json(message)
                else:
                    st.info("📭 No messages received yet")
            else:
                st.error(f"❌ Failed to load messages: {messages_data.get('error', 'Unknown error')}")
    
    with tab3:
        st.header("Settings & Configuration")
        
        st.subheader("🔧 Backend Configuration")
        
        # Display current configuration
        try:
            config_response = requests.get(f"{BACKEND_URL}/config", timeout=5)
            if config_response.status_code == 200:
                config = config_response.json()
                
                st.json(config)
                
                # Configuration status
                st.subheader("📊 Configuration Status")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Phone Number ID",
                        "✅ Set" if config.get("phone_number_id_set") else "❌ Not Set"
                    )
                
                with col2:
                    st.metric(
                        "Access Token",
                        "✅ Set" if config.get("access_token_set") else "❌ Not Set"
                    )
                
                with col3:
                    st.metric(
                        "Webhook Token",
                        "✅ Set" if config.get("webhook_verify_token_set") else "❌ Not Set"
                    )
                
                if not all([config.get("phone_number_id_set"), config.get("access_token_set"), config.get("webhook_verify_token_set")]):
                    st.warning("⚠️ Some configuration is missing. Please check your .env file.")
            else:
                st.error("❌ Could not retrieve configuration")
        except Exception as e:
            st.error(f"❌ Error connecting to backend: {e}")
        
        st.subheader("📚 Setup Instructions")
        st.markdown("""
        ### Quick Setup Guide
        
        1. **Create Meta Developer Account**
           - Go to [Meta for Developers](https://developers.facebook.com/)
           - Create a new app and select "Business"
        
        2. **Add WhatsApp Product**
           - In your app, add the WhatsApp product
           - Get your Phone Number ID and Access Token
        
        3. **Configure Environment**
           - Copy `.env.example` to `.env`
           - Fill in your WhatsApp credentials
        
        4. **Set up Webhook**
           - Use ngrok for local testing: `ngrok http 8000`
           - Configure webhook URL in Meta Developer Portal
        
        5. **Start the Application**
           - Backend: `cd backend && python -m uvicorn app.main:app --reload`
           - UI: `cd ui && streamlit run app.py`
        """)
        
        st.subheader("🔗 Useful Links")
        st.markdown("""
        - [WhatsApp Business API Documentation](https://developers.facebook.com/docs/whatsapp)
        - [Meta for Developers](https://developers.facebook.com/)
        - [ngrok for Webhooks](https://ngrok.com/)
        """)

if __name__ == "__main__":
    main()