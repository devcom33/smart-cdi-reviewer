# app/main.py

from fastapi import FastAPI
from app.routers import placeholder
from app import splitter, embeddings, retriever, parser
from app.services.contract_review import parse_contract, splitter_contract  #  new import
from app.services.contract_review import retriever_contract
from app.services.contract_review import Generation

from app.services.contract_review import indexing







app = FastAPI(title="AI Service", version="0.1.0")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ai-service", "version": "0.1.0"}

# Existing routers
app.include_router(placeholder.router, prefix="/api/v1", tags=["placeholder"])
app.include_router(parser.router, prefix="/api/v1", tags=["parser"])
app.include_router(splitter.router, prefix="/api/v1", tags=["splitter"])
app.include_router(embeddings.router, prefix="/api/v1", tags=["embeddings"])
app.include_router(retriever.router, prefix="/api/v1", tags=["retriever"])

#  Contract review routers
app.include_router(indexing.router, prefix="/api/v1/contracts", tags=["contract-indexing"])
app.include_router(retriever_contract.router, prefix="/api/v1/contracts", tags=["contract-retrieval"])
app.include_router(Generation.router, prefix="/api/v1/contracts", tags=["Generation-llm"])