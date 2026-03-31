"""
analysis.py
Performs statistical analysis and trend identification on weather data.
"""

import pandas as pd
import numpy as np


def get_summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute descriptive statistics for numeric weather columns.

    Args:
        df (pd.DataFrame): Preprocessed weather DataFrame.

    Returns:
        pd.DataFrame: Summary statistics table.
    """
    numeric_cols = ["temperature", "humidity", "rainfall"]
    stats = df[numeric_cols].describe().round(2)
    print("\n[STATS] Summary Statistics:")
    print(stats)
    return stats


def get_monthly_averages(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate average temperature, humidity, and rainfall per month.

    Args:
        df (pd.DataFrame): DataFrame with 'month' and 'month_name' columns.

    Returns:
        pd.DataFrame: Monthly averages sorted by month number.
    """
    monthly = df.groupby(["month", "month_name"]).agg(
        avg_temperature=("temperature", "mean"),
        avg_humidity=("humidity", "mean"),
        total_rainfall=("rainfall", "sum"),
        rainy_days=("rainfall", lambda x: (x > 0).sum())
    ).reset_index().sort_values("month")
    monthly = monthly.round(2)
    return monthly


def get_seasonal_averages(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate average metrics grouped by meteorological season.

    Args:
        df (pd.DataFrame): DataFrame with 'season' column.

    Returns:
        pd.DataFrame: Seasonal summary statistics.
    """
    seasonal = df.groupby("season").agg(
        avg_temperature=("temperature", "mean"),
        avg_humidity=("humidity", "mean"),
        total_rainfall=("rainfall", "sum"),
        days=("date", "count")
    ).reset_index().round(2)
    return seasonal


def get_yearly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identify year-over-year trends in temperature and rainfall.

    Args:
        df (pd.DataFrame): DataFrame with 'year' column.

    Returns:
        pd.DataFrame: Yearly aggregated statistics.
    """
    yearly = df.groupby("year").agg(
        avg_temperature=("temperature", "mean"),
        max_temperature=("temperature", "max"),
        min_temperature=("temperature", "min"),
        total_rainfall=("rainfall", "sum"),
        avg_humidity=("humidity", "mean")
    ).reset_index().round(2)
    return yearly


def compute_correlation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute Pearson correlation matrix for numeric weather variables.

    Args:
        df (pd.DataFrame): Preprocessed weather DataFrame.

    Returns:
        pd.DataFrame: Correlation matrix.
    """
    corr = df[["temperature", "humidity", "rainfall"]].corr().round(3)
    print("\n[STATS] Correlation Matrix:")
    print(corr)
    return corr
