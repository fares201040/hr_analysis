"""Data cleaning utilities for HR analysis."""


import warnings
from pathlib import Path

import pandas as pd


class DataCleaner:
    """Class for cleaning HR data."""

    def clean_all_csvs(self) -> None:
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
        for f in csv_files:
            df = pd.read_csv(f, low_memory=False)
            # Clean column names
            df.columns = [col.strip().replace(' ', '_').lower() for col in df.columns]
            # Convert date columns to datetime
            for col in df.columns:
                if any(keyword in col for keyword in ["date", "time", "day"]):
                    def try_parse(val):
                        for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%d-%m-%Y", "%m-%d-%Y", "%Y.%m.%d"]:
                            try:
                                return pd.to_datetime(val, format=fmt)
                            except Exception:
                                continue
                        try:
                            return pd.to_datetime(val)
                        except Exception:
                            return val
                    df[col] = df[col].apply(try_parse)
            # Create unique column and set as index
            if "employee_id" in df.columns and "date" in df.columns:
                df["employee_date_id"] = df["employee_id"].astype(str) + "_" + df["date"].astype(str)
                df.set_index("employee_date_id", inplace=True)
            clean_dir = base_dir / "clean_data"
            clean_dir.mkdir(exist_ok=True)
            cleaned_path = clean_dir / "cleaned.csv"
            df.to_csv(cleaned_path)


if __name__ == "__main__":
    cleaner = DataCleaner()
    cleaner.clean_all_csvs()
