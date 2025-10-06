"""
Seasonality analysis functions for stock data
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging
from datetime import datetime
import calendar

logger = logging.getLogger(__name__)

class SeasonalityAnalyzer:
    """Analyze seasonal patterns in stock data"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with stock data
        
        Args:
            data: DataFrame with OHLCV data (Date, Open, High, Low, Close, Volume)
        """
        self.data = data.copy()
        if not self.data.empty:
            self.data.index = pd.to_datetime(self.data.index)
            self.prepare_data()
    
    def prepare_data(self):
        """Prepare data for seasonality analysis"""
        if self.data.empty:
            return
        
        # Calculate daily returns
        self.data['Daily_Return'] = self.data['Close'].pct_change()
        
        # Calculate monthly returns
        self.data['Monthly_Return'] = self.data['Close'].resample('M').last().pct_change()
        
        # Calculate quarterly returns
        self.data['Quarterly_Return'] = self.data['Close'].resample('Q').last().pct_change()
        
        # Add time-based features
        self.data['Year'] = self.data.index.year
        self.data['Month'] = self.data.index.month
        self.data['Quarter'] = self.data.index.quarter
        self.data['DayOfWeek'] = self.data.index.dayofweek
        self.data['DayOfMonth'] = self.data.index.day
        self.data['WeekOfYear'] = self.data.index.isocalendar().week
    
    def analyze_monthly_seasonality(self) -> Dict:
        """
        Analyze monthly seasonality patterns
        
        Returns:
            Dictionary with monthly statistics
        """
        if self.data.empty:
            return {}
        
        monthly_stats = {}
        
        for month in range(1, 13):
            month_data = self.data[self.data['Month'] == month]
            
            if not month_data.empty:
                monthly_stats[month] = {
                    'month_name': calendar.month_name[month],
                    'avg_return': month_data['Daily_Return'].mean(),
                    'median_return': month_data['Daily_Return'].median(),
                    'std_return': month_data['Daily_Return'].std(),
                    'positive_days': (month_data['Daily_Return'] > 0).sum(),
                    'total_days': len(month_data),
                    'win_rate': (month_data['Daily_Return'] > 0).mean(),
                    'avg_volume': month_data['Volume'].mean(),
                    'avg_price_change': month_data['Close'].pct_change().mean()
                }
        
        return monthly_stats
    
    def analyze_quarterly_seasonality(self) -> Dict:
        """
        Analyze quarterly seasonality patterns
        
        Returns:
            Dictionary with quarterly statistics
        """
        if self.data.empty:
            return {}
        
        quarterly_stats = {}
        quarter_names = {1: 'Q1 (Jan-Mar)', 2: 'Q2 (Apr-Jun)', 3: 'Q3 (Jul-Sep)', 4: 'Q4 (Oct-Dec)'}
        
        for quarter in range(1, 5):
            quarter_data = self.data[self.data['Quarter'] == quarter]
            
            if not quarter_data.empty:
                quarterly_stats[quarter] = {
                    'quarter_name': quarter_names[quarter],
                    'avg_return': quarter_data['Daily_Return'].mean(),
                    'median_return': quarter_data['Daily_Return'].median(),
                    'std_return': quarter_data['Daily_Return'].std(),
                    'positive_days': (quarter_data['Daily_Return'] > 0).sum(),
                    'total_days': len(quarter_data),
                    'win_rate': (quarter_data['Daily_Return'] > 0).mean(),
                    'avg_volume': quarter_data['Volume'].mean(),
                    'total_return': quarter_data['Close'].iloc[-1] / quarter_data['Close'].iloc[0] - 1 if len(quarter_data) > 1 else 0
                }
        
        return quarterly_stats
    
    def analyze_dow_seasonality(self) -> Dict:
        """
        Analyze day-of-week seasonality patterns
        
        Returns:
            Dictionary with day-of-week statistics
        """
        if self.data.empty:
            return {}
        
        dow_stats = {}
        dow_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday'}
        
        for dow in range(5):  # Monday to Friday only
            dow_data = self.data[self.data['DayOfWeek'] == dow]
            
            if not dow_data.empty:
                dow_stats[dow] = {
                    'day_name': dow_names[dow],
                    'avg_return': dow_data['Daily_Return'].mean(),
                    'median_return': dow_data['Daily_Return'].median(),
                    'std_return': dow_data['Daily_Return'].std(),
                    'positive_days': (dow_data['Daily_Return'] > 0).sum(),
                    'total_days': len(dow_data),
                    'win_rate': (dow_data['Daily_Return'] > 0).mean(),
                    'avg_volume': dow_data['Volume'].mean()
                }
        
        return dow_stats
    
    def analyze_month_end_effect(self) -> Dict:
        """
        Analyze month-end effect (last few days of month vs other days)
        
        Returns:
            Dictionary with month-end statistics
        """
        if self.data.empty:
            return {}
        
        # Define month-end days (last 3 days of month)
        month_end_days = []
        other_days = []
        
        for date, row in self.data.iterrows():
            # Handle both datetime and date objects
            if hasattr(date, 'year') and hasattr(date, 'month') and hasattr(date, 'day'):
                year, month, day = date.year, date.month, date.day
            else:
                # If it's a string or other format, try to parse it
                try:
                    parsed_date = pd.to_datetime(date)
                    year, month, day = parsed_date.year, parsed_date.month, parsed_date.day
                except:
                    continue
            
            last_day_of_month = calendar.monthrange(year, month)[1]
            if day >= last_day_of_month - 2:  # Last 3 days
                month_end_days.append(row['Daily_Return'])
            else:
                other_days.append(row['Daily_Return'])
        
        month_end_returns = pd.Series(month_end_days).dropna()
        other_returns = pd.Series(other_days).dropna()
        
        return {
            'month_end': {
                'avg_return': month_end_returns.mean(),
                'median_return': month_end_returns.median(),
                'std_return': month_end_returns.std(),
                'positive_days': (month_end_returns > 0).sum(),
                'total_days': len(month_end_returns),
                'win_rate': (month_end_returns > 0).mean()
            },
            'other_days': {
                'avg_return': other_returns.mean(),
                'median_return': other_returns.median(),
                'std_return': other_returns.std(),
                'positive_days': (other_returns > 0).sum(),
                'total_days': len(other_returns),
                'win_rate': (other_returns > 0).mean()
            }
        }
    
    def create_seasonality_heatmap_data(self, period_type: str = 'monthly') -> pd.DataFrame:
        """
        Create data for seasonality heatmap visualization
        
        Args:
            period_type: 'monthly' or 'quarterly'
            
        Returns:
            DataFrame suitable for heatmap visualization
        """
        if self.data.empty:
            return pd.DataFrame()
        
        if period_type == 'monthly':
            # Group by year and month
            grouped = self.data.groupby([self.data.index.year, self.data.index.month])['Daily_Return'].mean()
            heatmap_data = grouped.unstack(level=1)
            heatmap_data.columns = [calendar.month_name[i] for i in heatmap_data.columns]
        
        elif period_type == 'quarterly':
            # Group by year and quarter
            grouped = self.data.groupby([self.data.index.year, self.data.index.quarter])['Daily_Return'].mean()
            heatmap_data = grouped.unstack(level=1)
            heatmap_data.columns = [f'Q{i}' for i in heatmap_data.columns]
        
        else:
            raise ValueError("period_type must be 'monthly' or 'quarterly'")
        
        return heatmap_data
    
    def get_seasonal_forecast(self, target_month: int, target_quarter: int = None) -> Dict:
        """
        Generate seasonal forecast based on historical patterns
        
        Args:
            target_month: Target month (1-12)
            target_quarter: Target quarter (1-4), optional
            
        Returns:
            Dictionary with seasonal forecast
        """
        if self.data.empty:
            return {}
        
        monthly_stats = self.analyze_monthly_seasonality()
        quarterly_stats = self.analyze_quarterly_seasonality()
        
        forecast = {
            'month_forecast': monthly_stats.get(target_month, {}),
            'quarter_forecast': quarterly_stats.get(target_quarter, {}) if target_quarter else {},
            'recommendation': 'neutral',
            'confidence': 'low'
        }
        
        # Generate recommendation based on historical performance
        if target_month in monthly_stats:
            month_data = monthly_stats[target_month]
            avg_return = month_data['avg_return']
            win_rate = month_data['win_rate']
            
            if avg_return > 0.001 and win_rate > 0.55:  # >0.1% avg return and >55% win rate
                forecast['recommendation'] = 'bullish'
                forecast['confidence'] = 'high' if win_rate > 0.6 else 'medium'
            elif avg_return < -0.001 and win_rate < 0.45:  # <-0.1% avg return and <45% win rate
                forecast['recommendation'] = 'bearish'
                forecast['confidence'] = 'high' if win_rate < 0.4 else 'medium'
            else:
                forecast['recommendation'] = 'neutral'
                forecast['confidence'] = 'medium' if abs(avg_return) > 0.0005 else 'low'
        
        return forecast
    
    def get_comprehensive_seasonality_report(self) -> Dict:
        """
        Get comprehensive seasonality analysis report
        
        Returns:
            Dictionary with all seasonality analyses
        """
        if self.data.empty:
            return {}
        
        return {
            'monthly_patterns': self.analyze_monthly_seasonality(),
            'quarterly_patterns': self.analyze_quarterly_seasonality(),
            'dow_patterns': self.analyze_dow_seasonality(),
            'month_end_effect': self.analyze_month_end_effect(),
            'heatmap_data_monthly': self.create_seasonality_heatmap_data('monthly'),
            'heatmap_data_quarterly': self.create_seasonality_heatmap_data('quarterly'),
            'summary': self._generate_seasonality_summary()
        }
    
    def _generate_seasonality_summary(self) -> Dict:
        """Generate summary of seasonality patterns"""
        monthly_stats = self.analyze_monthly_seasonality()
        quarterly_stats = self.analyze_quarterly_seasonality()
        
        if not monthly_stats or not quarterly_stats:
            return {}
        
        # Find best and worst performing months
        month_returns = {month: stats['avg_return'] for month, stats in monthly_stats.items()}
        best_month = max(month_returns, key=month_returns.get)
        worst_month = min(month_returns, key=month_returns.get)
        
        # Find best and worst performing quarters
        quarter_returns = {quarter: stats['avg_return'] for quarter, stats in quarterly_stats.items()}
        best_quarter = max(quarter_returns, key=quarter_returns.get)
        worst_quarter = min(quarter_returns, key=quarter_returns.get)
        
        return {
            'best_month': {
                'month': best_month,
                'month_name': calendar.month_name[best_month],
                'avg_return': month_returns[best_month]
            },
            'worst_month': {
                'month': worst_month,
                'month_name': calendar.month_name[worst_month],
                'avg_return': month_returns[worst_month]
            },
            'best_quarter': {
                'quarter': best_quarter,
                'quarter_name': f'Q{best_quarter}',
                'avg_return': quarter_returns[best_quarter]
            },
            'worst_quarter': {
                'quarter': worst_quarter,
                'quarter_name': f'Q{worst_quarter}',
                'avg_return': quarter_returns[worst_quarter]
            },
            'seasonality_strength': self._calculate_seasonality_strength(monthly_stats)
        }
    
    def _calculate_seasonality_strength(self, monthly_stats: Dict) -> str:
        """Calculate how strong the seasonality patterns are"""
        if not monthly_stats:
            return 'none'
        
        returns = [stats['avg_return'] for stats in monthly_stats.values()]
        std_dev = np.std(returns)
        
        if std_dev > 0.005:  # >0.5% standard deviation
            return 'strong'
        elif std_dev > 0.002:  # >0.2% standard deviation
            return 'moderate'
        elif std_dev > 0.001:  # >0.1% standard deviation
            return 'weak'
        else:
            return 'none'

def analyze_seasonality(data: pd.DataFrame) -> Dict:
    """
    Convenience function to analyze seasonality for stock data
    
    Args:
        data: DataFrame with OHLCV data
        
    Returns:
        Dictionary with comprehensive seasonality analysis
    """
    analyzer = SeasonalityAnalyzer(data)
    return analyzer.get_comprehensive_seasonality_report()
