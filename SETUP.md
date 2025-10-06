# Setup Guide - S&P 500 Stock Analysis Tool

This guide provides step-by-step instructions for setting up the S&P 500 Stock Analysis Tool on your system.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **Node.js**: Version 16 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: At least 2GB free space
- **Internet**: Stable connection for data downloading

### Required Software

#### Python 3.8+
```bash
# Check Python version
python3 --version

# Install Python (if not installed)
# Windows: Download from python.org
# macOS: brew install python3
# Ubuntu: sudo apt install python3 python3-pip
```

#### Node.js 16+
```bash
# Check Node.js version
node --version
npm --version

# Install Node.js (if not installed)
# Windows/macOS: Download from nodejs.org
# Ubuntu: curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
#         sudo apt-get install -y nodejs
```

#### Git (Optional)
```bash
# Check Git version
git --version

# Install Git (if not installed)
# Windows: Download from git-scm.com
# macOS: brew install git
# Ubuntu: sudo apt install git
```

## 🚀 Installation Steps

### Step 1: Download the Project

#### Option A: Clone with Git
```bash
git clone <repository-url>
cd Stock-Predictive-Model
```

#### Option B: Download ZIP
1. Download the project ZIP file
2. Extract to your desired location
3. Navigate to the extracted folder

### Step 2: Backend Setup

#### 2.1 Create Python Virtual Environment (Recommended)
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### 2.2 Install Python Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

#### 2.3 Initialize Database
```bash
# Run the database setup script
python scripts/setup_database.py

# This will:
# - Create database tables
# - Scrape S&P 500 tickers from Wikipedia
# - Download historical data (this may take 30-60 minutes)
```

**Note**: The initial data download may take 30-60 minutes depending on your internet connection. The script will show progress updates.

#### 2.4 Test Backend
```bash
# Start the backend server
cd backend
python api/run_server.py

# In another terminal, test the API
curl http://localhost:8000/health
```

You should see a response like:
```json
{"status": "healthy", "timestamp": "2024-01-15T10:30:00"}
```

### Step 3: Frontend Setup

#### 3.1 Install Node Dependencies
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Verify installation
npm list
```

#### 3.2 Test Frontend
```bash
# Start the development server
npm start

# The frontend will open at http://localhost:3000
```

### Step 4: Verify Installation

#### 4.1 Check Backend Health
Visit: `http://localhost:8000/health`

Expected response:
```json
{"status": "healthy", "timestamp": "2024-01-15T10:30:00"}
```

#### 4.2 Check Frontend
Visit: `http://localhost:3000`

You should see the S&P 500 Stock Analysis interface.

#### 4.3 Test Complete Flow
1. Select a stock (e.g., AAPL)
2. Wait for charts to load
3. Check seasonality heatmap
4. Review prediction panel

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:
```env
# API Configuration
API_URL=http://localhost:8000
API_TIMEOUT=30000

# Database Configuration
DATABASE_URL=sqlite:///./database/sp500_stocks.db

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Data Update Configuration
UPDATE_DELAY=0.1
MAX_RETRIES=3
```

### Backend Configuration

#### Database Settings
Edit `backend/database/models.py`:
```python
# Change database location
DATABASE_URL = "sqlite:///path/to/your/database.db"
```

#### API Settings
Edit `backend/api/main.py`:
```python
# Change CORS settings for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Production URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Frontend Configuration

#### API Endpoint
Edit `frontend/src/services/api.js`:
```javascript
// Change API base URL for production
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://your-api-domain.com';
```

## 📊 Data Management

### Initial Data Setup

#### Full Database Setup
```bash
# Complete setup with all data
python scripts/setup_database.py --mode full
```

#### Tickers Only
```bash
# Setup only S&P 500 ticker list
python scripts/setup_database.py --mode tickers-only
```

### Daily Updates

#### Manual Update
```bash
# Update all stock data
python scripts/daily_update.py --mode all

# Update specific tickers
python scripts/daily_update.py --mode specific --tickers AAPL MSFT GOOGL

# Check data freshness
python scripts/daily_update.py --mode check
```

#### Automated Updates

**Linux/macOS (Cron)**:
```bash
# Edit crontab
crontab -e

# Add daily update at 6 AM
0 6 * * * cd /path/to/Stock-Predictive-Model && python scripts/daily_update.py --mode all >> logs/daily_update.log 2>&1
```

**Windows (Task Scheduler)**:
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to Daily at 6:00 AM
4. Set action to run: `python scripts/daily_update.py --mode all`
5. Set start in: `C:\path\to\Stock-Predictive-Model`

## 🐛 Troubleshooting

### Common Installation Issues

#### Python Dependencies
```bash
# If pip install fails
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir

# If specific package fails
pip install package_name --upgrade
```

#### Node.js Dependencies
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# If permissions issues (Linux/macOS)
sudo npm install
```

#### Database Issues
```bash
# Check database file
ls -la database/sp500_stocks.db

# Recreate database
rm database/sp500_stocks.db
python scripts/setup_database.py
```

### Runtime Issues

#### Backend Not Starting
```bash
# Check if port 8000 is in use
netstat -an | grep 8000

# Kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Start backend again
cd backend
python api/run_server.py
```

#### Frontend Not Loading
```bash
# Check if port 3000 is in use
netstat -an | grep 3000

# Start frontend on different port
PORT=3001 npm start
```

#### API Connection Issues
```bash
# Test API connectivity
curl http://localhost:8000/health

# Check backend logs
tail -f logs/api.log

# Restart backend
cd backend
python api/run_server.py
```

### Data Issues

#### No Stock Data
```bash
# Check database content
sqlite3 database/sp500_stocks.db "SELECT COUNT(*) FROM stock_data;"

# Re-run data collection
python scripts/setup_database.py --mode full
```

#### Outdated Data
```bash
# Check latest data date
sqlite3 database/sp500_stocks.db "SELECT MAX(date) FROM stock_data;"

# Update data
python scripts/daily_update.py --mode all
```

#### Specific Ticker Issues
```bash
# Update specific ticker
python scripts/daily_update.py --mode specific --tickers AAPL

# Check ticker data
sqlite3 database/sp500_stocks.db "SELECT * FROM stock_data WHERE ticker='AAPL' ORDER BY date DESC LIMIT 5;"
```

## 📈 Performance Optimization

### Database Optimization
```bash
# Optimize SQLite database
sqlite3 database/sp500_stocks.db "VACUUM;"
sqlite3 database/sp500_stocks.db "ANALYZE;"
```

### Backend Optimization
```python
# Increase worker processes (in production)
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend Optimization
```bash
# Build optimized production version
cd frontend
npm run build

# Serve with nginx or Apache
```

## 🔒 Security Considerations

### Production Deployment

#### Backend Security
```python
# Use environment variables for secrets
import os
SECRET_KEY = os.getenv('SECRET_KEY')

# Enable HTTPS
# Configure SSL certificates
# Use proper CORS settings
```

#### Database Security
```bash
# Set proper file permissions
chmod 600 database/sp500_stocks.db

# Regular backups
cp database/sp500_stocks.db backups/sp500_stocks_$(date +%Y%m%d).db
```

## 📞 Getting Help

### Documentation
- Check the main README.md
- Review API documentation at `http://localhost:8000/docs`
- Read inline code comments

### Logs
```bash
# Backend logs
tail -f logs/api.log

# Update logs
tail -f logs/daily_update.log

# Frontend logs (in browser console)
```

### Common Commands Reference

```bash
# Start backend
cd backend && python api/run_server.py

# Start frontend
cd frontend && npm start

# Update data
python scripts/daily_update.py --mode all

# Check health
curl http://localhost:8000/health

# View database
sqlite3 database/sp500_stocks.db

# Check logs
tail -f logs/*.log
```

---

**Setup Complete! 🎉**

Your S&P 500 Stock Analysis Tool should now be running. Visit `http://localhost:3000` to start analyzing stocks!
