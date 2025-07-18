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
    Union,
)


import pandas as pd
from fastapi import (
    APIRouter,
    Body,
    Query,
)

# Use project-level cleaned DataFrame loader
from src.hr_analysis.data_cleaner import get_cleaned_df




# Initialize FastAPI router
router = APIRouter()


# --- Report Endpoints ---

# Report 23: Department List Report — see report_details.md
@router.get("/reports/departments", response_model=Dict[str, List[str]])
def department_list_report() -> Dict[str, List[str]]:
    """
    Returns a list of all departments found in the cleaned data file.
    """
    df = get_cleaned_df()
    if "department" in df.columns:
        departments = sorted(df["department"].dropna().unique())
    else:
        departments = []
    return {"departments": departments}


# Report 22: Employee List Report — see report_details.md
@router.get("/reports/employees", response_model=Dict[str, List[str]])
def employee_list_report() -> Dict[str, List[str]]:
    """
    Returns a list of all employee IDs found in the cleaned data file.
    """
    df = get_cleaned_df()
    if "employee_id" in df.columns:
        employees = sorted(df["employee_id"].dropna().unique())
    else:
        employees = []
    return {"employees": employees}

## Report 20: Monthly Overtime Comparison — see report_details.md
@router.get("/reports/overtime-month-comparison", response_model=Dict[str, Any])
def overtime_month_comparison(
    department: Optional[str] = Query(None, description="Filter by department"),
    employee_id: Optional[str] = Query(None, description="Filter by employee ID"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
) -> Dict[str, Any]:
    """
    Compares overtime hours across months for departments or employees.
    Filters: department, employee_id, start_date, end_date.
    """
    df = get_cleaned_df()
    # Standardize date column
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # Filter by date range
    if start_date:
        df = df[df["date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["date"] <= pd.to_datetime(end_date)]
    # Filter by department
    if department and "department" in df.columns:
        df = df[df["department"].str.lower() == department.lower()]
    # Filter by employee_id
    if employee_id:
        df = df[df["employee_id"] == employee_id]
    # Only consider rows with overtime
    if "total_ot" in df.columns:
        df = df[df["total_ot"].fillna(0) > 0]
    # Add month column
    df["month"] = df["date"].dt.strftime("%Y-%m")
    # Group by month, sum total_ot
    if "total_ot" in df.columns:
        summary = (
            df.groupby(["month"])["total_ot"].sum().reset_index()
        )
    else:
        summary = df.groupby(["month"]).size().reset_index(name="total_overtime_hours")
    # Build response
    result = []
    for _, row in summary.iterrows():
        result.append({
            "month": row["month"],
            "total_overtime_hours": float(row["total_ot"]) if "total_ot" in row else int(row["total_overtime_hours"])
        })
    return {"monthly_overtime_comparison": result}

## Report 2: All Employee Attendance Report (No Filtering) — see report_details.md
@router.get("/reports/attendance/all", response_model=Dict[str, List[Dict[str, Any]]])
def all_attendance_report() -> Dict[str, List[Dict[str, Any]]]:
    """
    Get all Employee Attendance records (no filtering).

    Returns all attendance records from cleaned.csv.

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
    df = get_cleaned_df()
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")
    columns = ["employee_id", "date", "department", "day_type", "exception"]
    attendance = df[columns].fillna("").to_dict(orient="records")
    return {"attendance": attendance}

## Report 1: Employee Attendance Report (Filtered) — see report_details.md
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
    df = get_cleaned_df()

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


## Report 15: Overtime Trends Over Time — see report_details.md
@router.get("/reports/overtime-trends", response_model=Dict[str, Any])
def overtime_trends(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    department: Optional[str] = Query(None, description="Filter by department"),
    employee_id: Optional[str] = Query(None, description="Filter by employee ID"),
    granularity: Optional[str] = Query("daily", description="Time granularity: daily, weekly, monthly")
) -> Dict[str, Any]:
    """
    Shows overtime hours trends (daily, weekly, monthly) for employees or departments.
    Filters: department, employee_id, time granularity, date range.
    """
    df = get_cleaned_df()
    # Standardize date column
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # Filter by date range
    if start_date:
        df = df[df["date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["date"] <= pd.to_datetime(end_date)]
    # Filter by department
    if department and "department" in df.columns:
        df = df[df["department"].str.lower() == department.lower()]
    # Filter by employee_id
    if employee_id:
        df = df[df["employee_id"] == employee_id]
    # Only consider rows with overtime
    if "total_ot" in df.columns:
        df = df[df["total_ot"].fillna(0) > 0]
    # Group by granularity
    if granularity == "monthly":
        df["period"] = df["date"].dt.strftime("%Y-%m")
    elif granularity == "weekly":
        df["period"] = df["date"].dt.strftime("%Y-W%V")
    else:
        df["period"] = df["date"].dt.strftime("%Y-%m-%d")
    group_cols = ["period"]
    if department:
        group_cols.append("department")
    if employee_id:
        group_cols.append("employee_id")
    summary = df.groupby(group_cols)["total_ot"].sum().reset_index()
    # Build response
    result = []
    for _, row in summary.iterrows():
        entry = {
            "date": row["period"],
            "total_overtime_hours": float(row["total_ot"])
        }
        if "department" in row:
            entry["department"] = row["department"]
        if "employee_id" in row:
            entry["employee_id"] = row["employee_id"]
        result.append(entry)
    return {"overtime_trends": result}


## Report 16: Top Overtime Employees — see report_details.md
@router.get("/reports/top-overtime-employees", response_model=Dict[str, Any])
def top_overtime_employees(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    department: Optional[str] = Query(None, description="Filter by department"),
    top_n: Optional[int] = Query(10, description="Limit results to top N records")
) -> Dict[str, Any]:
    """
    Lists employees with the highest overtime hours in a given period.
    Filters: department, date range, top N.
    """
    df = get_cleaned_df()
    # Standardize date column
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # Filter by date range
    if start_date:
        df = df[df["date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["date"] <= pd.to_datetime(end_date)]
    # Filter by department
    if department and "department" in df.columns:
        df = df[df["department"].str.lower() == department.lower()]
    # Only consider rows with overtime
    if "total_ot" in df.columns:
        df = df[df["total_ot"].fillna(0) > 0]
    # Group by employee, sum total_ot
    if "total_ot" in df.columns:
        summary = (
            df.groupby(["employee_id", "department"])["total_ot"].sum().reset_index()
        )
    else:
        summary = df.groupby(["employee_id", "department"]).size().reset_index(name="total_overtime_hours")
    # Sort and limit to top N
    summary = summary.sort_values(by="total_ot" if "total_ot" in summary.columns else "total_overtime_hours", ascending=False)
    summary = summary.head(top_n)
    # Build response
    result = []
    for _, row in summary.iterrows():
        result.append({
            "employee_id": row["employee_id"],
            "department": row["department"],
            "total_overtime_hours": float(row["total_ot"]) if "total_ot" in row else int(row["total_overtime_hours"])
        })
    return {"top_overtime_employees": result}

## Report 17: Overtime Exception Report — see report_details.md
@router.get("/reports/overtime-exceptions", response_model=Dict[str, Any])
def overtime_exceptions(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    department: Optional[str] = Query(None, description="Filter by department"),
    threshold_hours: Optional[float] = Query(None, description="Threshold hours for exception")
) -> Dict[str, Any]:
    """
    Identifies overtime entries that exceed policy limits or require approval.
    Filters: department, date range, threshold hours.
    """
    df = get_cleaned_df()
    # Standardize date column
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # Filter by date range
    if start_date:
        df = df[df["date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["date"] <= pd.to_datetime(end_date)]
    # Filter by department
    if department and "department" in df.columns:
        df = df[df["department"].str.lower() == department.lower()]
    # Only consider rows with overtime
    if "total_ot" in df.columns:
        df = df[df["total_ot"].fillna(0) > 0]
    # Apply threshold filter
    if threshold_hours is not None and "total_ot" in df.columns:
        df = df[df["total_ot"] > threshold_hours]
    # Build response
    result = []
    for _, row in df.iterrows():
        result.append({
            "employee_id": row["employee_id"],
            "department": row["department"] if "department" in row else None,
            "date": row["date"].strftime("%Y-%m-%d") if hasattr(row["date"], "strftime") else str(row["date"]),
            "overtime_hours": float(row["total_ot"]) if "total_ot" in row else None,
            "exception_reason": "Exceeded daily limit" if threshold_hours is not None and row["total_ot"] > threshold_hours else "Requires approval"
        })
    return {"overtime_exceptions": result}
def top_overtime_employees(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    department: Optional[str] = Query(None, description="Filter by department"),
    top_n: Optional[int] = Query(10, description="Limit results to top N records")
) -> Dict[str, Any]:
    """
    Lists employees with the highest overtime hours in a given period.
    Filters: department, date range, top N.
    """
    df = get_cleaned_df()
    # Standardize date column
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # Filter by date range
    if start_date:
        df = df[df["date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["date"] <= pd.to_datetime(end_date)]
    # Filter by department
    if department and "department" in df.columns:
        df = df[df["department"].str.lower() == department.lower()]
    # Only consider rows with overtime
    if "total_ot" in df.columns:
        df = df[df["total_ot"].fillna(0) > 0]
    # Group by employee, sum total_ot
    if "total_ot" in df.columns:
        summary = (
            df.groupby(["employee_id", "department"])["total_ot"].sum().reset_index()
        )
    else:
        summary = df.groupby(["employee_id", "department"]).size().reset_index(name="total_overtime_hours")
    # Sort and limit to top N
    summary = summary.sort_values(by="total_ot" if "total_ot" in summary.columns else "total_overtime_hours", ascending=False)
    summary = summary.head(top_n)
    # Build response
    result = []
    for _, row in summary.iterrows():
        result.append({
            "employee_id": row["employee_id"],
            "department": row["department"],
            "total_overtime_hours": float(row["total_ot"]) if "total_ot" in row else int(row["total_overtime_hours"])
        })
    return {"top_overtime_employees": result}
def overtime_trends(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    department: Optional[str] = Query(None, description="Filter by department"),
    employee_id: Optional[str] = Query(None, description="Filter by employee ID"),
    granularity: Optional[str] = Query("daily", description="Time granularity: daily, weekly, monthly")
) -> Dict[str, Any]:
    """
    Shows overtime hours trends (daily, weekly, monthly) for employees or departments.
    Filters: department, employee_id, time granularity, date range.
    """
    df = get_cleaned_df()
    # Standardize date column
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # Filter by date range
    if start_date:
        df = df[df["date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["date"] <= pd.to_datetime(end_date)]
    # Filter by department
    if department and "department" in df.columns:
        df = df[df["department"].str.lower() == department.lower()]
    # Filter by employee_id
    if employee_id:
        df = df[df["employee_id"] == employee_id]
    # Only consider rows with overtime
    if "total_ot" in df.columns:
        df = df[df["total_ot"].fillna(0) > 0]
    # Group by granularity
    if granularity == "monthly":
        df["period"] = df["date"].dt.strftime("%Y-%m")
    elif granularity == "weekly":
        df["period"] = df["date"].dt.strftime("%Y-W%V")
    else:
        df["period"] = df["date"].dt.strftime("%Y-%m-%d")
    group_cols = ["period"]
    if department:
        group_cols.append("department")
    if employee_id:
        group_cols.append("employee_id")
    summary = df.groupby(group_cols)["total_ot"].sum().reset_index()
    # Build response
    result = []
    for _, row in summary.iterrows():
        entry = {
            "date": row["period"],
            "total_overtime_hours": float(row["total_ot"])
        }
        if "department" in row:
            entry["department"] = row["department"]
        if "employee_id" in row:
            entry["employee_id"] = row["employee_id"]
        result.append(entry)
    return {"overtime_trends": result}
## Report 14: Department Overtime Summary — see report_details.md
@router.get("/reports/department-overtime", response_model=Dict[str, Any])
def department_overtime(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
) -> Dict[str, Any]:
    """
    Aggregates total overtime hours by department for a selected period.
    Filters: date range.
    """
    df = get_cleaned_df()
    # Standardize date column
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # Filter by date range
    if start_date:
        df = df[df["date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["date"] <= pd.to_datetime(end_date)]
    # Group by department, sum total_ot
    if "total_ot" in df.columns:
        summary = (
            df.groupby(["department"])["total_ot"].sum().reset_index()
        )
    else:
        summary = df.groupby(["department"]).size().reset_index(name="total_overtime_hours")
    # Build response
    result = []
    for _, row in summary.iterrows():
        result.append({
            "department": row["department"],
            "total_overtime_hours": float(row["total_ot"]) if "total_ot" in row else int(row["total_overtime_hours"])
        })
    return {"department_overtime": result}
## Report 13: Employee Overtime Summary — see report_details.md
def overtime_summary(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    department: Optional[str] = Query(None, description="Filter by department")
) -> Dict[str, Any]:
    """
    Summarizes total overtime hours per employee for a given period.
    Filters: department, date range.
    """
    df = get_cleaned_df()
    # Standardize date column
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # Filter by date range
    if start_date:
        df = df[df["date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["date"] <= pd.to_datetime(end_date)]
    # Filter by department
    if department and "department" in df.columns:
        df = df[df["department"].str.lower() == department.lower()]
    # Group by employee, sum total_ot
    if "total_ot" in df.columns:
        summary = (
            df.groupby(["employee_id", "department"])["total_ot"].sum().reset_index()
        )
    else:
        summary = df.groupby(["employee_id", "department"]).size().reset_index(name="total_overtime_hours")
    # Build response
    result = []
    for _, row in summary.iterrows():
        result.append({
            "employee_id": row["employee_id"],
            "department": row["department"],
            "total_overtime_hours": float(row["total_ot"]) if "total_ot" in row else int(row["total_overtime_hours"])
        })
    return {"overtime_summary": result}

# --- Report 21: Employee Overtime Days Per Week ---
## Report 21: Employee Overtime Days Per Week — see report_details.md
@router.get("/reports/overtime-weekly-summary", response_model=Dict[str, Any])
def overtime_weekly_summary(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    department: Optional[str] = Query(None, description="Filter by department"),
    employee_ids: Optional[List[str]] = Query(None, description="Filter by employee IDs (comma separated)"),
    week_start: str = Query("sunday", description="Start day of week: 'sunday' or 'monday' (default: sunday)")
) -> Dict[str, Any]:
    """
    For each employee, shows how many days they worked overtime in each week.
    You can select the week start day: Sunday (default) or Monday (ISO week).
    - If week_start='sunday', weeks start on Sunday and end on Saturday.
    - If week_start='monday', weeks start on Monday and end on Sunday (ISO week).
    Columns are week labels (YYYY-Www), rows are employees, each cell is count of overtime days for that employee in that week.
    """
    import numpy as np
    df = get_cleaned_df()
    # Standardize date column
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # Filter by date range
    if start_date:
        df = df[df["date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["date"] <= pd.to_datetime(end_date)]
    # Filter by department
    if department and "department" in df.columns:
        df = df[df["department"].str.lower() == department.lower()]
    # Filter by employee_ids
    if employee_ids:
        df = df[df["employee_id"].isin(employee_ids)]
    # Only consider days with overtime (total_ot > 0)
    if "total_ot" in df.columns:
        df = df[df["total_ot"].fillna(0) > 0]
    # Week calculation
    if week_start.lower() == "monday":
        # ISO week: Monday-Sunday
        df["week_label"] = df["date"].dt.strftime("%Y-W%V")
    else:
        # Custom week: Sunday-Saturday
        # Shift dates so that week starts on Sunday
        # pandas weekday: Monday=0, Sunday=6
        df["week_start"] = df["date"] - pd.to_timedelta((df["date"].dt.weekday + 1) % 7, unit="D")
        df["week_label"] = df["week_start"].dt.strftime("%Y-W%U")
    # Group by employee and week, count overtime days
    summary = (
        df.groupby(["employee_id", "week_label"]).size().reset_index(name="overtime_days")
    )
    # Pivot to wide format: rows=employee, columns=week
    pivot = summary.pivot(index="employee_id", columns="week_label", values="overtime_days").fillna(0).astype(int)
    # Build response
    result = []
    for emp_id, row in pivot.iterrows():
        weeks = {week: int(row[week]) for week in pivot.columns}
        result.append({"employee_id": emp_id, "weeks": weeks})
    columns = ["employee_id"] + list(pivot.columns)
    return {"overtime_weekly_summary": result, "columns": columns}

## Report 18: Department Overtime Comparison — see report_details.md
@router.get("/reports/overtime-department-comparison", response_model=Dict[str, Any])
def overtime_department_comparison(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
) -> Dict[str, Any]:
    """
    Compares overtime hours across departments for a selected period.
    Filters: start_date, end_date.
    """
    df = get_cleaned_df()
    # Standardize date column
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # Filter by date range
    if start_date:
        df = df[df["date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["date"] <= pd.to_datetime(end_date)]
    # Group by department, sum total_ot
    if "total_ot" in df.columns:
        summary = (
            df.groupby(["department"])["total_ot"].sum().reset_index()
        )
    else:
        summary = df.groupby(["department"]).size().reset_index(name="total_overtime_hours")
    # Build response
    result = []
    for _, row in summary.iterrows():
        result.append({
            "department": row["department"],
            "total_overtime_hours": float(row["total_ot"]) if "total_ot" in row else int(row["total_overtime_hours"])
        })
    return {"department_overtime_comparison": result}

## Report 19: Employee Overtime Comparison — see report_details.md
@router.get("/reports/overtime-employee-comparison", response_model=Dict[str, Any])
def overtime_employee_comparison(
    employee_ids: Optional[List[str]] = Query(None, description="Filter by employee IDs (comma separated)"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
) -> Dict[str, Any]:
    """
    Compares overtime hours between selected employees for a given period.
    Filters: employee_ids, start_date, end_date.
    """
    df = get_cleaned_df()
    # Standardize date column
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # Filter by date range
    if start_date:
        df = df[df["date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["date"] <= pd.to_datetime(end_date)]
    # Filter by employee_ids
    if employee_ids:
        df = df[df["employee_id"].isin(employee_ids)]
    # Group by employee, sum total_ot
    if "total_ot" in df.columns:
        summary = (
            df.groupby(["employee_id"])["total_ot"].sum().reset_index()
        )
    else:
        summary = df.groupby(["employee_id"]).size().reset_index(name="total_overtime_hours")
    # Build response
    result = []
    for _, row in summary.iterrows():
        result.append({
            "employee_id": row["employee_id"],
            "total_overtime_hours": float(row["total_ot"]) if "total_ot" in row else int(row["total_overtime_hours"])
        })
    return {"employee_overtime_comparison": result}

## Report 3: List Reports — see report_details.md
@router.get("/reports")
def list_reports():
    """List all reports."""
    df = get_cleaned_df()
    return {"reports": []}
