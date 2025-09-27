from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import placeholder
from app import splitter, embeddings, retriever, parser
from app.services.contract_review import parse_contract, splitter_contract
from app.services.contract_review import retriever_contract
from app.services.contract_review import Generation
from app.services.contract_review.indexing import index_contract

from app.services.contract_review import indexing
from pydantic import BaseModel

app = FastAPI(title="AI Service", version="0.1.0")

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ai-service", "version": "0.1.0"}

app.include_router(placeholder.router, prefix="/api/v1", tags=["placeholder"])
app.include_router(parser.router, prefix="/api/v1", tags=["parser"])
app.include_router(splitter.router, prefix="/api/v1", tags=["splitter"])
app.include_router(embeddings.router, prefix="/api/v1", tags=["embeddings"])
app.include_router(retriever.router, prefix="/api/v1", tags=["retriever"])

#  Contract review routers
#app.include_router(indexing.router, prefix="/api/v1/contracts", tags=["contract-indexing"])
app.include_router(retriever_contract.router, prefix="/api/v1/contracts", tags=["contract-retrieval"])
#app.include_router(Generation.router, prefix="/api/v1/contracts", tags=["Generation-llm"])


class DocumentInput(BaseModel):
    file_name: str
    extracted_text: str
    header: str

@app.post("/analyze")
async def analyze(input: DocumentInput):
    index_contract(input.extracted_text)
    return Generation.generate_issues()