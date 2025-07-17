"""Data cleaning utilities for HR analysis."""


import warnings
from pathlib import Path

import pandas as pd



def clean_all_csvs() -> None:
    """
    Cleans all CSV files in unclean_data:
    - Strips leading/trailing spaces from column names
    - Converts column names to lowercase and replaces spaces with underscores
    - Uniforms columns with date values to pandas datetime format
    - Saves cleaned files with '_cleaned' suffix in unclean_data
    """
    base_dir = Path(__file__).parent.parent
    unclean_dir = base_dir / "unclean_data"
    csv_files = list(unclean_dir.glob("*.csv"))
    cleaned_dfs = []
    for f in csv_files:
        df = pd.read_csv(f, low_memory=False)
        # Normalize column names (expand variants)
        col_map = {}
        for col in df.columns:
            norm = col.strip().replace(' ', '_').replace('__', '_').lower()
            # Map possible employee_id columns
            if norm in ["employee_id", "employeeid", "employee", "id", "emp_code", "emp_id", "empid"]:
                col_map[col] = "employee_id"
            elif norm in ["date", "date_", "day", "date_of_attendance", "attendance_date", "date "]:
                col_map[col] = "date"
            else:
                col_map[col] = norm
        df.rename(columns=col_map, inplace=True)
        # Strip spaces from all string values in all columns
        for col in df.columns:
            df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
        # Convert date columns to datetime (add more formats)
        if "date" in df.columns:
            import warnings
            def try_parse(val):
                for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%d-%m-%Y", "%m-%d-%Y", "%Y.%m.%d", "%b %d %Y", "%b  %d %Y", "%b %d %Y "]:
                    try:
                        return pd.to_datetime(val, format=fmt)
                    except Exception:
                        continue
                try:
                    with warnings.catch_warnings():
                        warnings.filterwarnings("ignore", category=UserWarning, module="pandas")
                        return pd.to_datetime(val)
                except Exception:
                    return val
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UserWarning, module="pandas")
                df["date"] = df["date"].apply(try_parse)
        cleaned_dfs.append(df)
    # Create unique column for each DataFrame
    for i, df in enumerate(cleaned_dfs):
        if "employee_id" in df.columns and "date" in df.columns:
            df["employee_date_id"] = df["employee_id"].astype(str) + "_" + df["date"].astype(str)
        else:
            df["employee_date_id"] = df.index.map(lambda x: f"unidentified_{i}_{str(x)}")
    # Concatenate all cleaned DataFrames
    merged_df = pd.concat(cleaned_dfs, axis=0, ignore_index=True)
    # Remove duplicate columns by name
    merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]
    # Remove duplicate rows by 'employee_date_id'
    if "employee_date_id" in merged_df.columns:
        merged_df.drop_duplicates(subset=["employee_date_id"], inplace=True)
        merged_df.set_index("employee_date_id", inplace=True)
    # Remove duplicate columns by name
    merged_df = merged_df.loc[:,~merged_df.columns.duplicated()]
    # Remove duplicate columns by content
    def drop_duplicate_content(df, exclude=None):
        if exclude is None:
            exclude = []
        cols = [c for c in df.columns if c not in exclude]
        to_drop = set()
        for i in range(len(cols)):
            for j in range(i+1, len(cols)):
                if df[cols[i]].equals(df[cols[j]]):
                    to_drop.add(cols[j])
        return df.drop(columns=list(to_drop))
    merged_df = drop_duplicate_content(merged_df, exclude=["employee_date_id"])
    # Robustly handle duplicate columns and types for employee_id and date
    for col_base in ["employee_id", "date"]:
        cols = [c for c in merged_df.columns if c.startswith(col_base)]
        if len(cols) > 1:
            # Prefer non-null values, then drop others
            merged_df[col_base] = merged_df[cols].bfill(axis=1).iloc[:, 0]
            merged_df.drop(columns=[c for c in cols if c != col_base], inplace=True)
    # Ensure employee_id and date are string type and not DataFrame
    for col_base in ["employee_id", "date"]:
        if col_base in merged_df.columns:
            col = merged_df[col_base]
            if isinstance(col, pd.DataFrame):
                merged_df[col_base] = col.iloc[:, 0].astype(str)
            else:
                merged_df[col_base] = col.astype(str)
    # Create unique column and set as index
    if "employee_id" in merged_df.columns and "date" in merged_df.columns:
        merged_df["employee_date_id"] = merged_df["employee_id"].astype(str) + "_" + merged_df["date"].astype(str)
        merged_df.set_index("employee_date_id", inplace=True)
    clean_dir = base_dir / "clean_data"
    clean_dir.mkdir(exist_ok=True)
    cleaned_path = clean_dir / "cleaned.csv"
    merged_df.to_csv(cleaned_path)
    print(f"Cleaned file saved successfully to: {cleaned_path}")


if __name__ == "__main__":
    clean_all_csvs()
