# Main FastAPI entrypoint
# app/main.py
# Minimal FastAPI application for ai-service
# This will be the entrypoint of your AI microservice

from fastapi import FastAPI
from app.routers import placeholder

app = FastAPI(title="AI Service", version="0.1.0")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ai-service", "version": "0.1.0"}

# include placeholder router
app.include_router(placeholder.router, prefix="/api/v1", tags=["placeholder"])
