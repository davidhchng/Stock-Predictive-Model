# API Documentation - S&P 500 Stock Analysis Tool

This document provides comprehensive API documentation for the S&P 500 Stock Analysis Tool backend.

## 🌐 Base URL

**Development**: `http://localhost:8000`  
**Production**: `https://your-api-domain.com`

## 📊 API Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/tickers` | Get all S&P 500 tickers |
| GET | `/tickers/{ticker}/exists` | Check ticker existence |
| GET | `/stocks/{ticker}/data` | Get historical stock data |
| GET | `/stocks/{ticker}/latest` | Get latest stock data |
| GET | `/analysis/{ticker}/technical` | Get technical analysis |
| GET | `/analysis/{ticker}/indicators` | Get technical indicators |
| GET | `/analysis/{ticker}/seasonality` | Get seasonality analysis |
| GET | `/analysis/{ticker}/seasonality/heatmap` | Get seasonality heatmap |
| GET | `/prediction/{ticker}` | Get next day prediction |
| GET | `/analysis/{ticker}/comprehensive` | Get comprehensive analysis |
| GET | `/analysis/{ticker}/summary` | Get analysis summary |
| GET | `/data/status` | Get data status |

## 🔍 Detailed Endpoint Documentation

### Health Check

#### GET `/health`
Check if the API is running and healthy.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

---

### Ticker Endpoints

#### GET `/tickers`
Get all S&P 500 ticker symbols and company names.

**Response:**
```json
[
  {
    "ticker": "AAPL",
    "name": "Apple Inc."
  },
  {
    "ticker": "MSFT",
    "name": "Microsoft Corporation"
  }
]
```

#### GET `/tickers/{ticker}/exists`
Check if a ticker exists in the database.

**Parameters:**
- `ticker` (path): Stock ticker symbol (e.g., "AAPL")

**Response:**
```json
{
  "ticker": "AAPL",
  "exists": true
}
```

---

### Stock Data Endpoints

#### GET `/stocks/{ticker}/data`
Get historical stock data for a specific ticker.

**Parameters:**
- `ticker` (path): Stock ticker symbol
- `start_date` (query, optional): Start date in YYYY-MM-DD format
- `end_date` (query, optional): End date in YYYY-MM-DD format

**Example Request:**
```
GET /stocks/AAPL/data?start_date=2024-01-01&end_date=2024-01-31
```

**Response:**
```json
[
  {
    "date": "2024-01-15",
    "open": 185.92,
    "high": 186.40,
    "low": 182.13,
    "close": 185.14,
    "adj_close": 185.14,
    "volume": 52393000
  }
]
```

#### GET `/stocks/{ticker}/latest`
Get the latest stock data for a ticker.

**Parameters:**
- `ticker` (path): Stock ticker symbol

**Response:**
```json
{
  "ticker": "AAPL",
  "latest_date": "2024-01-15",
  "data": [
    {
      "date": "2024-01-15",
      "open": 185.92,
      "high": 186.40,
      "low": 182.13,
      "close": 185.14,
      "adj_close": 185.14,
      "volume": 52393000
    }
  ]
}
```

---

### Technical Analysis Endpoints

#### GET `/analysis/{ticker}/technical`
Get comprehensive technical analysis for a ticker.

**Parameters:**
- `ticker` (path): Stock ticker symbol

**Response:**
```json
{
  "ticker": "AAPL",
  "period_days": 252,
  "price_change_percent": 15.2,
  "volatility": 0.0234,
  "trend_strength": "strong",
  "technical_indicators": {
    "current_price": 185.14,
    "daily_return": 0.0123,
    "volatility_20d": 0.0234,
    "ma_20": 182.45,
    "ma_50": 178.92,
    "ma_200": 165.34,
    "price_vs_ma20": 1.47,
    "price_vs_ma50": 3.48,
    "price_vs_ma200": 12.0,
    "rsi": 65.4,
    "macd": 2.34,
    "macd_signal": 1.89,
    "bb_upper": 188.45,
    "bb_lower": 176.23,
    "stoch_k": 78.2,
    "stoch_d": 72.1,
    "volume": 52393000,
    "volume_ma": 45123000,
    "obv": 1234567890
  },
  "trend_signals": {
    "ma_trend_short": 1,
    "ma_trend_medium": 1,
    "ma_trend_long": 1,
    "overall_trend": 1.0,
    "rsi_oversold": 0,
    "rsi_overbought": 0,
    "macd_bullish": 1,
    "macd_bearish": 0
  }
}
```

#### GET `/analysis/{ticker}/indicators`
Get current technical indicators only.

**Parameters:**
- `ticker` (path): Stock ticker symbol

**Response:**
```json
{
  "current_price": 185.14,
  "daily_return": 0.0123,
  "volatility_20d": 0.0234,
  "ma_20": 182.45,
  "ma_50": 178.92,
  "ma_200": 165.34,
  "rsi": 65.4,
  "macd": 2.34,
  "macd_signal": 1.89
}
```

---

### Seasonality Analysis Endpoints

#### GET `/analysis/{ticker}/seasonality`
Get comprehensive seasonality analysis.

**Parameters:**
- `ticker` (path): Stock ticker symbol

**Response:**
```json
{
  "monthly_patterns": {
    "1": {
      "month_name": "January",
      "avg_return": 0.0123,
      "median_return": 0.0089,
      "std_return": 0.0456,
      "positive_days": 245,
      "total_days": 420,
      "win_rate": 0.583,
      "avg_volume": 52393000,
      "avg_price_change": 0.0123
    }
  },
  "quarterly_patterns": {
    "1": {
      "quarter_name": "Q1 (Jan-Mar)",
      "avg_return": 0.0234,
      "median_return": 0.0198,
      "std_return": 0.0678,
      "positive_days": 1250,
      "total_days": 2100,
      "win_rate": 0.595,
      "avg_volume": 50123000,
      "total_return": 0.1234
    }
  },
  "dow_patterns": {
    "0": {
      "day_name": "Monday",
      "avg_return": -0.0012,
      "median_return": -0.0008,
      "std_return": 0.0234,
      "positive_days": 180,
      "total_days": 350,
      "win_rate": 0.514,
      "avg_volume": 48923000
    }
  },
  "month_end_effect": {
    "month_end": {
      "avg_return": 0.0056,
      "median_return": 0.0034,
      "std_return": 0.0234,
      "positive_days": 45,
      "total_days": 78,
      "win_rate": 0.577
    },
    "other_days": {
      "avg_return": 0.0023,
      "median_return": 0.0018,
      "std_return": 0.0234,
      "positive_days": 1200,
      "total_days": 2300,
      "win_rate": 0.522
    }
  },
  "summary": {
    "best_month": {
      "month": 11,
      "month_name": "November",
      "avg_return": 0.0234
    },
    "worst_month": {
      "month": 9,
      "month_name": "September",
      "avg_return": -0.0123
    },
    "seasonality_strength": "moderate"
  }
}
```

#### GET `/analysis/{ticker}/seasonality/heatmap`
Get seasonality heatmap data for visualization.

**Parameters:**
- `ticker` (path): Stock ticker symbol
- `period_type` (query): "monthly" or "quarterly" (default: "monthly")

**Example Request:**
```
GET /analysis/AAPL/seasonality/heatmap?period_type=monthly
```

**Response:**
```json
{
  "2020": {
    "1": 0.0123,
    "2": -0.0234,
    "3": 0.0456
  },
  "2021": {
    "1": 0.0234,
    "2": 0.0345,
    "3": 0.0123
  }
}
```

---

### Prediction Endpoints

#### GET `/prediction/{ticker}`
Get next day prediction for a ticker.

**Parameters:**
- `ticker` (path): Stock ticker symbol

**Response:**
```json
{
  "prediction": "bullish",
  "probability": 0.734,
  "confidence": "high",
  "model_used": "random_forest",
  "features_analyzed": 20
}
```

**Prediction Values:**
- `prediction`: "bullish", "bearish", or "neutral"
- `confidence`: "high", "medium", or "low"
- `probability`: Float between 0 and 1

---

### Comprehensive Analysis Endpoints

#### GET `/analysis/{ticker}/comprehensive`
Get complete analysis including technical, seasonality, and predictions.

**Parameters:**
- `ticker` (path): Stock ticker symbol

**Response:**
```json
{
  "ticker": "AAPL",
  "analysis_date": "2024-01-15T10:30:00.000Z",
  "data_period": {
    "start_date": "2018-01-01",
    "end_date": "2024-01-15",
    "total_days": 2205
  },
  "technical_analysis": {
    "current_indicators": {
      "current_price": 185.14,
      "daily_return": 0.0123,
      "volatility_20d": 0.0234,
      "ma_20": 182.45,
      "rsi": 65.4,
      "macd": 2.34
    },
    "trend_signals": {
      "overall_trend": 1.0,
      "ma_trend_short": 1,
      "rsi_oversold": 0
    },
    "data_with_indicators": []
  },
  "seasonality_analysis": {
    "monthly_patterns": {},
    "quarterly_patterns": {},
    "summary": {
      "best_month": {
        "month": 11,
        "month_name": "November",
        "avg_return": 0.0234
      },
      "seasonality_strength": "moderate"
    }
  },
  "predictive_analysis": {
    "next_day_prediction": {
      "prediction": "bullish",
      "probability": 0.734,
      "confidence": "high",
      "model_used": "random_forest",
      "features_analyzed": 20
    },
    "feature_importance": {
      "Price_vs_MA20": 0.1234,
      "RSI": 0.0987,
      "Momentum_5d": 0.0876
    },
    "backtest_results": {
      "accuracy": 0.678,
      "total_return": 0.234,
      "win_rate": 0.612,
      "total_trades": 450,
      "avg_probability": 0.567
    }
  },
  "summary": {
    "overall_sentiment": "bullish",
    "confidence_level": "high",
    "key_insights": [
      "Price is significantly above 20-day moving average",
      "Strong seasonal patterns detected",
      "High confidence bullish prediction for next day"
    ],
    "recommendations": [
      "Strong buy signal - consider long position"
    ],
    "disclaimer": "This analysis is for educational purposes only and should not be considered financial advice"
  }
}
```

#### GET `/analysis/{ticker}/summary`
Get analysis summary with recommendations.

**Parameters:**
- `ticker` (path): Stock ticker symbol

**Response:**
```json
{
  "overall_sentiment": "bullish",
  "confidence_level": "high",
  "key_insights": [
    "Price is significantly above 20-day moving average",
    "Strong seasonal patterns detected"
  ],
  "recommendations": [
    "Strong buy signal - consider long position"
  ]
}
```

---

### Data Management Endpoints

#### GET `/data/status`
Get status of data in the database.

**Response:**
```json
{
  "total_tickers": 503,
  "tickers_with_data": 498,
  "data_coverage": 99.0,
  "last_updated": "2024-01-15T06:00:00.000Z"
}
```

---

## 🔧 Error Handling

### HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Resource not found |
| 500 | Internal server error |

### Error Response Format

```json
{
  "detail": "Error message description",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### Common Error Scenarios

#### Ticker Not Found
```json
{
  "detail": "No data found for ticker INVALID"
}
```

#### Insufficient Data
```json
{
  "detail": "Insufficient data for prediction (need at least 100 days)"
}
```

#### Server Error
```json
{
  "detail": "Internal server error",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

---

## 📝 Usage Examples

### Python Example

```python
import requests
import json

# Base URL
BASE_URL = "http://localhost:8000"

# Get all tickers
tickers = requests.get(f"{BASE_URL}/tickers").json()
print(f"Found {len(tickers)} tickers")

# Get stock data for AAPL
data = requests.get(f"{BASE_URL}/stocks/AAPL/data").json()
print(f"Retrieved {len(data)} data points for AAPL")

# Get prediction for MSFT
prediction = requests.get(f"{BASE_URL}/prediction/MSFT").json()
print(f"Prediction: {prediction['prediction']} ({prediction['probability']:.2%})")

# Get comprehensive analysis
analysis = requests.get(f"{BASE_URL}/analysis/GOOGL/comprehensive").json()
print(f"Overall sentiment: {analysis['summary']['overall_sentiment']}")
```

### JavaScript Example

```javascript
const API_BASE = 'http://localhost:8000';

// Get all tickers
fetch(`${API_BASE}/tickers`)
  .then(response => response.json())
  .then(tickers => console.log(`Found ${tickers.length} tickers`));

// Get prediction for a ticker
async function getPrediction(ticker) {
  const response = await fetch(`${API_BASE}/prediction/${ticker}`);
  const prediction = await response.json();
  return prediction;
}

// Usage
getPrediction('AAPL').then(prediction => {
  console.log(`Prediction: ${prediction.prediction} (${(prediction.probability * 100).toFixed(1)}%)`);
});
```

### cURL Examples

```bash
# Health check
curl http://localhost:8000/health

# Get all tickers
curl http://localhost:8000/tickers

# Get stock data
curl "http://localhost:8000/stocks/AAPL/data?start_date=2024-01-01&end_date=2024-01-31"

# Get prediction
curl http://localhost:8000/prediction/MSFT

# Get comprehensive analysis
curl http://localhost:8000/analysis/GOOGL/comprehensive
```

---

## 🔒 Authentication & Rate Limiting

Currently, the API does not require authentication. For production deployment, consider implementing:

- API key authentication
- Rate limiting
- CORS configuration
- HTTPS enforcement

---

## 📊 Data Formats

### Date Format
All dates are in ISO 8601 format: `YYYY-MM-DD`

### Price Format
All prices are floating-point numbers with appropriate decimal precision.

### Volume Format
Volume is represented as integers.

### Return Format
Returns are represented as decimal values (e.g., 0.05 = 5%)

---

## 🚀 Performance Considerations

### Response Times
- Health check: < 50ms
- Ticker list: < 100ms
- Stock data: < 500ms
- Analysis: < 2s
- Predictions: < 3s

### Caching
Consider implementing caching for:
- Ticker lists
- Technical indicators
- Seasonality patterns

### Pagination
For large datasets, consider implementing pagination:
```
GET /stocks/AAPL/data?page=1&limit=100
```

---

## 📞 Support

For API issues or questions:
- Check the troubleshooting section in README.md
- Review server logs
- Test with the health endpoint
- Verify data availability

---

**API Documentation Complete! 📚**
