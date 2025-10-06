"""
Predictive model for stock price direction prediction
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from typing import Dict, Tuple, List
import logging
import warnings
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class StockPredictor:
    """Predictive model for stock price direction"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize predictor with stock data
        
        Args:
            data: DataFrame with OHLCV data and technical indicators
        """
        self.data = data.copy()
        self.models = {}
        self.feature_importance = {}
        self.scaler = StandardScaler()
        self.prepare_features()
    
    def prepare_features(self):
        """Prepare features for prediction model"""
        if self.data.empty:
            return
        
        # Calculate target variable (next day direction)
        self.data['Next_Day_Return'] = self.data['Close'].shift(-1) / self.data['Close'] - 1
        self.data['Next_Day_Direction'] = (self.data['Next_Day_Return'] > 0).astype(int)
        
        # Technical indicators as features
        self.data['MA_5'] = self.data['Close'].rolling(5).mean()
        self.data['MA_10'] = self.data['Close'].rolling(10).mean()
        self.data['MA_20'] = self.data['Close'].rolling(20).mean()
        self.data['MA_50'] = self.data['Close'].rolling(50).mean()
        
        # Price momentum features
        self.data['Price_vs_MA5'] = (self.data['Close'] - self.data['MA_5']) / self.data['MA_5']
        self.data['Price_vs_MA20'] = (self.data['Close'] - self.data['MA_20']) / self.data['MA_20']
        self.data['Price_vs_MA50'] = (self.data['Close'] - self.data['MA_50']) / self.data['MA_50']
        
        # Volatility features
        self.data['Volatility_5d'] = self.data['Close'].rolling(5).std()
        self.data['Volatility_20d'] = self.data['Close'].rolling(20).std()
        self.data['Volatility_Ratio'] = self.data['Volatility_5d'] / self.data['Volatility_20d']
        
        # Volume features
        self.data['Volume_MA'] = self.data['Volume'].rolling(20).mean()
        self.data['Volume_Ratio'] = self.data['Volume'] / self.data['Volume_MA']
        
        # Price action features
        self.data['High_Low_Range'] = (self.data['High'] - self.data['Low']) / self.data['Close']
        self.data['Close_Open_Range'] = (self.data['Close'] - self.data['Open']) / self.data['Open']
        
        # Momentum features
        self.data['Momentum_5d'] = self.data['Close'] / self.data['Close'].shift(5) - 1
        self.data['Momentum_10d'] = self.data['Close'] / self.data['Close'].shift(10) - 1
        
        # RSI-like feature
        price_changes = self.data['Close'].diff()
        gains = price_changes.where(price_changes > 0, 0).rolling(14).mean()
        losses = (-price_changes.where(price_changes < 0, 0)).rolling(14).mean()
        rs = gains / losses
        self.data['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD features
        ema_12 = self.data['Close'].ewm(span=12).mean()
        ema_26 = self.data['Close'].ewm(span=26).mean()
        self.data['MACD'] = ema_12 - ema_26
        self.data['MACD_Signal'] = self.data['MACD'].ewm(span=9).mean()
        self.data['MACD_Histogram'] = self.data['MACD'] - self.data['MACD_Signal']
        
        # Bollinger Bands features
        bb_middle = self.data['Close'].rolling(20).mean()
        bb_std = self.data['Close'].rolling(20).std()
        self.data['BB_Upper'] = bb_middle + (bb_std * 2)
        self.data['BB_Lower'] = bb_middle - (bb_std * 2)
        self.data['BB_Position'] = (self.data['Close'] - self.data['BB_Lower']) / (self.data['BB_Upper'] - self.data['BB_Lower'])
        
        # Seasonal features
        self.data['Month'] = self.data.index.month
        self.data['Quarter'] = self.data.index.quarter
        self.data['DayOfWeek'] = self.data.index.dayofweek
        
        # Lagged features
        for lag in [1, 2, 3, 5]:
            self.data[f'Return_Lag_{lag}'] = self.data['Close'].pct_change(lag)
            self.data[f'Volume_Lag_{lag}'] = self.data['Volume'].shift(lag) / self.data['Volume_MA']
    
    def get_feature_columns(self) -> List[str]:
        """Get list of feature columns for model training"""
        feature_cols = [
            'Price_vs_MA5', 'Price_vs_MA20', 'Price_vs_MA50',
            'Volatility_Ratio', 'Volume_Ratio', 'High_Low_Range',
            'Close_Open_Range', 'Momentum_5d', 'Momentum_10d',
            'RSI', 'MACD', 'MACD_Signal', 'MACD_Histogram',
            'BB_Position', 'Month', 'Quarter', 'DayOfWeek'
        ]
        
        # Add lagged features
        for lag in [1, 2, 3, 5]:
            feature_cols.extend([f'Return_Lag_{lag}', f'Volume_Lag_{lag}'])
        
        return feature_cols
    
    def prepare_training_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare training data with features and targets"""
        feature_cols = self.get_feature_columns()
        
        # Remove rows with NaN values
        clean_data = self.data[feature_cols + ['Next_Day_Direction']].dropna()
        
        if clean_data.empty:
            logger.warning("No clean data available for training")
            return np.array([]), np.array([])
        
        X = clean_data[feature_cols].values
        y = clean_data['Next_Day_Direction'].values
        
        return X, y
    
    def train_models(self, test_size: float = 0.2, random_state: int = 42):
        """Train multiple prediction models"""
        X, y = self.prepare_training_data()
        
        if X.size == 0:
            logger.error("No training data available")
            return
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Define models
        models = {
            'random_forest': RandomForestClassifier(
                n_estimators=100, 
                max_depth=10, 
                random_state=random_state,
                class_weight='balanced'
            ),
            'gradient_boosting': GradientBoostingClassifier(
                n_estimators=100,
                max_depth=6,
                random_state=random_state
            ),
            'logistic_regression': LogisticRegression(
                random_state=random_state,
                class_weight='balanced',
                max_iter=1000
            )
        }
        
        # Train models
        model_scores = {}
        for name, model in models.items():
            try:
                if name == 'logistic_regression':
                    model.fit(X_train_scaled, y_train)
                    y_pred = model.predict(X_test_scaled)
                    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
                else:
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)
                    y_pred_proba = model.predict_proba(X_test)[:, 1]
                
                accuracy = accuracy_score(y_test, y_pred)
                model_scores[name] = accuracy
                
                self.models[name] = model
                
                # Store feature importance for tree-based models
                if hasattr(model, 'feature_importances_'):
                    feature_names = self.get_feature_columns()
                    importance_dict = dict(zip(feature_names, model.feature_importances_))
                    self.feature_importance[name] = importance_dict
                
                logger.info(f"{name} accuracy: {accuracy:.4f}")
                
            except Exception as e:
                logger.error(f"Error training {name}: {e}")
        
        # Select best model
        if model_scores:
            best_model_name = max(model_scores, key=model_scores.get)
            self.best_model = self.models[best_model_name]
            self.best_model_name = best_model_name
            logger.info(f"Best model: {best_model_name} with accuracy: {model_scores[best_model_name]:.4f}")
    
    def predict_next_day(self) -> Dict:
        """Predict next day stock direction"""
        if not hasattr(self, 'best_model') or self.best_model is None:
            logger.error("No trained model available")
            return {'prediction': 'neutral', 'probability': 0.5, 'confidence': 'low'}
        
        # Get latest data
        latest_data = self.data.iloc[-1:]
        feature_cols = self.get_feature_columns()
        
        # Prepare features
        X_latest = latest_data[feature_cols].values
        
        if np.isnan(X_latest).any():
            logger.warning("Latest data contains NaN values, cannot make prediction")
            return {'prediction': 'neutral', 'probability': 0.5, 'confidence': 'low'}
        
        try:
            # Make prediction
            if self.best_model_name == 'logistic_regression':
                X_latest_scaled = self.scaler.transform(X_latest)
                probability = self.best_model.predict_proba(X_latest_scaled)[0, 1]
            else:
                probability = self.best_model.predict_proba(X_latest)[0, 1]
            
            # Determine prediction and confidence
            if probability > 0.6:
                prediction = 'bullish'
                confidence = 'high' if probability > 0.75 else 'medium'
            elif probability < 0.4:
                prediction = 'bearish'
                confidence = 'high' if probability < 0.25 else 'medium'
            else:
                prediction = 'neutral'
                confidence = 'medium' if abs(probability - 0.5) > 0.05 else 'low'
            
            return {
                'prediction': prediction,
                'probability': probability,
                'confidence': confidence,
                'model_used': self.best_model_name,
                'features_analyzed': len(feature_cols)
            }
            
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            return {'prediction': 'neutral', 'probability': 0.5, 'confidence': 'low'}
    
    def get_feature_importance(self, model_name: str = None) -> Dict:
        """Get feature importance from trained models"""
        if model_name and model_name in self.feature_importance:
            return self.feature_importance[model_name]
        elif hasattr(self, 'best_model_name') and self.best_model_name in self.feature_importance:
            return self.feature_importance[self.best_model_name]
        else:
            return {}
    
    def backtest_model(self, days_back: int = 252) -> Dict:
        """Backtest the model on historical data"""
        if not hasattr(self, 'best_model') or self.best_model is None:
            logger.error("No trained model available for backtesting")
            return {}
        
        # Get recent data for backtesting
        backtest_data = self.data.tail(days_back)
        feature_cols = self.get_feature_columns()
        
        predictions = []
        actuals = []
        probabilities = []
        
        for i in range(1, len(backtest_data)):
            try:
                # Get features for prediction
                X = backtest_data.iloc[i-1:i][feature_cols].values
                
                if np.isnan(X).any():
                    continue
                
                # Make prediction
                if self.best_model_name == 'logistic_regression':
                    X_scaled = self.scaler.transform(X)
                    prob = self.best_model.predict_proba(X_scaled)[0, 1]
                    pred = self.best_model.predict(X_scaled)[0]
                else:
                    prob = self.best_model.predict_proba(X)[0, 1]
                    pred = self.best_model.predict(X)[0]
                
                # Get actual result
                actual = backtest_data.iloc[i]['Next_Day_Direction']
                
                predictions.append(pred)
                actuals.append(actual)
                probabilities.append(prob)
                
            except Exception as e:
                logger.warning(f"Error in backtest iteration {i}: {e}")
                continue
        
        if not predictions:
            return {}
        
        # Calculate backtest metrics
        accuracy = accuracy_score(actuals, predictions)
        
        # Calculate strategy returns
        strategy_returns = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            if i < len(actuals):
                actual_return = backtest_data.iloc[i+1]['Close'] / backtest_data.iloc[i]['Close'] - 1
                # Simple strategy: go long if prediction is bullish with high confidence
                if pred == 1 and prob > 0.6:
                    strategy_returns.append(actual_return)
                elif pred == 0 and prob < 0.4:
                    strategy_returns.append(-actual_return)  # Short position
                else:
                    strategy_returns.append(0)  # No position
        
        total_return = sum(strategy_returns)
        win_rate = sum(1 for r in strategy_returns if r > 0) / len(strategy_returns) if strategy_returns else 0
        
        return {
            'accuracy': accuracy,
            'total_return': total_return,
            'win_rate': win_rate,
            'total_trades': len(predictions),
            'avg_probability': np.mean(probabilities),
            'strategy_returns': strategy_returns
        }

def create_predictive_model(data: pd.DataFrame) -> StockPredictor:
    """
    Convenience function to create and train a predictive model
    
    Args:
        data: DataFrame with OHLCV data
        
    Returns:
        Trained StockPredictor instance
    """
    predictor = StockPredictor(data)
    predictor.train_models()
    return predictor
