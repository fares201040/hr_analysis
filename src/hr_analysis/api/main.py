"""Main entry point for HR Analytics API."""

import uvicorn
from fastapi import FastAPI
import sys
from pathlib import Path

app = FastAPI()

# Import and include routers here
from src.hr_analysis.api.endpoints import (
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

# --- Allow running with 'python main.py' ---
if __name__ == "__main__":
    # Clean data before starting the server
    from src.hr_analysis.data_cleaner import clean_all_csvs
    clean_all_csvs()
    uvicorn.run(
        "src.hr_analysis.api.main:app",
        host="0.0.0.0",
        port=10000,
        reload=True
    )
