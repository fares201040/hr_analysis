"""Employee endpoints for HR Analytics API."""

from fastapi import APIRouter

router = APIRouter()

@router.get("/employees")
def list_employees():
    """List all employees."""
    return {"employees": []}
