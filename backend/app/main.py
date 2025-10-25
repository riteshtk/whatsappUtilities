from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import logging
import uvicorn
import os

from .config import settings
from .routes import messages, webhooks

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="WhatsApp Messaging Utility",
    description="A utility for sending and receiving WhatsApp messages via Business API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploaded media
uploads_dir = "uploads"
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Include routers
app.include_router(messages.router)
app.include_router(webhooks.router)

@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info("Starting WhatsApp Messaging Utility...")
    
    # Validate configuration
    if not settings.validate_whatsapp_config():
        logger.error("WhatsApp configuration is incomplete!")
        logger.error("Please check your environment variables:")
        logger.error(f"  WHATSAPP_PHONE_NUMBER_ID: {'✓' if settings.WHATSAPP_PHONE_NUMBER_ID else '✗'}")
        logger.error(f"  WHATSAPP_ACCESS_TOKEN: {'✓' if settings.WHATSAPP_ACCESS_TOKEN else '✗'}")
        logger.error(f"  WHATSAPP_WEBHOOK_VERIFY_TOKEN: {'✓' if settings.WHATSAPP_WEBHOOK_VERIFY_TOKEN else '✗'}")
    else:
        logger.info("WhatsApp configuration validated successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("Shutting down WhatsApp Messaging Utility...")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "WhatsApp Messaging Utility API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "whatsapp_configured": settings.validate_whatsapp_config()
    }

@app.get("/config")
async def get_config():
    """Get configuration status (without sensitive data)."""
    return {
        "phone_number_id_set": bool(settings.WHATSAPP_PHONE_NUMBER_ID),
        "access_token_set": bool(settings.WHATSAPP_ACCESS_TOKEN),
        "webhook_verify_token_set": bool(settings.WHATSAPP_WEBHOOK_VERIFY_TOKEN),
        "api_base_url": settings.WHATSAPP_API_BASE_URL,
        "host": settings.HOST,
        "port": settings.PORT,
        "debug": settings.DEBUG
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )