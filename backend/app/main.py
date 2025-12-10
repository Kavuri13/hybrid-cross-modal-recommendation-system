from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from app.api.routes import router
from app.models.clip_model import CLIPModel
from app.utils.faiss_index import FAISSIndex
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Cross-Modal Product Recommendation API",
    description="CLIP-based product recommendation system with image and text search",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:5173",  # Vite dev server
        "http://frontend:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for product images
if os.path.exists("/app/data/images"):
    app.mount("/images", StaticFiles(directory="/app/data/images"), name="images")

# Include API routes
app.include_router(router, prefix="/api/v1")

# Global variables for models
clip_model = None
faiss_index = None

@app.on_event("startup")
async def startup_event():
    """Initialize models on startup"""
    global clip_model, faiss_index
    
    try:
        logger.info("Loading CLIP model...")
        clip_model = CLIPModel()
        
        logger.info("Loading FAISS index...")
        faiss_index = FAISSIndex()
        
        # Store models in app state
        app.state.clip_model = clip_model
        app.state.faiss_index = faiss_index
        
        logger.info("Models loaded successfully!")
        
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        # Continue without models for now
        pass

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Cross-Modal Product Recommendation API",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check with model status"""
    return {
        "status": "healthy",
        "models": {
            "clip_loaded": hasattr(app.state, 'clip_model') and app.state.clip_model is not None,
            "faiss_loaded": hasattr(app.state, 'faiss_index') and app.state.faiss_index is not None
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )