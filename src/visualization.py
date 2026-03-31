"""
visualization.py
Creates all plots and the interactive dashboard using Matplotlib and Seaborn.
Saves all figures to the results/ folder.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

# Output folder for saving charts
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Set global style
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.dpi"] = 100


def plot_temperature_trend(df: pd.DataFrame) -> None:
    """
    Plot daily temperature with 7-day and 30-day moving averages.

    Args:
        df (pd.DataFrame): DataFrame with temperature SMA columns.
    """
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(df["date"], df["temperature"], alpha=0.3, color="steelblue", label="Daily Temp")
    ax.plot(df["date"], df["temperature_sma7"], color="orange", linewidth=1.5, label="7-Day SMA")
    ax.plot(df["date"], df["temperature_sma30"], color="red", linewidth=2, label="30-Day SMA")
    ax.set_title("Temperature Trend with Moving Averages", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/temperature_trend.png")
    plt.close()
    print("[PLOT] Saved: temperature_trend.png")


def plot_monthly_averages(monthly_df: pd.DataFrame) -> None:
    """
    Bar chart of average monthly temperature and total rainfall.

    Args:
        monthly_df (pd.DataFrame): Output from analysis.get_monthly_averages().
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Temperature
    sns.barplot(data=monthly_df, x="month_name", y="avg_temperature", ax=ax1,
                palette="coolwarm", order=monthly_df.sort_values("month")["month_name"])
    ax1.set_title("Average Monthly Temperature", fontweight="bold")
    ax1.set_ylabel("Temperature (°C)")
    ax1.set_xlabel("")

    # Rainfall
    sns.barplot(data=monthly_df, x="month_name", y="total_rainfall", ax=ax2,
                palette="Blues_d", order=monthly_df.sort_values("month")["month_name"])
    ax2.set_title("Total Monthly Rainfall", fontweight="bold")
    ax2.set_ylabel("Rainfall (mm)")
    ax2.set_xlabel("Month")

    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/monthly_averages.png")
    plt.close()
    print("[PLOT] Saved: monthly_averages.png")


def plot_seasonal_patterns(df: pd.DataFrame) -> None:
    """
    Boxplot of temperature and humidity grouped by season.

    Args:
        df (pd.DataFrame): DataFrame with 'season' column.
    """
    season_order = ["Winter", "Summer", "Monsoon", "Post-Monsoon"]
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    sns.boxplot(data=df, x="season", y="temperature", order=season_order,
                palette="Set2", ax=axes[0])
    axes[0].set_title("Temperature by Season", fontweight="bold")
    axes[0].set_ylabel("Temperature (°C)")

    sns.boxplot(data=df, x="season", y="humidity", order=season_order,
                palette="Set3", ax=axes[1])
    axes[1].set_title("Humidity by Season", fontweight="bold")
    axes[1].set_ylabel("Humidity (%)")

    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/seasonal_patterns.png")
    plt.close()
    print("[PLOT] Saved: seasonal_patterns.png")


def plot_correlation_heatmap(df: pd.DataFrame) -> None:
    """
    Heatmap of correlation between temperature, humidity, and rainfall.

    Args:
        df (pd.DataFrame): Preprocessed weather DataFrame.
    """
    fig, ax = plt.subplots(figsize=(7, 5))
    corr = df[["temperature", "humidity", "rainfall"]].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
                linewidths=0.5, ax=ax, square=True)
    ax.set_title("Correlation Heatmap", fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/correlation_heatmap.png")
    plt.close()
    print("[PLOT] Saved: correlation_heatmap.png")


def plot_forecast(df: pd.DataFrame, forecast_df: pd.DataFrame, column: str = "temperature") -> None:
    """
    Plot historical data with future forecast.

    Args:
        df (pd.DataFrame): Historical weather DataFrame.
        forecast_df (pd.DataFrame): Output from forecasting.forecast_next_n_days().
        column (str): Column to plot ('temperature', 'humidity', or 'rainfall').
    """
    fig, ax = plt.subplots(figsize=(14, 5))

    # Last 60 days of historical data
    recent = df.tail(60)
    ax.plot(recent["date"], recent[column], label="Historical", color="steelblue")
    ax.plot(recent["date"], recent[f"{column}_sma7"], label="7-Day SMA",
            color="orange", linestyle="--")

    # Forecast
    pred_col = f"predicted_{column}"
    ax.plot(forecast_df["date"], forecast_df[pred_col], label="Forecast",
            color="red", marker="o", linestyle="--")

    ax.axvline(x=df["date"].max(), color="gray", linestyle=":", label="Forecast Start")
    ax.set_title(f"{column.capitalize()} Forecast (Next 7 Days)", fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel(column.capitalize())
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/{column}_forecast.png")
    plt.close()
    print(f"[PLOT] Saved: {column}_forecast.png")


def plot_dashboard(df: pd.DataFrame, monthly_df: pd.DataFrame) -> None:
    """
    Create a summary dashboard combining key visualizations.

    Args:
        df (pd.DataFrame): Full preprocessed DataFrame with MA columns.
        monthly_df (pd.DataFrame): Monthly averages DataFrame.
    """
    fig = plt.figure(figsize=(18, 12))
    fig.suptitle("Weather Data Analysis Dashboard", fontsize=18, fontweight="bold", y=0.98)

    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.4, wspace=0.35)

    # 1. Temperature over time (top full row)
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(df["date"], df["temperature"], alpha=0.3, color="steelblue", label="Daily")
    ax1.plot(df["date"], df["temperature_sma30"], color="red", linewidth=2, label="30-Day SMA")
    ax1.set_title("Temperature Trend (2021-2023)")
    ax1.set_ylabel("°C")
    ax1.legend(fontsize=8)

    # 2. Monthly temperature bar
    ax2 = fig.add_subplot(gs[1, :2])
    monthly_sorted = monthly_df.sort_values("month")
    ax2.bar(monthly_sorted["month_name"], monthly_sorted["avg_temperature"],
            color=sns.color_palette("coolwarm", 12))
    ax2.set_title("Avg Monthly Temperature")
    ax2.set_ylabel("°C")
    ax2.tick_params(axis="x", rotation=45)

    # 3. Monthly rainfall bar
    ax3 = fig.add_subplot(gs[1, 2])
    ax3.bar(monthly_sorted["month_name"], monthly_sorted["total_rainfall"],
            color=sns.color_palette("Blues_d", 12))
    ax3.set_title("Monthly Rainfall")
    ax3.set_ylabel("mm")
    ax3.tick_params(axis="x", rotation=90)

    # 4. Humidity trend
    ax4 = fig.add_subplot(gs[2, :2])
    ax4.plot(df["date"], df["humidity"], alpha=0.3, color="green", label="Daily")
    ax4.plot(df["date"], df["humidity_sma30"], color="darkgreen", linewidth=2, label="30-Day SMA")
    ax4.set_title("Humidity Trend")
    ax4.set_ylabel("%")
    ax4.legend(fontsize=8)

    # 5. Correlation heatmap
    ax5 = fig.add_subplot(gs[2, 2])
    corr = df[["temperature", "humidity", "rainfall"]].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
                ax=ax5, linewidths=0.5, cbar=False)
    ax5.set_title("Correlation")

    plt.savefig(f"{RESULTS_DIR}/dashboard.png", bbox_inches="tight")
    plt.close()
    print("[PLOT] Saved: dashboard.png (Main Dashboard)")
