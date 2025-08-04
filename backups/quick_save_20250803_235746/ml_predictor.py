import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

class StockPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def prepare_features(self, data):
        """Prepare features for prediction"""
        features = pd.DataFrame()
        
        # Price-based features
        features['price_change'] = data['Close'].pct_change()
        features['price_volatility'] = features['price_change'].rolling(20).std()
        features['price_momentum'] = data['Close'] / data['Close'].shift(20) - 1
        
        # Volume features
        features['volume_change'] = data['Volume'].pct_change()
        features['volume_ma'] = data['Volume'].rolling(20).mean()
        
        # Technical indicators
        features['rsi'] = self.calculate_rsi(data['Close'])
        features['ma_ratio'] = data['Close'] / data['Close'].rolling(50).mean()
        
        # Remove NaN values
        features = features.dropna()
        
        return features
    
    def calculate_rsi(self, prices, period=14):
        """Calculate RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def train(self, data, target_days=5):
        """Train the model"""
        features = self.prepare_features(data)
        
        # Create target (future price change)
        target = data['Close'].shift(-target_days) / data['Close'] - 1
        target = target[features.index]
        
        # Align features and target
        common_index = features.index.intersection(target.index)
        features = features.loc[common_index]
        target = target.loc[common_index]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            features, target, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)
        
        print(f"Training R² Score: {train_score:.4f}")
        print(f"Testing R² Score: {test_score:.4f}")
        
        self.is_trained = True
        return train_score, test_score
    
    def predict(self, data):
        """Make predictions"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        features = self.prepare_features(data)
        if features.empty:
            return None
        
        # Use latest data point
        latest_features = features.iloc[-1:].values
        latest_features_scaled = self.scaler.transform(latest_features)
        
        prediction = self.model.predict(latest_features_scaled)[0]
        return prediction 