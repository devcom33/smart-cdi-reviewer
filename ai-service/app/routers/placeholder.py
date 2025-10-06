"""
Placeholder router for demonstration.
Replace with real API endpoints (e.g., /search, /compliance).
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/placeholder")
def placeholder_route():
    return {"message": "This is a placeholder endpoint."}
