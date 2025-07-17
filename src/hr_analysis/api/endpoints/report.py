"""Report endpoints for HR Analytics API.

This module provides API endpoints for HR analytics reports.
The Employee Attendance Report endpoint aggregates attendance data per employee and date,
with optional filtering by employee_id, date range, and department.

Data is loaded from cleaned.csv in the clean_data folder.
"""

from pathlib import Path
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

import pandas as pd
from fastapi import (
    APIRouter,
    Query,
)

router = APIRouter()

@router.get("/reports/attendance", response_model=Dict[str, List[Dict[str, Any]]])
def employee_attendance_report(
    employee_id: Optional[str] = Query(None, description="Filter by employee ID"),
    department: Optional[str] = Query(None, description="Filter by department"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get Employee Attendance Report.

    Returns attendance records per employee and date, with optional filtering.

    - **employee_id**: Filter by employee ID
    - **department**: Filter by department name
    - **start_date**/**end_date**: Filter by date range (YYYY-MM-DD)

    Example response:
    {
        "attendance": [
            {
                "employee_id": "A10017",
                "date": "2025-07-01",
                "department": "Engineering",
                "day_type": "Working Day",
                "exception": "Lateness and Early Out"
            },
            ...
        ]
    }
    """
    data_path = Path(__file__).parent.parent.parent / "clean_data" / "cleaned.csv"
    df = pd.read_csv(data_path)

    # Standardize date column
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")

    # Apply filters
    if employee_id:
        df = df[df["employee_id"] == employee_id]
    if department and "department" in df.columns:
        df = df[df["department"].str.lower() == department.lower()]
    if start_date:
        df = df[df["date"] >= start_date]
    if end_date:
        df = df[df["date"] <= end_date]

    # Select relevant columns for attendance report
    columns = ["employee_id", "date", "department", "day_type", "exception"]
    attendance = df[columns].fillna("").to_dict(orient="records")

    return {"attendance": attendance}

@router.get("/reports")
def list_reports():
    """List all reports."""
    return {"reports": []}
