"""
forecasting.py
Simple weather forecasting using moving averages.
Covers: Simple Moving Average (SMA) and Exponential Moving Average (EMA).
"""

import pandas as pd
import numpy as np


def simple_moving_average(series: pd.Series, window: int = 7) -> pd.Series:
    """
    Compute Simple Moving Average (SMA) for a time series.

    Args:
        series (pd.Series): Numeric time series (e.g., daily temperature).
        window (int): Rolling window size in days. Default is 7 (weekly).

    Returns:
        pd.Series: SMA values aligned with the original series.
    """
    return series.rolling(window=window, min_periods=1).mean().round(2)


def exponential_moving_average(series: pd.Series, span: int = 7) -> pd.Series:
    """
    Compute Exponential Moving Average (EMA) — gives more weight to recent values.

    Args:
        series (pd.Series): Numeric time series.
        span (int): Span for EMA smoothing (analogous to window size).

    Returns:
        pd.Series: EMA values.
    """
    return series.ewm(span=span, adjust=False).mean().round(2)


def forecast_next_n_days(df: pd.DataFrame, column: str, n: int = 7) -> pd.DataFrame:
    """
    Forecast the next N days using the last window's moving average.
    Uses the last 30-day average as the baseline prediction.

    Args:
        df (pd.DataFrame): DataFrame with 'date' and target column.
        column (str): Column name to forecast (e.g., 'temperature').
        n (int): Number of days to forecast.

    Returns:
        pd.DataFrame: DataFrame with forecasted dates and predicted values.
    """
    last_30_avg = df[column].tail(30).mean()
    last_date = df["date"].max()

    forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=n)

    # Add small random variation to make it realistic
    np.random.seed(0)
    variation = np.random.normal(0, df[column].std() * 0.1, n)
    predicted_values = np.round(last_30_avg + variation, 2)

    forecast_df = pd.DataFrame({
        "date": forecast_dates,
        f"predicted_{column}": predicted_values,
        "type": "Forecast"
    })

    print(f"[FORECAST] Next {n} days {column} forecast based on 30-day moving average:")
    print(forecast_df.to_string(index=False))
    return forecast_df


def add_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add SMA and EMA columns for temperature, humidity, and rainfall.

    Args:
        df (pd.DataFrame): Preprocessed weather DataFrame.

    Returns:
        pd.DataFrame: DataFrame with added moving average columns.
    """
    df = df.copy()
    for col in ["temperature", "humidity", "rainfall"]:
        df[f"{col}_sma7"] = simple_moving_average(df[col], window=7)
        df[f"{col}_ema7"] = exponential_moving_average(df[col], span=7)
        df[f"{col}_sma30"] = simple_moving_average(df[col], window=30)
    return df
