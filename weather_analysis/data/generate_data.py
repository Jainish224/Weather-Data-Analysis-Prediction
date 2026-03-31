"""
generate_data.py
Generates a synthetic weather dataset for demonstration purposes.
Run this once to create weather_data.csv in the data/ folder.
"""

import pandas as pd
import numpy as np

# Seed for reproducibility
np.random.seed(42)

# Generate 3 years of daily data (2021-2023)
dates = pd.date_range(start="2021-01-01", end="2023-12-31", freq="D")
n = len(dates)

# Simulate temperature with seasonal pattern (India-like)
day_of_year = np.array([d.timetuple().tm_yday for d in dates])
temperature = (
    25
    + 10 * np.sin(2 * np.pi * (day_of_year - 80) / 365)  # seasonal trend
    + np.random.normal(0, 2, n)                             # noise
)

# Simulate humidity (higher in monsoon: June-September)
humidity = (
    60
    + 20 * np.sin(2 * np.pi * (day_of_year - 160) / 365)
    + np.random.normal(0, 5, n)
)
humidity = np.clip(humidity, 20, 100)

# Simulate rainfall (mostly in monsoon months)
month = np.array([d.month for d in dates])
rainfall_prob = np.where((month >= 6) & (month <= 9), 0.5, 0.1)
rainfall = np.where(
    np.random.rand(n) < rainfall_prob,
    np.random.exponential(5, n),
    0.0
)
rainfall = np.round(rainfall, 2)

# Create DataFrame
df = pd.DataFrame({
    "date": dates,
    "temperature": np.round(temperature, 2),
    "humidity": np.round(humidity, 2),
    "rainfall": rainfall
})

# Save to CSV
df.to_csv("data/weather_data.csv", index=False)
print(f"Dataset created: {len(df)} rows")
print(df.head())
