"""
data_loader.py
Handles loading weather data from CSV or OpenWeatherMap API.
Follows PEP 8 standards.
"""

import pandas as pd
import os


def load_csv_data(filepath: str) -> pd.DataFrame:
    """
    Load weather data from a CSV file.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded weather DataFrame with parsed dates.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If required columns are missing.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    df = pd.read_csv(filepath, parse_dates=["date"])

    required_columns = {"date", "temperature", "humidity", "rainfall"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")

    print(f"[INFO] Loaded {len(df)} records from '{filepath}'")
    return df


def fetch_api_data(api_key: str, city: str, days: int = 5) -> pd.DataFrame:
    """
    Fetch weather forecast from OpenWeatherMap API.

    Args:
        api_key (str): Your OpenWeatherMap API key.
        city (str): City name (e.g., 'Ahmedabad').
        days (int): Number of forecast days (max 5 for free tier).

    Returns:
        pd.DataFrame: Weather data with columns [date, temperature, humidity, rainfall].

    Note:
        Requires 'requests' library. Free API key from openweathermap.org
    """
    import requests

    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "cnt": days * 8  # API returns 3-hour intervals
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    records = []
    for item in data["list"]:
        records.append({
            "date": pd.to_datetime(item["dt_txt"]),
            "temperature": item["main"]["temp"],
            "humidity": item["main"]["humidity"],
            "rainfall": item.get("rain", {}).get("3h", 0.0)
        })

    df = pd.DataFrame(records)
    print(f"[INFO] Fetched {len(df)} records from API for '{city}'")
    return df
