"""
Main analysis orchestrator that combines all analysis components
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.database.database_manager import DatabaseManager
from analysis.technical_indicators import TechnicalIndicators, calculate_all_indicators
from analysis.seasonality_analysis import SeasonalityAnalyzer, analyze_seasonality
from analysis.predictive_model import StockPredictor, create_predictive_model
import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple
import logging
from datetime import datetime, date, timedelta

logger = logging.getLogger(__name__)

class AnalysisOrchestrator:
    """Orchestrates all analysis components for stock data"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    def get_comprehensive_analysis(self, ticker: str, start_date: date = None, end_date: date = None) -> Dict:
        """
        Get comprehensive analysis for a ticker including technical indicators, seasonality, and predictions
        
        Args:
            ticker: Stock ticker symbol
            start_date: Start date for analysis
            end_date: End date for analysis
            
        Returns:
            Dictionary with complete analysis results
        """
        try:
            logger.info(f"Starting comprehensive analysis for {ticker}")
            
            # Get stock data
            stock_data = self.db_manager.get_stock_data(ticker, start_date, end_date)
            
            if stock_data.empty:
                logger.error(f"No data found for {ticker}")
                return {'error': f'No data found for {ticker}'}
            
            # Perform technical analysis
            technical_analysis = self._perform_technical_analysis(stock_data)
            
            # Perform seasonality analysis
            seasonality_analysis = self._perform_seasonality_analysis(stock_data)
            
            # Perform predictive analysis
            predictive_analysis = self._perform_predictive_analysis(stock_data)
            
            # Combine all analyses
            comprehensive_analysis = {
                'ticker': ticker,
                'analysis_date': datetime.now().isoformat(),
                'data_period': {
                    'start_date': str(stock_data.index.min().date()),
                    'end_date': str(stock_data.index.max().date()),
                    'total_days': len(stock_data)
                },
                'technical_analysis': technical_analysis,
                'seasonality_analysis': seasonality_analysis,
                'predictive_analysis': predictive_analysis,
                'summary': self._generate_analysis_summary(technical_analysis, seasonality_analysis, predictive_analysis)
            }
            
            logger.info(f"Comprehensive analysis completed for {ticker}")
            return comprehensive_analysis
            
        except Exception as e:
            logger.error(f"Error in comprehensive analysis for {ticker}: {e}")
            return {'error': str(e)}
    
    def _perform_technical_analysis(self, data: pd.DataFrame) -> Dict:
        """Perform technical analysis on stock data"""
        try:
            # Calculate all technical indicators
            data_with_indicators = calculate_all_indicators(data)
            
            # Get technical indicators calculator
            tech_calc = TechnicalIndicators(data_with_indicators)
            
            # Get current technical summary
            technical_summary = tech_calc.get_technical_summary()
            
            # Get trend signals
            trend_signals = tech_calc.calculate_trend_signals()
            
            # Get latest trend signal
            latest_trend = {}
            if not trend_signals:
                latest_trend = trend_signals.iloc[-1].to_dict()
            
            return {
                'current_indicators': technical_summary,
                'trend_signals': latest_trend,
                'data_with_indicators': data_with_indicators.tail(50).to_dict('records')  # Last 50 days for charts
            }
            
        except Exception as e:
            logger.error(f"Error in technical analysis: {e}")
            return {'error': str(e)}
    
    def _perform_seasonality_analysis(self, data: pd.DataFrame) -> Dict:
        """Perform seasonality analysis on stock data"""
        try:
            analyzer = SeasonalityAnalyzer(data)
            return analyzer.get_comprehensive_seasonality_report()
            
        except Exception as e:
            logger.error(f"Error in seasonality analysis: {e}")
            return {'error': str(e)}
    
    def _perform_predictive_analysis(self, data: pd.DataFrame) -> Dict:
        """Perform predictive analysis on stock data"""
        try:
            # Only proceed if we have enough data (at least 100 days)
            if len(data) < 100:
                logger.warning("Insufficient data for predictive analysis")
                return {'error': 'Insufficient data for prediction (need at least 100 days)'}
            
            # Create and train predictive model
            predictor = create_predictive_model(data)
            
            # Get next day prediction
            next_day_prediction = predictor.predict_next_day()
            
            # Get feature importance
            feature_importance = predictor.get_feature_importance()
            
            # Perform backtest
            backtest_results = predictor.backtest_model()
            
            return {
                'next_day_prediction': next_day_prediction,
                'feature_importance': feature_importance,
                'backtest_results': backtest_results,
                'model_performance': {
                    'model_name': next_day_prediction.get('model_used', 'unknown'),
                    'features_count': next_day_prediction.get('features_analyzed', 0)
                }
            }
            
        except Exception as e:
            logger.error(f"Error in predictive analysis: {e}")
            return {'error': str(e)}
    
    def _generate_analysis_summary(self, technical_analysis: Dict, seasonality_analysis: Dict, 
                                  predictive_analysis: Dict) -> Dict:
        """Generate overall analysis summary"""
        try:
            summary = {
                'overall_sentiment': 'neutral',
                'confidence_level': 'medium',
                'key_insights': [],
                'recommendations': []
            }
            
            # Analyze technical indicators
            tech_indicators = technical_analysis.get('current_indicators', {})
            if tech_indicators:
                # RSI analysis
                rsi = tech_indicators.get('rsi')
                if rsi:
                    if rsi > 70:
                        summary['key_insights'].append('RSI indicates overbought conditions')
                        summary['recommendations'].append('Consider taking profits')
                    elif rsi < 30:
                        summary['key_insights'].append('RSI indicates oversold conditions')
                        summary['recommendations'].append('Potential buying opportunity')
                
                # Moving average analysis
                price_vs_ma20 = tech_indicators.get('price_vs_ma20', 0)
                if price_vs_ma20 > 0.05:  # 5% above 20-day MA
                    summary['key_insights'].append('Price is significantly above 20-day moving average')
                    summary['overall_sentiment'] = 'bullish'
                elif price_vs_ma20 < -0.05:  # 5% below 20-day MA
                    summary['key_insights'].append('Price is significantly below 20-day moving average')
                    summary['overall_sentiment'] = 'bearish'
            
            # Analyze seasonality
            seasonality_summary = seasonality_analysis.get('summary', {})
            if seasonality_summary:
                best_month = seasonality_summary.get('best_month', {})
                if best_month:
                    current_month = datetime.now().month
                    if current_month == best_month['month']:
                        summary['key_insights'].append(f"Currently in historically best performing month ({best_month['month_name']})")
                        if summary['overall_sentiment'] == 'neutral':
                            summary['overall_sentiment'] = 'bullish'
                
                seasonality_strength = seasonality_summary.get('seasonality_strength', 'none')
                if seasonality_strength == 'strong':
                    summary['key_insights'].append('Strong seasonal patterns detected')
            
            # Analyze predictions
            prediction = predictive_analysis.get('next_day_prediction', {})
            if prediction and 'error' not in prediction:
                pred_value = prediction.get('prediction', 'neutral')
                confidence = prediction.get('confidence', 'medium')
                
                if pred_value == 'bullish' and summary['overall_sentiment'] == 'neutral':
                    summary['overall_sentiment'] = 'bullish'
                elif pred_value == 'bearish' and summary['overall_sentiment'] == 'neutral':
                    summary['overall_sentiment'] = 'bearish'
                
                if confidence == 'high':
                    summary['confidence_level'] = 'high'
                    summary['key_insights'].append(f'High confidence {pred_value} prediction for next day')
                elif confidence == 'low':
                    summary['confidence_level'] = 'low'
            
            # Generate final recommendations
            if summary['overall_sentiment'] == 'bullish':
                if summary['confidence_level'] == 'high':
                    summary['recommendations'].append('Strong buy signal - consider long position')
                else:
                    summary['recommendations'].append('Moderate buy signal - consider small long position')
            elif summary['overall_sentiment'] == 'bearish':
                if summary['confidence_level'] == 'high':
                    summary['recommendations'].append('Strong sell signal - consider reducing position')
                else:
                    summary['recommendations'].append('Moderate sell signal - consider hedging')
            else:
                summary['recommendations'].append('Neutral outlook - hold current position')
            
            # Add disclaimer
            summary['disclaimer'] = 'This analysis is for educational purposes only and should not be considered financial advice'
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating analysis summary: {e}")
            return {'error': str(e)}
    
    def get_trend_analysis(self, ticker: str, period_days: int = 252) -> Dict:
        """Get trend analysis for a specific period"""
        try:
            end_date = date.today()
            start_date = end_date - timedelta(days=period_days)
            
            stock_data = self.db_manager.get_stock_data(ticker, start_date, end_date)
            
            if stock_data.empty:
                return {'error': f'No data found for {ticker}'}
            
            tech_calc = TechnicalIndicators(stock_data)
            technical_summary = tech_calc.get_technical_summary()
            trend_signals = tech_calc.calculate_trend_signals()
            
            # Calculate trend strength
            price_change = (stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0]) / stock_data['Close'].iloc[0]
            volatility = stock_data['Close'].pct_change().std()
            
            return {
                'ticker': ticker,
                'period_days': period_days,
                'price_change_percent': price_change * 100,
                'volatility': volatility,
                'trend_strength': 'strong' if abs(price_change) > 0.2 else 'moderate' if abs(price_change) > 0.1 else 'weak',
                'technical_indicators': technical_summary,
                'trend_signals': trend_signals.iloc[-1].to_dict() if not trend_signals.empty else {}
            }
            
        except Exception as e:
            logger.error(f"Error in trend analysis for {ticker}: {e}")
            return {'error': str(e)}
    
    def get_seasonality_analysis(self, ticker: str) -> Dict:
        """Get seasonality analysis for a ticker"""
        try:
            stock_data = self.db_manager.get_stock_data(ticker)
            
            if stock_data.empty:
                return {'error': f'No data found for {ticker}'}
            
            return analyze_seasonality(stock_data)
            
        except Exception as e:
            logger.error(f"Error in seasonality analysis for {ticker}: {e}")
            return {'error': str(e)}
    
    def get_prediction(self, ticker: str) -> Dict:
        """Get next day prediction for a ticker"""
        try:
            stock_data = self.db_manager.get_stock_data(ticker)
            
            if stock_data.empty:
                return {'error': f'No data found for {ticker}'}
            
            if len(stock_data) < 100:
                return {'error': 'Insufficient data for prediction (need at least 100 days)'}
            
            predictor = create_predictive_model(stock_data)
            return predictor.predict_next_day()
            
        except Exception as e:
            logger.error(f"Error getting prediction for {ticker}: {e}")
            return {'error': str(e)}

# Global analysis orchestrator instance
analysis_orchestrator = AnalysisOrchestrator()
