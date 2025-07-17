"""Dashboard endpoints for HR Analytics API."""

from fastapi import APIRouter

router = APIRouter()

@router.get("/dashboard")
def get_dashboard():
    """Get dashboard data."""
    return {"dashboard": {}}
