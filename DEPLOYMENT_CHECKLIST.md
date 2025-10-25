# 🚀 WhatsApp Messaging Utility - Deployment Checklist

## 📋 Pre-Deployment Checklist

### ✅ Environment Setup
- [ ] WhatsApp Business API credentials obtained
- [ ] Meta Developer account created
- [ ] Phone Number ID and Access Token ready
- [ ] Webhook verification token generated
- [ ] Domain name registered (for production)
- [ ] SSL certificate obtained (Let's Encrypt, Cloudflare, etc.)

### ✅ Code Preparation
- [ ] All code committed to version control
- [ ] Environment variables documented
- [ ] `.env` file created with production values
- [ ] Dependencies updated and tested
- [ ] Code reviewed and tested locally

### ✅ Platform Selection
Choose your deployment platform:
- [ ] **Railway** (Recommended for beginners)
- [ ] **Heroku** (Easy deployment)
- [ ] **Docker** (Containerized deployment)
- [ ] **AWS EC2** (Full control)
- [ ] **Google Cloud** (Scalable)
- [ ] **DigitalOcean** (Simple VPS)

## 🚀 Quick Deployment Options

### Option 1: Railway (Easiest)

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login and deploy
railway login
cd backend
railway init
railway up

# 3. Set environment variables
railway variables set WHATSAPP_PHONE_NUMBER_ID=your_id
railway variables set WHATSAPP_ACCESS_TOKEN=your_token
railway variables set WHATSAPP_WEBHOOK_VERIFY_TOKEN=your_token
railway variables set MEDIA_BASE_URL=https://your-app.railway.app
```

### Option 2: Docker (Local/Server)

```bash
# 1. Setup environment
./deploy.sh setup

# 2. Deploy with Docker
./deploy.sh docker

# 3. Check status
docker-compose ps
docker-compose logs -f
```

### Option 3: Heroku

```bash
# 1. Install Heroku CLI
# macOS: brew install heroku/brew/heroku
# Ubuntu: sudo snap install --classic heroku

# 2. Deploy
./deploy.sh heroku

# 3. Set environment variables
heroku config:set WHATSAPP_PHONE_NUMBER_ID=your_id
heroku config:set WHATSAPP_ACCESS_TOKEN=your_token
heroku config:set WHATSAPP_WEBHOOK_VERIFY_TOKEN=your_token
heroku config:set MEDIA_BASE_URL=https://your-app.herokuapp.com
```

## 🔧 Post-Deployment Configuration

### 1. Configure WhatsApp Webhook

1. **Get your deployment URL:**
   - Railway: Check your app dashboard
   - Heroku: `heroku info`
   - Docker: `http://your-server-ip:8000`
   - Custom domain: `https://your-domain.com`

2. **Update Meta Developer Portal:**
   - Go to [Meta for Developers](https://developers.facebook.com/)
   - Navigate to your WhatsApp Business app
   - Go to WhatsApp > Configuration
   - Set Webhook URL: `https://your-domain.com/webhook`
   - Set Verify Token: (same as WHATSAPP_WEBHOOK_VERIFY_TOKEN)
   - Subscribe to `messages` events

### 2. Test Your Deployment

```bash
# Test health endpoint
curl https://your-domain.com/health

# Test sending a message
curl -X POST "https://your-domain.com/api/messages/send-text" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "to=1234567890&text=Hello from production!"

# Test webhook (send a message to your WhatsApp Business number)
```

### 3. Monitor Your Application

```bash
# Check logs
# Railway: railway logs
# Heroku: heroku logs --tail
# Docker: docker-compose logs -f

# Check status
curl https://your-domain.com/health
curl https://your-domain.com/config
```

## 🛡️ Security Checklist

### ✅ Basic Security
- [ ] HTTPS enabled (SSL certificate configured)
- [ ] Environment variables secured (not in code)
- [ ] API keys rotated and secured
- [ ] File uploads validated
- [ ] Rate limiting implemented
- [ ] CORS configured properly

### ✅ Advanced Security
- [ ] API authentication implemented
- [ ] Input validation and sanitization
- [ ] File type and size restrictions
- [ ] Malware scanning for uploads
- [ ] Database security (if using)
- [ ] Backup strategy implemented

## 📊 Monitoring Checklist

### ✅ Application Monitoring
- [ ] Health check endpoint working
- [ ] Logs being collected
- [ ] Error tracking configured
- [ ] Performance monitoring
- [ ] Uptime monitoring

### ✅ WhatsApp API Monitoring
- [ ] Message delivery tracking
- [ ] Webhook receiving messages
- [ ] Media upload/download working
- [ ] Error handling for API failures
- [ ] Rate limit monitoring

## 🔄 Maintenance Checklist

### ✅ Regular Tasks
- [ ] Monitor application logs
- [ ] Check WhatsApp API quotas
- [ ] Update dependencies
- [ ] Backup data (if using database)
- [ ] Test webhook functionality
- [ ] Review security settings

### ✅ Monthly Tasks
- [ ] Rotate API keys
- [ ] Review access logs
- [ ] Update SSL certificates
- [ ] Performance optimization
- [ ] Security audit

## 🚨 Troubleshooting

### Common Issues

#### 1. Webhook Not Receiving Messages
```bash
# Check webhook configuration
curl -X GET "https://your-domain.com/webhook/status"

# Verify webhook URL in Meta Developer Portal
# Ensure HTTPS is working
# Check firewall settings
```

#### 2. Media Upload Failures
```bash
# Check media URL accessibility
curl -I https://your-domain.com/uploads/test-file.jpg

# Verify MEDIA_BASE_URL is set correctly
# Check file permissions
# Test with small files first
```

#### 3. API Authentication Issues
```bash
# Verify credentials
curl -X GET "https://your-domain.com/config"

# Check environment variables
# Verify WhatsApp API credentials
# Test with Meta's API directly
```

### Debug Commands

```bash
# Check application status
curl https://your-domain.com/health

# Test message sending
curl -X POST "https://your-domain.com/api/messages/send-text" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "to=1234567890&text=Test message"

# Check received messages
curl https://your-domain.com/api/messages/

# Test file upload
curl -X POST "https://your-domain.com/api/messages/media/upload" \
  -F "file=@test.jpg"
```

## 📚 Platform-Specific Guides

### Railway Deployment
1. Create account at [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Set environment variables in dashboard
4. Deploy automatically on push

### Heroku Deployment
1. Create account at [heroku.com](https://heroku.com)
2. Install Heroku CLI
3. Create app: `heroku create your-app-name`
4. Set config vars: `heroku config:set KEY=value`
5. Deploy: `git push heroku main`

### Docker Deployment
1. Install Docker and Docker Compose
2. Run: `./deploy.sh docker`
3. Access at `http://localhost:8000`
4. Configure reverse proxy (nginx) for production

### AWS EC2 Deployment
1. Launch EC2 instance (Ubuntu 20.04)
2. Configure security groups
3. Install Docker: `sudo apt install docker.io docker-compose`
4. Clone repository and deploy
5. Configure domain and SSL

## 🎯 Success Criteria

Your deployment is successful when:

- [ ] Health check returns 200 OK
- [ ] Can send text messages via API
- [ ] Can send media messages via API
- [ ] Can receive messages via webhook
- [ ] File uploads work correctly
- [ ] All endpoints respond properly
- [ ] SSL certificate is valid
- [ ] Webhook is configured in Meta Developer Portal

## 🆘 Getting Help

If you encounter issues:

1. **Check the logs** for error messages
2. **Test individual endpoints** with curl
3. **Verify environment variables** are set correctly
4. **Check WhatsApp API status** in Meta Developer Portal
5. **Review the troubleshooting section** above
6. **Check platform-specific documentation**

## 📞 Support Resources

- **WhatsApp Business API Docs:** [developers.facebook.com/docs/whatsapp](https://developers.facebook.com/docs/whatsapp)
- **Railway Docs:** [docs.railway.app](https://docs.railway.app)
- **Heroku Docs:** [devcenter.heroku.com](https://devcenter.heroku.com)
- **Docker Docs:** [docs.docker.com](https://docs.docker.com)

---

**Ready to deploy?** Choose your platform and follow the checklist above! 🚀