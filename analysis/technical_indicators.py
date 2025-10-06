"""
Technical indicators and trend analysis functions
"""

import pandas as pd
import numpy as np
import ta
from typing import Dict, Tuple, List
import logging

logger = logging.getLogger(__name__)

class TechnicalIndicators:
    """Calculate various technical indicators for stock analysis"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with stock data
        
        Args:
            data: DataFrame with OHLCV data (Date, Open, High, Low, Close, Volume)
        """
        self.data = data.copy()
        self.calculate_basic_indicators()
    
    def calculate_basic_indicators(self):
        """Calculate basic price indicators"""
        if self.data.empty:
            return
        
        # Price changes
        self.data['Daily_Return'] = self.data['Close'].pct_change()
        self.data['Price_Change'] = self.data['Close'].diff()
        
        # Price ranges
        self.data['High_Low_Range'] = self.data['High'] - self.data['Low']
        self.data['Close_Open_Range'] = self.data['Close'] - self.data['Open']
        
        # Volatility (rolling standard deviation of returns)
        self.data['Volatility_5d'] = self.data['Daily_Return'].rolling(window=5).std()
        self.data['Volatility_20d'] = self.data['Daily_Return'].rolling(window=20).std()
    
    def calculate_moving_averages(self, periods: List[int] = [5, 10, 20, 50, 200]) -> pd.DataFrame:
        """
        Calculate moving averages for specified periods
        
        Args:
            periods: List of periods for moving averages
            
        Returns:
            DataFrame with moving averages
        """
        result = self.data.copy()
        
        for period in periods:
            if period <= len(self.data):
                result[f'MA_{period}'] = self.data['Close'].rolling(window=period).mean()
                result[f'EMA_{period}'] = self.data['Close'].ewm(span=period).mean()
        
        return result
    
    def calculate_rsi(self, period: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index (RSI)
        
        Args:
            period: RSI calculation period
            
        Returns:
            Series with RSI values
        """
        return ta.momentum.RSIIndicator(self.data['Close'], window=period).rsi()
    
    def calculate_macd(self, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, pd.Series]:
        """
        Calculate MACD (Moving Average Convergence Divergence)
        
        Args:
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line EMA period
            
        Returns:
            Dictionary with MACD, signal, and histogram
        """
        macd_indicator = ta.trend.MACD(self.data['Close'], window_fast=fast, window_slow=slow, window_sign=signal)
        
        return {
            'macd': macd_indicator.macd(),
            'macd_signal': macd_indicator.macd_signal(),
            'macd_histogram': macd_indicator.macd_diff()
        }
    
    def calculate_bollinger_bands(self, period: int = 20, std_dev: float = 2) -> Dict[str, pd.Series]:
        """
        Calculate Bollinger Bands
        
        Args:
            period: Moving average period
            std_dev: Standard deviation multiplier
            
        Returns:
            Dictionary with upper, middle, and lower bands
        """
        bb_indicator = ta.volatility.BollingerBands(self.data['Close'], window=period, window_dev=std_dev)
        
        return {
            'bb_upper': bb_indicator.bollinger_hband(),
            'bb_middle': bb_indicator.bollinger_mavg(),
            'bb_lower': bb_indicator.bollinger_lband()
        }
    
    def calculate_stochastic(self, k_period: int = 14, d_period: int = 3) -> Dict[str, pd.Series]:
        """
        Calculate Stochastic Oscillator
        
        Args:
            k_period: %K calculation period
            d_period: %D smoothing period
            
        Returns:
            Dictionary with %K and %D values
        """
        stoch_indicator = ta.momentum.StochasticOscillator(
            self.data['High'], self.data['Low'], self.data['Close'],
            window=k_period, smooth_window=d_period
        )
        
        return {
            'stoch_k': stoch_indicator.stoch(),
            'stoch_d': stoch_indicator.stoch_signal()
        }
    
    def calculate_volume_indicators(self) -> Dict[str, pd.Series]:
        """
        Calculate volume-based indicators
        
        Returns:
            Dictionary with volume indicators
        """
        # On-Balance Volume (OBV)
        obv = ta.volume.OnBalanceVolumeIndicator(self.data['Close'], self.data['Volume']).on_balance_volume()
        
        # Volume Rate of Change
        volume_roc = self.data['Volume'].pct_change(periods=10)
        
        # Volume Moving Average
        volume_ma = self.data['Volume'].rolling(window=20).mean()
        
        # Price-Volume Trend
        pvt = ta.volume.VolumePriceTrendIndicator(self.data['Close'], self.data['Volume']).volume_price_trend()
        
        return {
            'obv': obv,
            'volume_roc': volume_roc,
            'volume_ma': volume_ma,
            'pvt': pvt
        }
    
    def calculate_trend_signals(self) -> Dict[str, pd.Series]:
        """
        Calculate trend signals based on multiple indicators
        
        Returns:
            Dictionary with trend signals
        """
        signals = {}
        
        # Moving average signals
        ma_20 = self.data['Close'].rolling(window=20).mean()
        ma_50 = self.data['Close'].rolling(window=50).mean()
        ma_200 = self.data['Close'].rolling(window=200).mean()
        
        # Trend direction signals
        signals['ma_trend_short'] = np.where(self.data['Close'] > ma_20, 1, -1)  # Short-term trend
        signals['ma_trend_medium'] = np.where(ma_20 > ma_50, 1, -1)  # Medium-term trend
        signals['ma_trend_long'] = np.where(ma_50 > ma_200, 1, -1)  # Long-term trend
        
        # Overall trend score (average of all trend signals)
        trend_signals = pd.DataFrame(signals)
        signals['overall_trend'] = trend_signals.mean(axis=1)
        
        # RSI signals
        rsi = self.calculate_rsi()
        signals['rsi_oversold'] = np.where(rsi < 30, 1, 0)  # Oversold
        signals['rsi_overbought'] = np.where(rsi > 70, 1, 0)  # Overbought
        
        # MACD signals
        macd_data = self.calculate_macd()
        signals['macd_bullish'] = np.where(
            (macd_data['macd'] > macd_data['macd_signal']) & 
            (macd_data['macd'].shift(1) <= macd_data['macd_signal'].shift(1)), 1, 0
        )  # MACD bullish crossover
        
        signals['macd_bearish'] = np.where(
            (macd_data['macd'] < macd_data['macd_signal']) & 
            (macd_data['macd'].shift(1) >= macd_data['macd_signal'].shift(1)), 1, 0
        )  # MACD bearish crossover
        
        # Convert to pandas Series
        for key, value in signals.items():
            signals[key] = pd.Series(value, index=self.data.index)
        
        return signals
    
    def get_technical_summary(self) -> Dict:
        """
        Get a summary of current technical indicators
        
        Returns:
            Dictionary with current technical indicator values
        """
        if self.data.empty:
            return {}
        
        latest_data = self.data.iloc[-1]
        
        # Calculate indicators
        rsi = self.calculate_rsi()
        macd_data = self.calculate_macd()
        bb_data = self.calculate_bollinger_bands()
        stoch_data = self.calculate_stochastic()
        volume_data = self.calculate_volume_indicators()
        
        # Moving averages
        ma_20 = self.data['Close'].rolling(window=20).mean().iloc[-1]
        ma_50 = self.data['Close'].rolling(window=50).mean().iloc[-1]
        ma_200 = self.data['Close'].rolling(window=200).mean().iloc[-1]
        
        summary = {
            'current_price': latest_data['Close'],
            'daily_return': latest_data.get('Daily_Return', 0),
            'volatility_20d': latest_data.get('Volatility_20d', 0),
            
            # Moving averages
            'ma_20': ma_20,
            'ma_50': ma_50,
            'ma_200': ma_200,
            'price_vs_ma20': (latest_data['Close'] - ma_20) / ma_20 * 100,
            'price_vs_ma50': (latest_data['Close'] - ma_50) / ma_50 * 100,
            'price_vs_ma200': (latest_data['Close'] - ma_200) / ma_200 * 100,
            
            # Technical indicators
            'rsi': rsi.iloc[-1] if not rsi.empty else None,
            'macd': macd_data['macd'].iloc[-1] if not macd_data['macd'].empty else None,
            'macd_signal': macd_data['macd_signal'].iloc[-1] if not macd_data['macd_signal'].empty else None,
            'bb_upper': bb_data['bb_upper'].iloc[-1] if not bb_data['bb_upper'].empty else None,
            'bb_lower': bb_data['bb_lower'].iloc[-1] if not bb_data['bb_lower'].empty else None,
            'stoch_k': stoch_data['stoch_k'].iloc[-1] if not stoch_data['stoch_k'].empty else None,
            'stoch_d': stoch_data['stoch_d'].iloc[-1] if not stoch_data['stoch_d'].empty else None,
            
            # Volume
            'volume': latest_data['Volume'],
            'volume_ma': volume_data['volume_ma'].iloc[-1] if not volume_data['volume_ma'].empty else None,
            'obv': volume_data['obv'].iloc[-1] if not volume_data['obv'].empty else None,
        }
        
        return summary

def calculate_all_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate all technical indicators for a stock dataset
    
    Args:
        data: DataFrame with OHLCV data
        
    Returns:
        DataFrame with all technical indicators
    """
    if data.empty:
        return data
    
    indicator_calc = TechnicalIndicators(data)
    
    # Get data with moving averages
    result = indicator_calc.calculate_moving_averages()
    
    # Add RSI
    result['RSI'] = indicator_calc.calculate_rsi()
    
    # Add MACD
    macd_data = indicator_calc.calculate_macd()
    result['MACD'] = macd_data['macd']
    result['MACD_Signal'] = macd_data['macd_signal']
    result['MACD_Histogram'] = macd_data['macd_histogram']
    
    # Add Bollinger Bands
    bb_data = indicator_calc.calculate_bollinger_bands()
    result['BB_Upper'] = bb_data['bb_upper']
    result['BB_Middle'] = bb_data['bb_middle']
    result['BB_Lower'] = bb_data['bb_lower']
    
    # Add Stochastic
    stoch_data = indicator_calc.calculate_stochastic()
    result['Stoch_K'] = stoch_data['stoch_k']
    result['Stoch_D'] = stoch_data['stoch_d']
    
    # Add volume indicators
    volume_data = indicator_calc.calculate_volume_indicators()
    result['OBV'] = volume_data['obv']
    result['Volume_MA'] = volume_data['volume_ma']
    result['PVT'] = volume_data['pvt']
    
    # Add trend signals
    trend_signals = indicator_calc.calculate_trend_signals()
    for signal_name, signal_data in trend_signals.items():
        result[f'Trend_{signal_name.title()}'] = signal_data
    
    return result
