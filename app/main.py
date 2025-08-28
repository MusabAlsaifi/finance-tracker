from fastapi import FastAPI
from config import settings

app = FastAPI(
    title="Finance tracker",
)

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.APP_NAME}"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "message": "API is running",
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG
    }
