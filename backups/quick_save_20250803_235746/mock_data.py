#!/usr/bin/env python3
"""
Mock Data Provider with Realistic Current Prices
"""

import random
import time
from datetime import datetime, timedelta
from typing import Dict, Optional
import pandas as pd

class MockDataProvider:
    """Provides realistic mock market data when APIs are rate limited"""
    
    def __init__(self):
        # Realistic base prices (as of recent market data)
        self.base_prices = {
            "AAPL": 175.50,
            "MSFT": 380.25,
            "GOOGL": 140.75,
            "TSLA": 245.80,
            "NVDA": 850.20,
            "META": 485.90,
            "SPY": 520.45,
            "HOOD": 18.75,
            "PLTR": 22.30,
            "AMZN": 155.60,
            "NFLX": 580.40,
            "AMD": 125.30,
            "INTC": 32.15,
            "ORCL": 125.80,
            "CRM": 245.60
        }
        
        # Market volatility (percentage)
        self.volatility = 0.02  # 2% volatility
        
    def get_realistic_price(self, symbol: str) -> float:
        """Generate a realistic price for a symbol"""
        base_price = self.base_prices.get(symbol, 100.0)
        
        # Add some realistic movement
        movement = random.gauss(0, self.volatility)
        new_price = base_price * (1 + movement)
        
        # Update base price for next call
        self.base_prices[symbol] = new_price
        
        return round(new_price, 2)
    
    def get_mock_quote(self, symbol: str) -> Dict:
        """Get a realistic mock quote"""
        current_price = self.get_realistic_price(symbol)
        previous_close = self.base_prices.get(symbol, current_price) * 0.995  # Slight difference
        
        change = current_price - previous_close
        change_percent = (change / previous_close) * 100
        
        volume = random.randint(1000000, 10000000)
        
        return {
            "symbol": symbol,
            "price": current_price,
            "previous_close": round(previous_close, 2),
            "change": round(change, 2),
            "change_percent": round(change_percent, 2),
            "volume": volume,
            "avg_volume": volume * random.uniform(0.8, 1.2),
            "market_cap": current_price * random.randint(1000000, 10000000),
            "pe_ratio": random.uniform(15, 35),
            "data_source": "mock_data",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_mock_stock_data(self, symbol: str, interval: str = "1m", period: str = "1d") -> pd.DataFrame:
        """Generate realistic historical stock data"""
        current_price = self.get_realistic_price(symbol)
        
        # Generate data points
        if period == "1d":
            data_points = 390  # Market hours in minutes
        elif period == "1w":
            data_points = 1950  # 5 days * 390 minutes
        elif period == "1m":
            data_points = 7800  # ~20 trading days * 390 minutes
        else:
            data_points = 390
        
        # Generate time series
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=data_points)
        
        # Create time index
        time_index = pd.date_range(start=start_time, end=end_time, periods=data_points)
        
        # Generate price data with realistic movement
        prices = []
        current = current_price
        
        for i in range(data_points):
            # Add some trend and noise
            trend = random.gauss(0, 0.001)  # Small trend
            noise = random.gauss(0, 0.005)  # Price noise
            current = current * (1 + trend + noise)
            prices.append(current)
        
        # Create OHLC data
        data = []
        for i in range(0, len(prices), 5):  # 5-minute candles
            if i + 4 < len(prices):
                candle_prices = prices[i:i+5]
                open_price = candle_prices[0]
                high_price = max(candle_prices)
                low_price = min(candle_prices)
                close_price = candle_prices[-1]
                volume = random.randint(100000, 1000000)
                
                data.append({
                    'Open': round(open_price, 2),
                    'High': round(high_price, 2),
                    'Low': round(low_price, 2),
                    'Close': round(close_price, 2),
                    'Volume': volume
                })
        
        df = pd.DataFrame(data)
        df.index = pd.date_range(start=start_time, end=end_time, periods=len(df))
        
        return df
    
    def get_mock_market_data_batch(self, symbols: list) -> Dict[str, Dict]:
        """Get mock data for multiple symbols"""
        results = {}
        
        for symbol in symbols:
            results[symbol] = self.get_mock_quote(symbol)
            time.sleep(0.1)  # Small delay to simulate processing
        
        return results

# Global instance
mock_data_provider = MockDataProvider() 