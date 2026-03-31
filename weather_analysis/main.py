"""
main.py
Entry point for the Weather Data Analysis and Prediction project.
Run this file to execute the full pipeline.

Usage:
    python main.py

Output:
    - Charts saved in results/ folder
    - Summary statistics printed to console
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from data_loader import load_csv_data
from preprocessing import clean_data, add_time_features
from analysis import (
    get_summary_statistics,
    get_monthly_averages,
    get_seasonal_averages,
    get_yearly_trend,
    compute_correlation
)
from forecasting import add_moving_averages, forecast_next_n_days
from visualization import (
    plot_temperature_trend,
    plot_monthly_averages,
    plot_seasonal_patterns,
    plot_correlation_heatmap,
    plot_forecast,
    plot_dashboard
)


def main():
    """Main pipeline: load → clean → analyze → visualize → forecast."""
    print("=" * 60)
    print("   WEATHER DATA ANALYSIS AND PREDICTION")
    print("=" * 60)

    # ── STEP 1: Load Data ──────────────────────────────────────────
    print("\n[STEP 1] Loading data...")
    df = load_csv_data("data/weather_data.csv")

    # ── STEP 2: Clean & Preprocess ────────────────────────────────
    print("\n[STEP 2] Cleaning and preprocessing...")
    df = clean_data(df)
    df = add_time_features(df)

    # ── STEP 3: Statistical Analysis ─────────────────────────────
    print("\n[STEP 3] Running statistical analysis...")
    summary_stats = get_summary_statistics(df)
    monthly_df = get_monthly_averages(df)
    seasonal_df = get_seasonal_averages(df)
    yearly_df = get_yearly_trend(df)
    correlation = compute_correlation(df)

    print("\nMonthly Averages:")
    print(monthly_df.to_string(index=False))

    print("\nSeasonal Averages:")
    print(seasonal_df.to_string(index=False))

    # ── STEP 4: Forecasting ───────────────────────────────────────
    print("\n[STEP 4] Computing moving averages and forecast...")
    df = add_moving_averages(df)
    temp_forecast = forecast_next_n_days(df, "temperature", n=7)
    humidity_forecast = forecast_next_n_days(df, "humidity", n=7)

    # ── STEP 5: Visualization ─────────────────────────────────────
    print("\n[STEP 5] Generating visualizations...")
    plot_temperature_trend(df)
    plot_monthly_averages(monthly_df)
    plot_seasonal_patterns(df)
    plot_correlation_heatmap(df)
    plot_forecast(df, temp_forecast, column="temperature")
    plot_forecast(df, humidity_forecast, column="humidity")
    plot_dashboard(df, monthly_df)

    print("\n" + "=" * 60)
    print("   ANALYSIS COMPLETE")
    print("   Charts saved in: results/ folder")
    print("=" * 60)


if __name__ == "__main__":
    main()
