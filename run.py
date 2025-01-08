import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run(
        app,  
        host="0.0.0.0",
        port=8000,
        workers=1,  # Number of worker processes
        reload=False  # Disable reload in production
    )