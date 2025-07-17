"""Main entry point for HR Analytics API."""

import uvicorn
from fastapi import FastAPI
import sys
from pathlib import Path

app = FastAPI()

# --- Run data cleaner at startup ---
@app.on_event("startup")
def run_data_cleaner():
    # Import DataCleaner from the correct path
    sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
    try:
        from src.hr_analysis.data_cleaner import DataCleaner
        cleaner = DataCleaner()
        cleaner.clean_all_csvs()
    except Exception as e:
        print(f"[Startup] Data cleaning failed: {e}")

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
    
    uvicorn.run(
        "src.hr_analysis.api.main:app",
        host="0.0.0.0",
        port=10000,
        reload=True
    )
