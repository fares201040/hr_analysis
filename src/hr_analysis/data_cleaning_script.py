"""
HR Data Cleaning Script
Standardizes date formats, converts numerics, fills missing values, and drops empty columns.
Follows project architecture and coding standards.
"""

from pathlib import Path

import pandas as pd


def clean_hr_csv(input_path: str, output_path: str) -> None:
    """
    Cleans HR CSV data: standardizes dates, converts numerics, fills missing, drops empty columns.
    Args:
        input_path (str): Path to input CSV file.
        output_path (str): Path to save cleaned CSV file.
    """
    # Load data
    df = pd.read_csv(input_path)

    # Date columns to standardize
    date_cols = [
        "Date",
        "Schedule_From_Date",
        "Schedule_To_Date",
        "Actual_From_Date",
        "Actual_To_Date",
        "From_Date",
        "To_Date",
        "Pre_OT_Start_Time",
        "Pre_OT_End_Time",
        "Post_OT_Start_Time",
        "Post_OT_End_Time",
        "last_Updated_date",
    ]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Numeric columns to convert
    numeric_cols = [
        "Total_Worked_Hrs",
        "Lateness_Hrs",
        "Early_Out_Hrs",
        "Overbreak_Hrs",
        "Regular_Units",
        "pre_ot_hrs",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Categorical columns to fill
    cat_cols = ["Day_Type", "Holiday_Type", "Shift", "Leave_Type", "Exception"]
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    # Drop columns with all missing values
    df = df.dropna(axis=1, how="all")

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Save cleaned data
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    # Example usage
    input_csv = (
        "src/unclean_data/A11017__48151122_d1f3568c-5c8e-446c-bab2-757676ef5e9f.csv"
    )
    output_csv = "src/clean_data/cleaned.csv"
    clean_hr_csv(input_csv, output_csv)
