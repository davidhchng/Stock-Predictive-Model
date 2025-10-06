# S&P 500 Stock Analysis Tool

A comprehensive full-stack web application for analyzing S&P 500 stock trends, seasonality patterns, and AI-powered predictions.

## 🌟 Features

### 📊 Technical Analysis
- **Interactive Price Charts**: Candlestick and line charts with technical indicators
- **Moving Averages**: 5, 10, 20, 50, and 200-day moving averages
- **Technical Indicators**: RSI, MACD, Bollinger Bands, Stochastic Oscillator
- **Volume Analysis**: Volume indicators and price-volume relationships

### 📅 Seasonality Analysis
- **Monthly Patterns**: Historical performance by month
- **Quarterly Trends**: Quarterly performance analysis
- **Interactive Heatmaps**: Visual representation of seasonal patterns
- **Day-of-Week Effects**: Analysis of weekday performance patterns

### 🤖 AI Predictions
- **Next-Day Predictions**: Machine learning models for price direction
- **Multiple Algorithms**: Random Forest, Gradient Boosting, Logistic Regression
- **Feature Engineering**: 20+ technical and fundamental features
- **Confidence Levels**: High, medium, and low confidence predictions

### 🔄 Automated Data Management
- **Daily Updates**: Automated data collection from Yahoo Finance
- **S&P 500 Tickers**: Current list scraped from Wikipedia
- **Historical Data**: Data from 2018 to present
- **Database Management**: SQLite with optimized queries

## 🏗️ Architecture

### Backend (Python)
- **FastAPI**: Modern, fast web framework for APIs
- **SQLite**: Lightweight database for data storage
- **scikit-learn**: Machine learning models and preprocessing
- **yfinance**: Yahoo Finance data integration
- **BeautifulSoup**: Web scraping for S&P 500 tickers

### Frontend (React)
- **React 18**: Modern React with hooks
- **Material-UI**: Professional UI components
- **Plotly.js**: Interactive charts and visualizations
- **Axios**: HTTP client for API communication

### Data Flow
```
Wikipedia/Yahoo Finance → Data Collectors → SQLite Database → FastAPI Backend → React Frontend
```

## 📁 Project Structure

```
Stock-Predictive-Model/
├── backend/
│   ├── api/
│   │   ├── main.py                 # FastAPI application
│   │   └── run_server.py           # Server runner
│   ├── database/
│   │   ├── models.py               # SQLAlchemy models
│   │   └── database_manager.py     # Database operations
│   ├── scrapers/
│   │   ├── sp500_scraper.py        # Wikipedia S&P 500 scraper
│   │   ├── yahoo_data_fetcher.py   # Yahoo Finance data fetcher
│   │   └── data_collector.py       # Main data collection orchestrator
│   └── analysis/
│       ├── technical_indicators.py # Technical analysis functions
│       ├── seasonality_analysis.py # Seasonality analysis
│       ├── predictive_model.py     # Machine learning models
│       └── analysis_orchestrator.py # Analysis coordinator
├── frontend/
│   ├── src/
│   │   ├── components/             # React components
│   │   ├── services/               # API service layer
│   │   └── App.js                  # Main application
│   └── package.json                # Frontend dependencies
├── scripts/
│   ├── setup_database.py           # Database initialization
│   ├── daily_update.py             # Daily update script
│   └── cron_setup.md               # Scheduling instructions
├── database/                       # SQLite database files
├── analysis/                       # Analysis modules
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Stock-Predictive-Model
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Initialize Database
```bash
python scripts/setup_database.py
```

This will:
- Create database tables
- Scrape current S&P 500 tickers from Wikipedia
- Download historical data for all tickers (2018-present)
- Set up initial data structure

#### Start Backend Server
```bash
cd backend
python api/run_server.py
```

The API will be available at `http://localhost:8000`

### 3. Frontend Setup

#### Install Node Dependencies
```bash
cd frontend
npm install
```

#### Start Development Server
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

### 4. Access the Application
Open your browser and navigate to `http://localhost:3000`

## 📊 API Documentation

### Endpoints

#### Health Check
- `GET /health` - Check API status

#### Tickers
- `GET /tickers` - Get all S&P 500 tickers
- `GET /tickers/{ticker}/exists` - Check if ticker exists

#### Stock Data
- `GET /stocks/{ticker}/data` - Get historical data
- `GET /stocks/{ticker}/latest` - Get latest data

#### Analysis
- `GET /analysis/{ticker}/technical` - Technical analysis
- `GET /analysis/{ticker}/seasonality` - Seasonality analysis
- `GET /analysis/{ticker}/comprehensive` - Full analysis
- `GET /prediction/{ticker}` - Next day prediction

### Example API Usage
```python
import requests

# Get all tickers
tickers = requests.get('http://localhost:8000/tickers').json()

# Get stock data for AAPL
data = requests.get('http://localhost:8000/stocks/AAPL/data').json()

# Get prediction for MSFT
prediction = requests.get('http://localhost:8000/prediction/MSFT').json()
```

## 🔄 Daily Updates

### Automated Updates
Set up automated daily updates to keep data fresh:

#### Linux/macOS (Cron)
```bash
# Add to crontab (crontab -e)
0 6 * * * cd /path/to/Stock-Predictive-Model && python scripts/daily_update.py --mode all
```

#### Windows (Task Scheduler)
Create a scheduled task to run:
```bash
python scripts/daily_update.py --mode all
```

### Manual Updates
```bash
# Update all data
python scripts/daily_update.py --mode all

# Update specific tickers
python scripts/daily_update.py --mode specific --tickers AAPL MSFT GOOGL

# Check data freshness
python scripts/daily_update.py --mode check
```

## 🧠 Machine Learning Models

### Features Used
- Price momentum (5-day, 10-day)
- Moving average ratios
- Volatility indicators
- Volume ratios
- Technical indicators (RSI, MACD, Bollinger Bands)
- Seasonal features (month, quarter, day of week)
- Lagged returns and volume

### Models
1. **Random Forest**: Ensemble method with 100 trees
2. **Gradient Boosting**: Sequential boosting algorithm
3. **Logistic Regression**: Linear model with regularization

### Performance Metrics
- Accuracy score
- Win rate
- Feature importance
- Backtesting results

## 📈 Usage Guide

### 1. Stock Selection
- Use the search bar to find any S&P 500 company
- Search by ticker symbol or company name
- Real-time filtering and autocomplete

### 2. Price Chart Analysis
- Switch between candlestick and line charts
- Toggle technical indicators (moving averages)
- Interactive zoom and pan
- Hover for detailed price information

### 3. Seasonality Analysis
- View monthly or quarterly patterns
- Interactive heatmap visualization
- Best/worst performing periods
- Historical performance insights

### 4. AI Predictions
- Next-day price direction prediction
- Confidence levels (high/medium/low)
- Probability scores
- Key insights and recommendations

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:
```env
API_URL=http://localhost:8000
DATABASE_URL=sqlite:///./database/sp500_stocks.db
LOG_LEVEL=INFO
```

### Backend Configuration
Modify `backend/api/main.py` for:
- CORS settings
- Rate limiting
- Database connections
- Logging levels

### Frontend Configuration
Modify `frontend/src/services/api.js` for:
- API base URL
- Request timeouts
- Error handling

## 🐛 Troubleshooting

### Common Issues

#### Database Connection Errors
```bash
# Check database file permissions
ls -la database/sp500_stocks.db

# Recreate database
python scripts/setup_database.py
```

#### API Connection Issues
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check logs
tail -f logs/api.log
```

#### Frontend Build Issues
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### Data Loading Issues
```bash
# Check data freshness
python scripts/daily_update.py --mode check

# Force update specific ticker
python scripts/daily_update.py --mode specific --tickers AAPL
```

### Performance Optimization

#### Database Optimization
- Regular VACUUM operations
- Index optimization
- Query performance monitoring

#### API Optimization
- Response caching
- Rate limiting
- Connection pooling

#### Frontend Optimization
- Component memoization
- Lazy loading
- Bundle optimization

## 📚 Additional Resources

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/docs/)
- [Material-UI Documentation](https://mui.com/)
- [Plotly.js Documentation](https://plotly.com/javascript/)

### Financial Data Sources
- [Yahoo Finance API](https://finance.yahoo.com/)
- [S&P 500 Wikipedia Page](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies)

### Machine Learning Resources
- [scikit-learn Documentation](https://scikit-learn.org/)
- [Technical Analysis Library](https://github.com/bukosabino/ta)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for educational and research purposes only. The predictions and analysis should not be considered as financial advice. Always consult with qualified financial professionals before making investment decisions. Past performance does not guarantee future results.

## 📞 Support

For questions, issues, or contributions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the documentation

---

**Happy Analyzing! 📊🚀**