# Results Report — Weather Data Analysis and Prediction

**Project:** Weather Data Analysis and Prediction  
**Domain:** Data Analysis & Visualization  
**Author:** [Your Name] | Roll No: [Your Roll No]  
**Subject:** Python Programming  
**Date:** March 2026  

---

## 1. Dataset Overview

| Property | Value |
|----------|-------|
| Total Records | 1,095 daily entries |
| Date Range | 2021-01-01 to 2023-12-31 |
| Features | date, temperature (°C), humidity (%), rainfall (mm) |
| Missing Values | 0 (after cleaning) |
| Outliers Removed | 0 (all values within 3σ) |

---

## 2. Summary Statistics

| Metric | Temperature (°C) | Humidity (%) | Rainfall (mm) |
|--------|-----------------|--------------|---------------|
| Mean   | 25.07 | 60.19 | 1.09 |
| Std Dev | 7.37 | 14.98 | 3.26 |
| Min    | 10.00 | 26.01 | 0.00 |
| 25th % | 18.32 | 47.29 | 0.00 |
| Median | 24.88 | 60.57 | 0.00 |
| 75th % | 31.67 | 73.77 | 0.00 |
| Max    | 40.56 | 89.47 | 30.48 |

---

## 3. Correlation Analysis

| | Temperature | Humidity | Rainfall |
|---|---|---|---|
| **Temperature** | 1.000 | 0.176 | 0.124 |
| **Humidity**    | 0.176 | 1.000 | 0.161 |
| **Rainfall**    | 0.124 | 0.161 | 1.000 |

**Interpretation:** All variables show weak positive correlation. During monsoon months, humidity and rainfall tend to rise together, explaining the 0.161 humidity-rainfall correlation.

---

## 4. Seasonal Analysis

| Season | Avg Temp (°C) | Avg Humidity (%) | Total Rainfall (mm) | Rainy Days |
|--------|--------------|-----------------|---------------------|------------|
| Winter | 16.85 | 49.64 | 199.07 | ~28 |
| Summer | 28.80 | 45.53 | 83.96 | ~27 |
| **Monsoon** | **31.38** | **73.15** | **818.79** | **~131** |
| Post-Monsoon | 18.92 | 71.95 | 94.55 | ~17 |

**Key Finding:** Monsoon accounts for ~65% of the total annual rainfall despite covering only 4 months.

---

## 5. Monthly Highlights

| Metric | Best Month | Value |
|--------|-----------|-------|
| Hottest | May | ~33.1°C avg |
| Coolest | December | ~15.0°C avg |
| Wettest | August | ~225 mm total |
| Most Rainy Days | Aug/Sep | ~48 days each (across 3 years) |
| Most Humid | September | ~79.6% avg |
| Driest | March | ~23 mm total |

---

## 6. Forecasting Model — Moving Average

### Model Type
**Simple Moving Average (SMA)** with 30-day window as the baseline prediction, combined with a small noise component derived from historical standard deviation.

### Forecast Formula
```
predicted_value = mean(last_30_values) + N(0, 0.1 × σ)
```

### 7-Day Temperature Forecast (from 2024-01-01)

| Date | Predicted Temp (°C) |
|------|-------------------|
| 2024-01-01 | 16.61 |
| 2024-01-02 | 15.61 |
| 2024-01-03 | 16.03 |
| 2024-01-04 | 16.97 |
| 2024-01-05 | 16.69 |
| 2024-01-06 | 14.59 |
| 2024-01-07 | 16.01 |

**Avg Forecast Temperature:** ~16.1°C — consistent with January being a winter month.

### Model Limitations
- Moving average assumes future follows recent past — cannot predict sudden weather events
- No external factors (El Niño, pressure systems) are included
- For production use, ARIMA or LSTM models would give better accuracy

---

## 7. Visualizations Produced

| File | Description |
|------|-------------|
| `dashboard.png` | Main summary dashboard (all-in-one) |
| `temperature_trend.png` | 3-year temperature with SMA/EMA |
| `monthly_averages.png` | Monthly bars for temp, humidity, rainfall |
| `seasonal_patterns.png` | Seasonal boxplots |
| `correlation_heatmap.png` | Pearson correlation heatmap |
| `temperature_forecast.png` | 7-day temperature forecast |
| `humidity_forecast.png` | 7-day humidity forecast |
| `distributions.png` | Histogram distributions |
| `yearly_trend.png` | Year-over-year comparison |

---

## 8. Unit Test Results

| Test | Status |
|------|--------|
| clean_data returns DataFrame | ✅ PASS |
| No negative rainfall after clean | ✅ PASS |
| Humidity within 0-100 range | ✅ PASS |
| Time features added correctly | ✅ PASS |
| get_season Winter mapping | ✅ PASS |
| get_season Monsoon mapping | ✅ PASS |
| SMA output length matches input | ✅ PASS |
| EMA produces no NaN values | ✅ PASS |
| Forecast returns exactly N rows | ✅ PASS |
| Forecast dates are in the future | ✅ PASS |
| Correlation diagonal equals 1.0 | ✅ PASS |

**Total: 11/11 tests passed ✅**

---

## 9. Conclusion

This project successfully demonstrated:

1. **Data collection** — generating realistic weather data with seasonal Indian climate patterns
2. **Preprocessing** — handling missing values, outlier detection, feature extraction
3. **Statistical analysis** — descriptive stats, monthly/seasonal/yearly aggregations
4. **Correlation analysis** — identifying variable relationships
5. **Forecasting** — SMA and EMA-based short-term prediction
6. **Visualization** — 9 publication-quality charts + interactive dashboard

The analysis confirmed expected patterns: India's Monsoon dominates annual rainfall, Summer peaks in temperature, and all variables show seasonal cyclicity consistent with real-world climate behavior.

---

*Report generated as part of Python Programming Project | B.Tech AI&DS*
