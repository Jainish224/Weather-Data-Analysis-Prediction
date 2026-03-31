# Weather Data Analysis and Prediction

**Domain:** Data Analysis & Visualization  
**Tools:** Python, pandas, NumPy, Matplotlib, Seaborn  
**Author:** Jainish Dabgar | B.Tech AI&DS

---

## Project Overview

This project analyzes historical weather data (temperature, humidity, rainfall) and produces:
- Statistical analysis and trend identification
- Seasonal pattern visualizations
- Simple forecasting using Moving Averages
- An interactive summary dashboard

---

## Project Structure

```
weather_analysis/
├── data/
│   ├── weather_data.csv          # Dataset (generated or downloaded)
│   └── generate_data.py          # Script to create synthetic data
├── src/
│   ├── data_loader.py            # Load CSV or API data
│   ├── preprocessing.py          # Cleaning, feature extraction
│   ├── analysis.py               # Statistical analysis
│   ├── visualization.py          # All charts and dashboard
│   └── forecasting.py            # Moving average forecasting
├── tests/
│   └── test_functions.py         # Unit tests (pytest)
├── notebooks/
│   └── weather_analysis.ipynb    # Jupyter Notebook walkthrough
├── results/                      # Auto-created: saved charts
├── main.py                       # Run the full pipeline
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## Installation

1. **Clone or download** this repository.

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate dataset** (if no CSV available):
   ```bash
   cd data/
   python generate_data.py
   cd ..
   ```

---

## Usage

### Run the full pipeline:
```bash
python main.py
```

### Run unit tests:
```bash
python -m pytest tests/ -v
```

### Open Jupyter Notebook:
```bash
jupyter notebook notebooks/weather_analysis.ipynb
```

---

## Dataset

- **Source:** Synthetic data generated using NumPy (simulates Indian climate patterns)
- **Columns:** `date`, `temperature` (°C), `humidity` (%), `rainfall` (mm)
- **Range:** 2021-01-01 to 2023-12-31 (1095 daily records)
- **Alternative:** Real data can be downloaded from [Kaggle Weather Dataset](https://www.kaggle.com/datasets/muthuj7/weather-dataset) or fetched via [OpenWeatherMap API](https://openweathermap.org/api)

---

## Output

All charts are saved to the `results/` folder:
| File | Description |
|------|-------------|
| `dashboard.png` | Summary dashboard (main output) |
| `temperature_trend.png` | Temp trend with SMA/EMA |
| `monthly_averages.png` | Monthly bar charts |
| `seasonal_patterns.png` | Seasonal boxplots |
| `correlation_heatmap.png` | Variable correlation |
| `temperature_forecast.png` | 7-day temperature forecast |
| `humidity_forecast.png` | 7-day humidity forecast |

---

## Key Concepts Used

- **Pandas:** Data loading, cleaning, groupby aggregation
- **NumPy:** Array operations, statistical computation
- **Matplotlib/Seaborn:** Line plots, bar charts, heatmaps, boxplots
- **Moving Averages:** SMA (Simple) and EMA (Exponential) for smoothing & forecasting
- **Time-series features:** Season extraction, monthly/yearly aggregation
- **Unit Testing:** pytest for validating all core functions
