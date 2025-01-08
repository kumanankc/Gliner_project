from fastapi import FastAPI, HTTPException
import logging
from app.config import settings
from app.schemas import TextInput, Entity, EntityResponse, HealthResponse
from app.model import NERModel

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# Global model instance
model = None



@app.on_event("startup")
async def load_model():
    """Load the NER model during application startup."""
    global model
    try:
        logger.info("Starting model initialization...")
        model = NERModel(model_name=settings.MODEL_NAME)
        model.warm_up()
        logger.info("Model loaded successfully.")
    except Exception as e:
        logger.error(f"Error during model initialization: {str(e)}")
        raise RuntimeError(f"Failed to initialize model: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint showing API information."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": "GLiNER Entity Extraction API",
        "docs": "/docs",
        "health": "/health"
    }
    
@app.post("/predict")
async def predict(input_data: TextInput):
    """Predict named entities in the input text."""
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Get predictions
        predictions = model.predict(input_data.text, input_data.labels)
        

        formatted_output = []
        for pred in predictions:
            formatted_output.append(f"{pred['text']} => {pred['label']}")
        
        return formatted_output
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
    
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check if the service is healthy."""
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return HealthResponse(
        status="healthy",
        model_name=settings.MODEL_NAME,
        version=settings.VERSION
    )