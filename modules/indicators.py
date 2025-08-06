#!/usr/bin/env python3
"""
Technical Indicators Module
Calculates various technical indicators for options scalping
"""

import pandas as pd
import numpy as np

def calc_indicators(data):
    """
    Calculate technical indicators for the given data
    
    Args:
        data (pd.DataFrame): OHLCV data
    
    Returns:
        dict: Dictionary containing calculated indicators
    """
    if data.empty:
        return {}
    
    indicators = {}
    
    # RSI
    indicators['rsi'] = calculate_rsi(data['Close'])
    
    # Moving Averages
    indicators['sma_20'] = data['Close'].rolling(window=20).mean().iloc[-1]
    indicators['sma_50'] = data['Close'].rolling(window=50).mean().iloc[-1]
    
    # MACD
    macd_data = calculate_macd(data['Close'])
    indicators['macd'] = macd_data['macd'].iloc[-1]
    indicators['macd_signal'] = macd_data['signal'].iloc[-1]
    indicators['macd_histogram'] = macd_data['histogram'].iloc[-1]
    
    # Bollinger Bands
    bb_data = calculate_bollinger_bands(data['Close'])
    indicators['bb_upper'] = bb_data['upper'].iloc[-1]
    indicators['bb_middle'] = bb_data['middle'].iloc[-1]
    indicators['bb_lower'] = bb_data['lower'].iloc[-1]
    
    # Volume indicators
    indicators['volume_sma'] = data['Volume'].rolling(window=20).mean().iloc[-1]
    indicators['volume_ratio'] = data['Volume'].iloc[-1] / indicators['volume_sma']
    
    # Price momentum
    indicators['price_change'] = data['Close'].iloc[-1] - data['Close'].iloc[-2] if len(data) > 1 else 0
    indicators['price_change_pct'] = ((data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2] * 100) if len(data) > 1 else 0
    
    # Current price
    indicators['current_price'] = data['Close'].iloc[-1]
    
    return indicators

def calculate_rsi(prices, period=14):
    """Calculate RSI"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not rsi.empty else 50

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calculate MACD"""
    ema_fast = prices.ewm(span=fast).mean()
    ema_slow = prices.ewm(span=slow).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal).mean()
    histogram = macd - signal_line
    
    return {
        'macd': macd,
        'signal': signal_line,
        'histogram': histogram
    }

def calculate_bollinger_bands(prices, period=20, std_dev=2):
    """Calculate Bollinger Bands"""
    middle = prices.rolling(window=period).mean()
    std = prices.rolling(window=period).std()
    upper = middle + (std * std_dev)
    lower = middle - (std * std_dev)
    
    return {
        'upper': upper,
        'middle': middle,
        'lower': lower
    }

def calculate_atr(data, period=14):
    """Calculate Average True Range"""
    high = data['High']
    low = data['Low']
    close = data['Close']
    
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    
    return atr.iloc[-1] if not atr.empty else 0 