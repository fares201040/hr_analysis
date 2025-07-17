"""Main entry point for HR Analytics API."""

from fastapi import FastAPI

app = FastAPI()

# Import and include routers here
from .endpoints import (
    dashboard,
    employee,
    report,
)

app.include_router(employee.router)
app.include_router(report.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    """Root endpoint for health check."""
    return {"status": "HR Analytics API is running"}
