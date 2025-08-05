#!/usr/bin/env python3
"""
Technical Indicators for Options Scalping Bot
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional

class TechnicalIndicators:
    def __init__(self):
        """Initialize technical indicators calculator"""
        pass
    
    def calculate_all_indicators(self, data: pd.DataFrame) -> Dict:
        """Calculate all technical indicators for a dataset"""
        if data is None or data.empty:
            return {}
        
        try:
            indicators = {}
            
            # Basic price data
            indicators['current_price'] = data['Close'].iloc[-1]
            indicators['open_price'] = data['Open'].iloc[-1]
            indicators['high_price'] = data['High'].iloc[-1]
            indicators['low_price'] = data['Low'].iloc[-1]
            
            # RSI
            indicators['rsi'] = self.calculate_rsi(data['Close'])
            
            # MACD
            macd_data = self.calculate_macd(data['Close'])
            indicators['macd'] = macd_data['macd']
            indicators['macd_signal'] = macd_data['signal']
            indicators['macd_histogram'] = macd_data['histogram']
            
            # Moving Averages
            indicators['sma_20'] = self.calculate_sma(data['Close'], 20)
            indicators['sma_50'] = self.calculate_sma(data['Close'], 50)
            indicators['ema_12'] = self.calculate_ema(data['Close'], 12)
            indicators['ema_26'] = self.calculate_ema(data['Close'], 26)
            
            # Bollinger Bands
            bb_data = self.calculate_bollinger_bands(data['Close'])
            indicators['bb_upper'] = bb_data['upper']
            indicators['bb_middle'] = bb_data['middle']
            indicators['bb_lower'] = bb_data['lower']
            indicators['bb_width'] = bb_data['width']
            
            # Volume indicators
            indicators['volume_sma'] = self.calculate_volume_sma(data)
            indicators['volume_ratio'] = self.calculate_volume_ratio(data)
            
            # ATR for volatility
            indicators['atr'] = self.calculate_atr(data)
            
            # VWAP
            indicators['vwap'] = self.calculate_vwap(data)
            
            return indicators
            
        except Exception as e:
            print(f"Error calculating indicators: {e}")
            return {}
    
    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> float:
        """Calculate Relative Strength Index"""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi.iloc[-1] if not rsi.empty else 50
        except Exception:
            return 50
    
    def calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
        """Calculate MACD (Moving Average Convergence Divergence)"""
        try:
            ema_fast = self.calculate_ema(prices, fast)
            ema_slow = self.calculate_ema(prices, slow)
            macd_line = ema_fast - ema_slow
            
            # Calculate signal line (EMA of MACD)
            macd_series = prices.ewm(span=fast).mean() - prices.ewm(span=slow).mean()
            signal_line = macd_series.ewm(span=signal).mean()
            
            return {
                'macd': macd_line,
                'signal': signal_line.iloc[-1] if not signal_line.empty else 0,
                'histogram': macd_line - signal_line.iloc[-1] if not signal_line.empty else 0
            }
        except Exception:
            return {'macd': 0, 'signal': 0, 'histogram': 0}
    
    def calculate_sma(self, prices: pd.Series, period: int) -> float:
        """Calculate Simple Moving Average"""
        try:
            sma = prices.rolling(window=period).mean()
            return sma.iloc[-1] if not sma.empty else prices.iloc[-1]
        except Exception:
            return prices.iloc[-1] if not prices.empty else 0
    
    def calculate_ema(self, prices: pd.Series, period: int) -> float:
        """Calculate Exponential Moving Average"""
        try:
            ema = prices.ewm(span=period).mean()
            return ema.iloc[-1] if not ema.empty else prices.iloc[-1]
        except Exception:
            return prices.iloc[-1] if not prices.empty else 0
    
    def calculate_bollinger_bands(self, prices: pd.Series, period: int = 20, std_dev: int = 2) -> Dict:
        """Calculate Bollinger Bands"""
        try:
            sma = prices.rolling(window=period).mean()
            std = prices.rolling(window=period).std()
            
            upper_band = sma + (std * std_dev)
            lower_band = sma - (std * std_dev)
            
            return {
                'upper': upper_band.iloc[-1] if not upper_band.empty else prices.iloc[-1],
                'middle': sma.iloc[-1] if not sma.empty else prices.iloc[-1],
                'lower': lower_band.iloc[-1] if not lower_band.empty else prices.iloc[-1],
                'width': (upper_band.iloc[-1] - lower_band.iloc[-1]) / sma.iloc[-1] if not sma.empty else 0
            }
        except Exception:
            current_price = prices.iloc[-1] if not prices.empty else 0
            return {
                'upper': current_price,
                'middle': current_price,
                'lower': current_price,
                'width': 0
            }
    
    def calculate_volume_sma(self, data: pd.DataFrame, period: int = 20) -> float:
        """Calculate Volume Simple Moving Average"""
        try:
            volume_sma = data['Volume'].rolling(window=period).mean()
            current_volume = data['Volume'].iloc[-1]
            return current_volume / volume_sma.iloc[-1] if not volume_sma.empty and volume_sma.iloc[-1] > 0 else 1
        except Exception:
            return 1
    
    def calculate_volume_ratio(self, data: pd.DataFrame) -> float:
        """Calculate volume ratio (current volume vs average)"""
        try:
            avg_volume = data['Volume'].mean()
            current_volume = data['Volume'].iloc[-1]
            return current_volume / avg_volume if avg_volume > 0 else 1
        except Exception:
            return 1
    
    def calculate_atr(self, data: pd.DataFrame, period: int = 14) -> float:
        """Calculate Average True Range"""
        try:
            high_low = data['High'] - data['Low']
            high_close = np.abs(data['High'] - data['Close'].shift())
            low_close = np.abs(data['Low'] - data['Close'].shift())
            
            true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            atr = true_range.rolling(window=period).mean()
            
            return atr.iloc[-1] if not atr.empty else 0
        except Exception:
            return 0
    
    def calculate_vwap(self, data: pd.DataFrame) -> float:
        """Calculate Volume Weighted Average Price"""
        try:
            typical_price = (data['High'] + data['Low'] + data['Close']) / 3
            vwap = (typical_price * data['Volume']).cumsum() / data['Volume'].cumsum()
            return vwap.iloc[-1] if not vwap.empty else data['Close'].iloc[-1]
        except Exception:
            return data['Close'].iloc[-1] if not data.empty else 0
    
    def get_signal_strength(self, indicators: Dict) -> Dict:
        """Get signal strength based on indicators"""
        try:
            strength = 0
            reasons = []
            
            # RSI signals
            rsi = indicators.get('rsi', 50)
            if rsi < 30:
                strength += 25
                reasons.append("RSI oversold")
            elif rsi > 70:
                strength -= 25
                reasons.append("RSI overbought")
            
            # MACD signals
            macd = indicators.get('macd', 0)
            macd_signal = indicators.get('macd_signal', 0)
            if macd > macd_signal:
                strength += 20
                reasons.append("MACD bullish")
            elif macd < macd_signal:
                strength -= 20
                reasons.append("MACD bearish")
            
            # Bollinger Bands signals
            current_price = indicators.get('current_price', 0)
            bb_upper = indicators.get('bb_upper', 0)
            bb_lower = indicators.get('bb_lower', 0)
            
            if current_price < bb_lower:
                strength += 20
                reasons.append("Price below BB")
            elif current_price > bb_upper:
                strength -= 20
                reasons.append("Price above BB")
            
            # Volume signals
            volume_sma = indicators.get('volume_sma', 1)
            if volume_sma > 1.5:
                strength += 15
                reasons.append("High volume")
            elif volume_sma < 0.5:
                strength -= 15
                reasons.append("Low volume")
            
            # Moving average signals
            sma_20 = indicators.get('sma_20', 0)
            if current_price > sma_20:
                strength += 10
                reasons.append("Price above SMA20")
            else:
                strength -= 10
                reasons.append("Price below SMA20")
            
            return {
                'strength': strength,
                'reasons': reasons,
                'signal': 'BUY' if strength >= 30 else 'SELL' if strength <= -30 else 'HOLD'
            }
            
        except Exception as e:
            return {
                'strength': 0,
                'reasons': [f"Error: {e}"],
                'signal': 'HOLD'
            } 