# app/main.py
from fastapi import FastAPI
from app.routers import placeholder
from app import parser
from app import splitter, embeddings  # updated imports

app = FastAPI(title="AI Service", version="0.1.0")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ai-service", "version": "0.1.0"}

# Existing routers
app.include_router(placeholder.router, prefix="/api/v1", tags=["placeholder"])
app.include_router(parser.router, prefix="/api/v1", tags=["parser"])

# New routers
app.include_router(splitter.router, prefix="/api/v1", tags=["splitter"])
app.include_router(embeddings.router, prefix="/api/v1", tags=["embeddings"])
