"""
test_functions.py
Unit tests for the weather analysis project.
Run with: python -m pytest tests/ -v
"""

import sys
import os
import pandas as pd
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from preprocessing import clean_data, add_time_features, get_season
from analysis import get_summary_statistics, get_monthly_averages, compute_correlation
from forecasting import simple_moving_average, exponential_moving_average, forecast_next_n_days


# ─── Fixtures ────────────────────────────────────────────────────

@pytest.fixture
def sample_df():
    """Create a small sample DataFrame for testing."""
    dates = pd.date_range("2023-01-01", periods=30, freq="D")
    return pd.DataFrame({
        "date": dates,
        "temperature": np.random.uniform(15, 35, 30),
        "humidity": np.random.uniform(40, 90, 30),
        "rainfall": np.random.uniform(0, 10, 30)
    })


# ─── Preprocessing Tests ─────────────────────────────────────────

def test_clean_data_returns_dataframe(sample_df):
    """clean_data should return a DataFrame."""
    result = clean_data(sample_df)
    assert isinstance(result, pd.DataFrame)


def test_clean_data_no_negatives(sample_df):
    """Rainfall should never be negative after cleaning."""
    sample_df.loc[0, "rainfall"] = -5
    result = clean_data(sample_df)
    assert (result["rainfall"] >= 0).all()


def test_clean_data_humidity_range(sample_df):
    """Humidity should be within 0-100 after cleaning."""
    sample_df.loc[0, "humidity"] = 150
    result = clean_data(sample_df)
    assert result["humidity"].max() <= 100


def test_add_time_features_columns(sample_df):
    """add_time_features should add year, month, season columns."""
    df = clean_data(sample_df)
    result = add_time_features(df)
    for col in ["year", "month", "day_of_year", "season", "month_name"]:
        assert col in result.columns, f"Column '{col}' missing"


def test_get_season_mapping():
    """get_season should correctly map months to seasons."""
    assert get_season(1) == "Winter"
    assert get_season(4) == "Summer"
    assert get_season(7) == "Monsoon"
    assert get_season(10) == "Post-Monsoon"


# ─── Analysis Tests ──────────────────────────────────────────────

def test_summary_statistics_shape(sample_df):
    """Summary stats should have 3 columns (numeric ones)."""
    df = clean_data(sample_df)
    stats = get_summary_statistics(df)
    assert stats.shape[1] == 3


def test_correlation_matrix_shape(sample_df):
    """Correlation matrix should be 3x3."""
    df = clean_data(sample_df)
    corr = compute_correlation(df)
    assert corr.shape == (3, 3)


def test_correlation_diagonal_is_one(sample_df):
    """Diagonal of correlation matrix should be 1.0."""
    df = clean_data(sample_df)
    corr = compute_correlation(df)
    for col in ["temperature", "humidity", "rainfall"]:
        assert corr.loc[col, col] == pytest.approx(1.0, abs=0.001)


# ─── Forecasting Tests ───────────────────────────────────────────

def test_sma_length(sample_df):
    """SMA output should have same length as input."""
    result = simple_moving_average(sample_df["temperature"], window=7)
    assert len(result) == len(sample_df)


def test_ema_no_nulls(sample_df):
    """EMA should produce no NaN values."""
    result = exponential_moving_average(sample_df["temperature"], span=7)
    assert result.isnull().sum() == 0


def test_forecast_length(sample_df):
    """forecast_next_n_days should return exactly N rows."""
    df = clean_data(sample_df)
    df = add_time_features(df)
    from forecasting import add_moving_averages
    df = add_moving_averages(df)
    forecast = forecast_next_n_days(df, "temperature", n=7)
    assert len(forecast) == 7


def test_forecast_dates_are_future(sample_df):
    """All forecast dates should be after the last historical date."""
    df = clean_data(sample_df)
    df = add_time_features(df)
    from forecasting import add_moving_averages
    df = add_moving_averages(df)
    forecast = forecast_next_n_days(df, "temperature", n=5)
    assert (forecast["date"] > df["date"].max()).all()
