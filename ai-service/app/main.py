from fastapi import FastAPI
from app.routers import placeholder
from app import parser   # ✅ import

app = FastAPI(title="AI Service", version="0.1.0")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ai-service", "version": "0.1.0"}

app.include_router(placeholder.router, prefix="/api/v1", tags=["placeholder"])
app.include_router(parser.router, prefix="/api/v1", tags=["parser"])
