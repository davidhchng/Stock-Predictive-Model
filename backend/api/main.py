"""
FastAPI backend for S&P 500 Stock Analysis Tool
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import date, datetime
import logging

# Import our modules
from database.database_manager import DatabaseManager
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from analysis.analysis_orchestrator import AnalysisOrchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="S&P 500 Stock Analysis API",
    description="API for analyzing S&P 500 stock trends, seasonality, and predictions",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
db_manager = DatabaseManager()
analysis_orchestrator = AnalysisOrchestrator()

# Pydantic models for request/response
class TickerResponse(BaseModel):
    ticker: str
    name: str

class StockDataResponse(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: int

class TechnicalAnalysisResponse(BaseModel):
    current_indicators: Dict[str, Any]
    trend_signals: Dict[str, Any]

class PredictionResponse(BaseModel):
    prediction: str
    probability: float
    confidence: str
    model_used: Optional[str] = None
    features_analyzed: Optional[int] = None

class SeasonalityResponse(BaseModel):
    monthly_patterns: Dict[str, Any]
    quarterly_patterns: Dict[str, Any]
    dow_patterns: Dict[str, Any]
    summary: Dict[str, Any]

class AnalysisSummaryResponse(BaseModel):
    overall_sentiment: str
    confidence_level: str
    key_insights: List[str]
    recommendations: List[str]

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/init-database")
async def init_database():
    """Initialize database with S&P 500 data"""
    try:
        from backend.scrapers.data_collector import DataCollector
        from backend.database.database_manager import DatabaseManager
        
        # Initialize database
        db_manager = DatabaseManager()
        
        # Collect S&P 500 data
        collector = DataCollector()
        result = collector.collect_all_data()
        
        return {
            "status": "success", 
            "message": "Database initialized successfully",
            "tickers_added": result.get("tickers_added", 0),
            "stocks_processed": result.get("stocks_processed", 0)
        }
    except Exception as e:
        return {"status": "error", "message": f"Database initialization failed: {str(e)}"}

# Ticker endpoints
@app.get("/tickers", response_model=List[TickerResponse])
async def get_tickers():
    """Get all S&P 500 tickers"""
    try:
        tickers = db_manager.get_all_tickers()
        return [TickerResponse(ticker=ticker, name=name) for ticker, name in tickers]
    except Exception as e:
        logger.error(f"Error getting tickers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tickers/{ticker}/exists")
async def check_ticker_exists(ticker: str):
    """Check if a ticker exists in the database"""
    try:
        tickers = db_manager.get_all_tickers()
        ticker_symbols = [t[0] for t in tickers]
        exists = ticker.upper() in ticker_symbols
        return {"ticker": ticker.upper(), "exists": exists}
    except Exception as e:
        logger.error(f"Error checking ticker existence: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Stock data endpoints
@app.get("/stocks/{ticker}/data", response_model=List[StockDataResponse])
async def get_stock_data(
    ticker: str,
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)")
):
    """Get historical stock data for a ticker"""
    try:
        ticker = ticker.upper()
        stock_data = db_manager.get_stock_data(ticker, start_date, end_date)
        
        if stock_data.empty:
            raise HTTPException(status_code=404, detail=f"No data found for ticker {ticker}")
        
        # Convert to response format
        response_data = []
        for date_idx, row in stock_data.iterrows():
            # Handle both date and datetime index
            if hasattr(date_idx, 'date'):
                date_str = str(date_idx.date())
            else:
                date_str = str(date_idx)
            
            response_data.append(StockDataResponse(
                date=date_str,
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                adj_close=row['Adj Close'],
                volume=int(row['Volume'])
            ))
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting stock data for {ticker}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stocks/{ticker}/latest")
async def get_latest_stock_data(ticker: str):
    """Get latest stock data for a ticker"""
    try:
        ticker = ticker.upper()
        latest_date = db_manager.get_latest_date(ticker)
        
        if not latest_date:
            raise HTTPException(status_code=404, detail=f"No data found for ticker {ticker}")
        
        # Get data for the last 5 days
        stock_data = db_manager.get_stock_data(ticker, None, latest_date)
        latest_data = stock_data.tail(5)
        
        return {
            "ticker": ticker,
            "latest_date": str(latest_date),
            "data": [
                {
                    "date": str(date_idx.date()),
                    "open": row['Open'],
                    "high": row['High'],
                    "low": row['Low'],
                    "close": row['Close'],
                    "adj_close": row['Adj Close'],
                    "volume": int(row['Volume'])
                }
                for date_idx, row in latest_data.iterrows()
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting latest data for {ticker}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Technical analysis endpoints
@app.get("/analysis/{ticker}/technical")
async def get_technical_analysis(ticker: str):
    """Get technical analysis for a ticker"""
    try:
        ticker = ticker.upper()
        trend_analysis = analysis_orchestrator.get_trend_analysis(ticker)
        
        if 'error' in trend_analysis:
            raise HTTPException(status_code=404, detail=trend_analysis['error'])
        
        return trend_analysis
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting technical analysis for {ticker}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analysis/{ticker}/indicators")
async def get_technical_indicators(ticker: str):
    """Get current technical indicators for a ticker"""
    try:
        ticker = ticker.upper()
        comprehensive_analysis = analysis_orchestrator.get_comprehensive_analysis(ticker)
        
        if 'error' in comprehensive_analysis:
            raise HTTPException(status_code=404, detail=comprehensive_analysis['error'])
        
        technical_analysis = comprehensive_analysis.get('technical_analysis', {})
        return technical_analysis.get('current_indicators', {})
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting technical indicators for {ticker}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Seasonality analysis endpoints
@app.get("/analysis/{ticker}/seasonality")
async def get_seasonality_analysis(ticker: str):
    """Get seasonality analysis for a ticker"""
    try:
        ticker = ticker.upper()
        seasonality_analysis = analysis_orchestrator.get_seasonality_analysis(ticker)
        
        if 'error' in seasonality_analysis:
            raise HTTPException(status_code=404, detail=seasonality_analysis['error'])
        
        return seasonality_analysis
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting seasonality analysis for {ticker}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analysis/{ticker}/seasonality/heatmap")
async def get_seasonality_heatmap(ticker: str, period_type: str = Query("monthly", regex="^(monthly|quarterly)$")):
    """Get seasonality heatmap data for visualization"""
    try:
        ticker = ticker.upper()
        comprehensive_analysis = analysis_orchestrator.get_comprehensive_analysis(ticker)
        
        if 'error' in comprehensive_analysis:
            raise HTTPException(status_code=404, detail=comprehensive_analysis['error'])
        
        seasonality_analysis = comprehensive_analysis.get('seasonality_analysis', {})
        heatmap_key = f'heatmap_data_{period_type}'
        heatmap_data = seasonality_analysis.get(heatmap_key, {})
        
        # Convert to JSON-serializable format
        if hasattr(heatmap_data, 'to_dict'):
            return heatmap_data.to_dict()
        else:
            return heatmap_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting seasonality heatmap for {ticker}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Prediction endpoints
@app.get("/prediction/{ticker}", response_model=PredictionResponse)
async def get_prediction(ticker: str):
    """Get next day prediction for a ticker"""
    try:
        ticker = ticker.upper()
        prediction = analysis_orchestrator.get_prediction(ticker)
        
        if 'error' in prediction:
            raise HTTPException(status_code=404, detail=prediction['error'])
        
        return PredictionResponse(**prediction)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting prediction for {ticker}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Comprehensive analysis endpoint
@app.get("/analysis/{ticker}/comprehensive")
async def get_comprehensive_analysis(ticker: str):
    """Get comprehensive analysis including technical, seasonality, and predictions"""
    try:
        ticker = ticker.upper()
        comprehensive_analysis = analysis_orchestrator.get_comprehensive_analysis(ticker)
        
        if 'error' in comprehensive_analysis:
            raise HTTPException(status_code=404, detail=comprehensive_analysis['error'])
        
        return comprehensive_analysis
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting comprehensive analysis for {ticker}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analysis/{ticker}/summary", response_model=AnalysisSummaryResponse)
async def get_analysis_summary(ticker: str):
    """Get analysis summary with recommendations"""
    try:
        ticker = ticker.upper()
        comprehensive_analysis = analysis_orchestrator.get_comprehensive_analysis(ticker)
        
        if 'error' in comprehensive_analysis:
            raise HTTPException(status_code=404, detail=comprehensive_analysis['error'])
        
        summary = comprehensive_analysis.get('summary', {})
        return AnalysisSummaryResponse(**summary)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting analysis summary for {ticker}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Data management endpoints
@app.get("/data/status")
async def get_data_status():
    """Get status of data in the database"""
    try:
        tickers_with_data = db_manager.get_tickers_with_data()
        all_tickers = db_manager.get_all_tickers()
        
        return {
            "total_tickers": len(all_tickers),
            "tickers_with_data": len(tickers_with_data),
            "data_coverage": len(tickers_with_data) / len(all_tickers) * 100 if all_tickers else 0,
            "last_updated": "Unknown"  # Could be enhanced to track last update time
        }
        
    except Exception as e:
        logger.error(f"Error getting data status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found", "timestamp": datetime.now().isoformat()}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "timestamp": datetime.now().isoformat()}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
