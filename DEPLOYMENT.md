# WhatsApp Messaging Utility - Deployment Guide

## 🚀 Deployment Options

This guide covers multiple deployment options for your WhatsApp Messaging Utility, from simple cloud platforms to containerized solutions.

## 📋 Prerequisites

- WhatsApp Business API credentials configured
- Domain name (for production webhooks)
- SSL certificate (for HTTPS)
- Cloud platform account (AWS, Google Cloud, etc.)

## 🌐 Deployment Options

### 1. Railway (Recommended for Quick Start)

Railway is the easiest way to deploy with minimal configuration.

#### Setup Steps:

1. **Create Railway Account**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login to Railway
   railway login
   ```

2. **Deploy Backend**
   ```bash
   cd backend
   railway init
   railway up
   ```

3. **Configure Environment Variables**
   ```bash
   railway variables set WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
   railway variables set WHATSAPP_ACCESS_TOKEN=your_access_token
   railway variables set WHATSAPP_WEBHOOK_VERIFY_TOKEN=your_webhook_token
   railway variables set MEDIA_BASE_URL=https://your-app.railway.app
   ```

4. **Deploy UI (Optional)**
   ```bash
   cd ../ui
   railway init
   railway up
   ```

#### Railway Configuration Files:

**File: `railway.json`**
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health"
  }
}
```

### 2. Heroku

#### Setup Steps:

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Ubuntu
   sudo snap install --classic heroku
   ```

2. **Deploy Backend**
   ```bash
   cd backend
   heroku create your-whatsapp-api
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

3. **Configure Environment Variables**
   ```bash
   heroku config:set WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
   heroku config:set WHATSAPP_ACCESS_TOKEN=your_access_token
   heroku config:set WHATSAPP_WEBHOOK_VERIFY_TOKEN=your_webhook_token
   heroku config:set MEDIA_BASE_URL=https://your-whatsapp-api.herokuapp.com
   ```

#### Heroku Configuration Files:

**File: `backend/Procfile`**
```
web: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**File: `backend/runtime.txt`**
```
python-3.11.0
```

### 3. Docker Deployment

#### Create Docker Configuration:

**File: `Dockerfile`**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ .

# Create uploads directory
RUN mkdir -p uploads

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**File: `docker-compose.yml`**
```yaml
version: '3.8'

services:
  whatsapp-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - WHATSAPP_PHONE_NUMBER_ID=${WHATSAPP_PHONE_NUMBER_ID}
      - WHATSAPP_ACCESS_TOKEN=${WHATSAPP_ACCESS_TOKEN}
      - WHATSAPP_WEBHOOK_VERIFY_TOKEN=${WHATSAPP_WEBHOOK_VERIFY_TOKEN}
      - MEDIA_BASE_URL=${MEDIA_BASE_URL}
      - HOST=0.0.0.0
      - PORT=8000
    volumes:
      - ./uploads:/app/uploads
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - whatsapp-api
    restart: unless-stopped
```

**File: `nginx.conf`**
```nginx
events {
    worker_connections 1024;
}

http {
    upstream whatsapp_api {
        server whatsapp-api:8000;
    }

    server {
        listen 80;
        server_name your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        location / {
            proxy_pass http://whatsapp_api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /uploads/ {
            alias /app/uploads/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

#### Deploy with Docker:

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 4. AWS EC2 Deployment

#### Setup Steps:

1. **Launch EC2 Instance**
   - Choose Ubuntu 20.04 LTS
   - Select t3.micro (free tier eligible)
   - Configure security groups (ports 22, 80, 443, 8000)

2. **Connect and Setup**
   ```bash
   # Connect to instance
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and dependencies
   sudo apt install python3.11 python3.11-pip python3.11-venv nginx -y
   ```

3. **Deploy Application**
   ```bash
   # Clone your repository
   git clone https://github.com/your-username/CommsUtlities.git
   cd CommsUtlities
   
   # Create virtual environment
   python3.11 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   cd backend
   pip install -r requirements.txt
   
   # Create .env file
   nano .env
   # Add your environment variables
   ```

4. **Setup Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/whatsapp-api.service
   ```

   **File: `/etc/systemd/system/whatsapp-api.service`**
   ```ini
   [Unit]
   Description=WhatsApp Messaging Utility API
   After=network.target

   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/CommsUtlities/backend
   Environment=PATH=/home/ubuntu/CommsUtlities/venv/bin
   ExecStart=/home/ubuntu/CommsUtlities/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

5. **Start Service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable whatsapp-api
   sudo systemctl start whatsapp-api
   sudo systemctl status whatsapp-api
   ```

6. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/whatsapp-api
   ```

   **File: `/etc/nginx/sites-available/whatsapp-api`**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       location /uploads/ {
           alias /home/ubuntu/CommsUtlities/backend/uploads/;
           expires 1y;
           add_header Cache-Control "public, immutable";
       }
   }
   ```

   ```bash
   sudo ln -s /etc/nginx/sites-available/whatsapp-api /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### 5. Google Cloud Platform

#### Setup Steps:

1. **Create App Engine Application**
   ```bash
   # Install Google Cloud SDK
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   
   # Initialize project
   gcloud init
   ```

2. **Create App Engine Configuration**

   **File: `backend/app.yaml`**
   ```yaml
   runtime: python311
   env: standard

   instance_class: F1

   automatic_scaling:
     min_instances: 1
     max_instances: 10

   env_variables:
     WHATSAPP_PHONE_NUMBER_ID: "your_phone_number_id"
     WHATSAPP_ACCESS_TOKEN: "your_access_token"
     WHATSAPP_WEBHOOK_VERIFY_TOKEN: "your_webhook_token"
     MEDIA_BASE_URL: "https://your-project.appspot.com"

   handlers:
   - url: /.*
     script: auto
   ```

3. **Deploy to App Engine**
   ```bash
   cd backend
   gcloud app deploy
   ```

### 6. DigitalOcean App Platform

#### Setup Steps:

1. **Create App Spec**

   **File: `.do/app.yaml`**
   ```yaml
   name: whatsapp-messaging-utility
   services:
   - name: api
     source_dir: /backend
     github:
       repo: your-username/CommsUtlities
       branch: main
     run_command: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     envs:
     - key: WHATSAPP_PHONE_NUMBER_ID
       value: your_phone_number_id
     - key: WHATSAPP_ACCESS_TOKEN
       value: your_access_token
     - key: WHATSAPP_WEBHOOK_VERIFY_TOKEN
       value: your_webhook_token
     - key: MEDIA_BASE_URL
       value: https://your-app.ondigitalocean.app
   ```

2. **Deploy**
   ```bash
   doctl apps create --spec .do/app.yaml
   ```

## 🔧 Environment Configuration

### Production Environment Variables

```bash
# WhatsApp API Configuration
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_ACCESS_TOKEN=your_access_token
WHATSAPP_WEBHOOK_VERIFY_TOKEN=your_webhook_verify_token
WHATSAPP_API_BASE_URL=https://graph.facebook.com/v18.0

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Media Configuration
MEDIA_BASE_URL=https://your-domain.com

# Database (if using)
DATABASE_URL=postgresql://user:password@host:port/database

# Security
SECRET_KEY=your-secret-key
API_KEY=your-api-key
```

## 🛡️ Security Considerations

### 1. Environment Variables
- Never commit `.env` files to version control
- Use secure secret management (AWS Secrets Manager, Azure Key Vault)
- Rotate API keys regularly

### 2. HTTPS Configuration
- Always use HTTPS in production
- Configure SSL certificates (Let's Encrypt, Cloudflare)
- Redirect HTTP to HTTPS

### 3. API Security
- Implement API key authentication
- Add rate limiting
- Use CORS properly
- Validate all inputs

### 4. File Security
- Validate file types and sizes
- Scan uploaded files for malware
- Use secure file storage (AWS S3, Google Cloud Storage)

## 📊 Monitoring and Logging

### 1. Application Monitoring
```python
# Add to backend/app/main.py
import logging
from prometheus_client import Counter, Histogram, generate_latest

# Metrics
REQUEST_COUNT = Counter('requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('request_duration_seconds', 'Request duration')

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_DURATION.observe(duration)
    
    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

### 2. Health Checks
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "whatsapp_configured": settings.validate_whatsapp_config()
    }
```

### 3. Logging Configuration
```python
import logging
from pythonjsonlogger import jsonlogger

# Configure JSON logging
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
```

## 🚀 Deployment Checklist

### Pre-Deployment
- [ ] WhatsApp Business API credentials configured
- [ ] Domain name and SSL certificate ready
- [ ] Environment variables documented
- [ ] Database configured (if needed)
- [ ] File storage configured
- [ ] Monitoring setup

### Deployment
- [ ] Choose deployment platform
- [ ] Configure environment variables
- [ ] Deploy application
- [ ] Configure webhook URL in Meta Developer Portal
- [ ] Test all endpoints
- [ ] Verify file uploads work
- [ ] Test webhook receiving

### Post-Deployment
- [ ] Monitor application logs
- [ ] Set up alerts
- [ ] Test with real WhatsApp messages
- [ ] Performance testing
- [ ] Security audit
- [ ] Backup strategy

## 🔄 CI/CD Pipeline

### GitHub Actions Example

**File: `.github/workflows/deploy.yml`**
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        cd backend
        python -m pytest tests/
    
    - name: Deploy to Railway
      run: |
        railway up --service backend
      env:
        RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [Heroku Python Guide](https://devcenter.heroku.com/articles/getting-started-with-python)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [AWS EC2 User Guide](https://docs.aws.amazon.com/ec2/)
- [Google Cloud App Engine](https://cloud.google.com/appengine/docs)

---

**Ready to deploy?** Choose your preferred platform and follow the step-by-step guide above!