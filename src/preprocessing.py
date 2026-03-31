"""
preprocessing.py
Handles data cleaning, missing value treatment, and time-series feature extraction.
"""

import pandas as pd
import numpy as np


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean weather DataFrame: handle missing values, remove outliers,
    and ensure correct data types.

    Args:
        df (pd.DataFrame): Raw weather DataFrame.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    df = df.copy()

    # Ensure date column is datetime
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)
    df = df.sort_values("date").reset_index(drop=True)

    # Report missing values
    missing_count = df.isnull().sum()
    if missing_count.any():
        print(f"[INFO] Missing values found:\n{missing_count[missing_count > 0]}")
        # Fill numeric columns with forward fill, then mean
        numeric_cols = ["temperature", "humidity", "rainfall"]
        df[numeric_cols] = df[numeric_cols].fillna(method="ffill").fillna(df[numeric_cols].mean())

    # Remove temperature outliers (outside 3 standard deviations)
    temp_mean = df["temperature"].mean()
    temp_std = df["temperature"].std()
    outliers = ((df["temperature"] < temp_mean - 3 * temp_std) |
                (df["temperature"] > temp_mean + 3 * temp_std))
    if outliers.sum() > 0:
        print(f"[INFO] Removed {outliers.sum()} temperature outliers")
        df = df[~outliers]

    # Clip humidity to valid range
    df["humidity"] = df["humidity"].clip(0, 100)

    # Clip rainfall to non-negative
    df["rainfall"] = df["rainfall"].clip(lower=0)

    print(f"[INFO] Cleaned data: {len(df)} records remaining")
    return df.reset_index(drop=True)


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract time-based features from the date column for analysis.

    Args:
        df (pd.DataFrame): Cleaned DataFrame with 'date' column.

    Returns:
        pd.DataFrame: DataFrame with added time feature columns.
    """
    df = df.copy()
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day_of_year"] = df["date"].dt.dayofyear
    df["season"] = df["month"].map(get_season)
    df["month_name"] = df["date"].dt.strftime("%b")
    return df


def get_season(month: int) -> str:
    """
    Map a month number to an Indian meteorological season.

    Args:
        month (int): Month number (1-12).

    Returns:
        str: Season name.
    """
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Summer"
    elif month in [6, 7, 8, 9]:
        return "Monsoon"
    else:
        return "Post-Monsoon"
