#!/usr/bin/env python3
"""
Optimized Technical Indicators Module
Calculates various technical indicators for options scalping with enhanced performance
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

@dataclass
class IndicatorResult:
    """Structured indicator result"""
    value: float
    signal: str  # 'buy', 'sell', 'neutral'
    strength: float  # 0.0-1.0
    metadata: Dict

class OptimizedIndicators:
    """Optimized technical indicators calculator"""
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes
        
    def calc_indicators(self, data: pd.DataFrame) -> Dict:
        """
        Calculate comprehensive technical indicators for scalping
        
        Args:
            data (pd.DataFrame): OHLCV data
        
        Returns:
            dict: Dictionary containing calculated indicators
        """
        if data.empty or len(data) < 50:
            return self._get_default_indicators()
        
        indicators = {}
        
        # Basic price indicators
        indicators.update(self._calc_price_indicators(data))
        
        # Momentum indicators
        indicators.update(self._calc_momentum_indicators(data))
        
        # Volume indicators
        indicators.update(self._calc_volume_indicators(data))
        
        # Volatility indicators
        indicators.update(self._calc_volatility_indicators(data))
        
        # Trend indicators
        indicators.update(self._calc_trend_indicators(data))
        
        # Advanced scalping indicators
        indicators.update(self._calc_scalping_indicators(data))
        
        # Current price and metadata
        indicators['current_price'] = data['Close'].iloc[-1]
        indicators['timestamp'] = data.index[-1]
        
        return indicators
    
    def _calc_price_indicators(self, data: pd.DataFrame) -> Dict:
        """Calculate price-based indicators"""
        indicators = {}
        
        # Moving averages
        indicators['sma_20'] = data['Close'].rolling(window=20).mean().iloc[-1]
        indicators['sma_50'] = data['Close'].rolling(window=50).mean().iloc[-1]
        indicators['ema_12'] = data['Close'].ewm(span=12).mean().iloc[-1]
        indicators['ema_26'] = data['Close'].ewm(span=26).mean().iloc[-1]
        
        # Price changes
        if len(data) > 1:
            indicators['price_change'] = data['Close'].iloc[-1] - data['Close'].iloc[-2]
            indicators['price_change_pct'] = (indicators['price_change'] / data['Close'].iloc[-2]) * 100
            indicators['price_change_5min'] = (data['Close'].iloc[-1] - data['Close'].iloc[-6]) / data['Close'].iloc[-6] * 100 if len(data) > 6 else 0
        else:
            indicators['price_change'] = 0
            indicators['price_change_pct'] = 0
            indicators['price_change_5min'] = 0
        
        # Bollinger Bands
        bb_data = self._calculate_bollinger_bands(data['Close'])
        indicators.update(bb_data)
        
        # VWAP
        indicators['vwap'] = self._calculate_vwap(data)
        
        return indicators
    
    def _calc_momentum_indicators(self, data: pd.DataFrame) -> Dict:
        """Calculate momentum indicators"""
        indicators = {}
        
        # RSI with momentum
        indicators['rsi'] = self._calculate_rsi(data['Close'])
        indicators['rsi_momentum'] = self._calculate_rsi_momentum(data['Close'])
        
        # MACD
        macd_data = self._calculate_macd(data['Close'])
        indicators.update(macd_data)
        
        # Stochastic RSI
        stoch_rsi = self._calculate_stochastic_rsi(data['Close'])
        indicators.update(stoch_rsi)
        
        # Williams %R
        indicators['williams_r'] = self._calculate_williams_r(data)
        
        # CCI (Commodity Channel Index)
        indicators['cci'] = self._calculate_cci(data)
        
        return indicators
    
    def _calc_volume_indicators(self, data: pd.DataFrame) -> Dict:
        """Calculate volume-based indicators"""
        indicators = {}
        
        # Volume SMA and ratio
        indicators['volume_sma'] = data['Volume'].rolling(window=20).mean().iloc[-1]
        indicators['volume_ratio'] = data['Volume'].iloc[-1] / indicators['volume_sma'] if indicators['volume_sma'] > 0 else 1
        
        # OBV (On-Balance Volume)
        indicators['obv'] = self._calculate_obv(data)
        indicators['obv_momentum'] = self._calculate_obv_momentum(data)
        
        # Volume Price Trend
        indicators['vpt'] = self._calculate_vpt(data)
        
        # Money Flow Index
        indicators['mfi'] = self._calculate_mfi(data)
        
        return indicators
    
    def _calc_volatility_indicators(self, data: pd.DataFrame) -> Dict:
        """Calculate volatility indicators"""
        indicators = {}
        
        # ATR (Average True Range)
        indicators['atr'] = self._calculate_atr(data)
        
        # Bollinger Band width
        if 'bb_upper' in indicators and 'bb_lower' in indicators:
            bb_middle = (indicators['bb_upper'] + indicators['bb_lower']) / 2
            indicators['bb_width'] = (indicators['bb_upper'] - indicators['bb_lower']) / bb_middle if bb_middle > 0 else 0
        
        # Historical Volatility
        indicators['hist_volatility'] = self._calculate_historical_volatility(data['Close'])
        
        # Keltner Channels
        keltner_data = self._calculate_keltner_channels(data)
        indicators.update(keltner_data)
        
        return indicators
    
    def _calc_trend_indicators(self, data: pd.DataFrame) -> Dict:
        """Calculate trend indicators"""
        indicators = {}
        
        # ADX (Average Directional Index)
        adx_data = self._calculate_adx(data)
        indicators.update(adx_data)
        
        # Parabolic SAR
        indicators['psar'] = self._calculate_psar(data)
        
        # Ichimoku Cloud
        ichimoku_data = self._calculate_ichimoku(data)
        indicators.update(ichimoku_data)
        
        return indicators
    
    def _calc_scalping_indicators(self, data: pd.DataFrame) -> Dict:
        """Calculate specialized scalping indicators"""
        indicators = {}
        
        # Price action patterns
        indicators['doji'] = self._detect_doji(data)
        indicators['hammer'] = self._detect_hammer(data)
        indicators['engulfing'] = self._detect_engulfing(data)
        
        # Support/Resistance levels
        support_resistance = self._find_support_resistance(data)
        indicators.update(support_resistance)
        
        # Momentum divergence
        indicators['rsi_divergence'] = self._detect_rsi_divergence(data)
        
        # Volume profile
        indicators['volume_profile'] = self._calculate_volume_profile(data)
        
        return indicators
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> float:
        """Calculate RSI with optimization"""
        if len(prices) < period:
            return 50.0
        
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi.iloc[-1] if not rsi.empty and not np.isnan(rsi.iloc[-1]) else 50.0
    
    def _calculate_rsi_momentum(self, prices: pd.Series, period: int = 14) -> float:
        """Calculate RSI momentum"""
        rsi = pd.Series([self._calculate_rsi(prices.iloc[:i+1], period) 
                        for i in range(period, len(prices))], 
                       index=prices.index[period:])
        
        if len(rsi) > 1:
            return rsi.iloc[-1] - rsi.iloc[-2]
        return 0.0
    
    def _calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
        """Calculate MACD with enhanced signals"""
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal).mean()
        histogram = macd - signal_line
        
        return {
            'macd': macd.iloc[-1] if not macd.empty else 0,
            'macd_signal': signal_line.iloc[-1] if not signal_line.empty else 0,
            'macd_histogram': histogram.iloc[-1] if not histogram.empty else 0,
            'macd_crossover': macd.iloc[-1] > signal_line.iloc[-1] if len(macd) > 0 and len(signal_line) > 0 else False
        }
    
    def _calculate_bollinger_bands(self, prices: pd.Series, period: int = 20, std_dev: float = 2.0) -> Dict:
        """Calculate Bollinger Bands"""
        middle = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper = middle + (std * std_dev)
        lower = middle - (std * std_dev)
        
        return {
            'bb_upper': upper.iloc[-1] if not upper.empty else 0,
            'bb_middle': middle.iloc[-1] if not middle.empty else 0,
            'bb_lower': lower.iloc[-1] if not lower.empty else 0,
            'bb_position': (prices.iloc[-1] - lower.iloc[-1]) / (upper.iloc[-1] - lower.iloc[-1]) if len(upper) > 0 and len(lower) > 0 and upper.iloc[-1] != lower.iloc[-1] else 0.5
        }
    
    def _calculate_vwap(self, data: pd.DataFrame) -> float:
        """Calculate VWAP (Volume Weighted Average Price)"""
        typical_price = (data['High'] + data['Low'] + data['Close']) / 3
        vwap = (typical_price * data['Volume']).cumsum() / data['Volume'].cumsum()
        return vwap.iloc[-1] if not vwap.empty else 0
    
    def _calculate_stochastic_rsi(self, prices: pd.Series, period: int = 14, k_period: int = 3, d_period: int = 3) -> Dict:
        """Calculate Stochastic RSI"""
        rsi = pd.Series([self._calculate_rsi(prices.iloc[:i+1], period) 
                        for i in range(period, len(prices))], 
                       index=prices.index[period:])
        
        if len(rsi) < k_period:
            return {'stoch_rsi_k': 50, 'stoch_rsi_d': 50}
        
        rsi_min = rsi.rolling(window=k_period).min()
        rsi_max = rsi.rolling(window=k_period).max()
        
        stoch_k = 100 * (rsi - rsi_min) / (rsi_max - rsi_min)
        stoch_d = stoch_k.rolling(window=d_period).mean()
        
        return {
            'stoch_rsi_k': stoch_k.iloc[-1] if not stoch_k.empty else 50,
            'stoch_rsi_d': stoch_d.iloc[-1] if not stoch_d.empty else 50
        }
    
    def _calculate_williams_r(self, data: pd.DataFrame, period: int = 14) -> float:
        """Calculate Williams %R"""
        highest_high = data['High'].rolling(window=period).max()
        lowest_low = data['Low'].rolling(window=period).min()
        
        williams_r = -100 * (highest_high - data['Close']) / (highest_high - lowest_low)
        return williams_r.iloc[-1] if not williams_r.empty else -50
    
    def _calculate_cci(self, data: pd.DataFrame, period: int = 20) -> float:
        """Calculate CCI (Commodity Channel Index)"""
        typical_price = (data['High'] + data['Low'] + data['Close']) / 3
        sma_tp = typical_price.rolling(window=period).mean()
        mad = typical_price.rolling(window=period).apply(lambda x: np.mean(np.abs(x - x.mean())))
        
        cci = (typical_price - sma_tp) / (0.015 * mad)
        return cci.iloc[-1] if not cci.empty else 0
    
    def _calculate_obv(self, data: pd.DataFrame) -> float:
        """Calculate OBV (On-Balance Volume)"""
        obv = pd.Series(index=data.index, dtype=float)
        obv.iloc[0] = data['Volume'].iloc[0]
        
        for i in range(1, len(data)):
            if data['Close'].iloc[i] > data['Close'].iloc[i-1]:
                obv.iloc[i] = obv.iloc[i-1] + data['Volume'].iloc[i]
            elif data['Close'].iloc[i] < data['Close'].iloc[i-1]:
                obv.iloc[i] = obv.iloc[i-1] - data['Volume'].iloc[i]
            else:
                obv.iloc[i] = obv.iloc[i-1]
        
        return obv.iloc[-1] if not obv.empty else 0
    
    def _calculate_obv_momentum(self, data: pd.DataFrame, period: int = 10) -> float:
        """Calculate OBV momentum"""
        obv = self._calculate_obv(data)
        obv_series = pd.Series([self._calculate_obv(data.iloc[:i+1]) for i in range(len(data))])
        
        if len(obv_series) > period:
            return obv_series.iloc[-1] - obv_series.iloc[-period-1]
        return 0
    
    def _calculate_vpt(self, data: pd.DataFrame) -> float:
        """Calculate VPT (Volume Price Trend)"""
        price_change = data['Close'].pct_change()
        vpt = (price_change * data['Volume']).cumsum()
        return vpt.iloc[-1] if not vpt.empty else 0
    
    def _calculate_mfi(self, data: pd.DataFrame, period: int = 14) -> float:
        """Calculate MFI (Money Flow Index)"""
        typical_price = (data['High'] + data['Low'] + data['Close']) / 3
        money_flow = typical_price * data['Volume']
        
        positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0).rolling(window=period).sum()
        negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0).rolling(window=period).sum()
        
        mfi = 100 - (100 / (1 + positive_flow / negative_flow))
        return mfi.iloc[-1] if not mfi.empty else 50
    
    def _calculate_atr(self, data: pd.DataFrame, period: int = 14) -> float:
        """Calculate ATR (Average True Range)"""
        high = data['High']
        low = data['Low']
        close = data['Close']
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        
        return atr.iloc[-1] if not atr.empty else 0
    
    def _calculate_historical_volatility(self, prices: pd.Series, period: int = 20) -> float:
        """Calculate historical volatility"""
        returns = prices.pct_change().dropna()
        if len(returns) >= period:
            return returns.rolling(window=period).std().iloc[-1] * np.sqrt(252)  # Annualized
        return 0
    
    def _calculate_keltner_channels(self, data: pd.DataFrame, period: int = 20, multiplier: float = 2.0) -> Dict:
        """Calculate Keltner Channels"""
        typical_price = (data['High'] + data['Low'] + data['Close']) / 3
        atr = self._calculate_atr(data, period)
        
        middle = typical_price.rolling(window=period).mean()
        upper = middle + (multiplier * atr)
        lower = middle - (multiplier * atr)
        
        return {
            'keltner_upper': upper.iloc[-1] if not upper.empty else 0,
            'keltner_middle': middle.iloc[-1] if not middle.empty else 0,
            'keltner_lower': lower.iloc[-1] if not lower.empty else 0
        }
    
    def _calculate_adx(self, data: pd.DataFrame, period: int = 14) -> Dict:
        """Calculate ADX (Average Directional Index)"""
        high = data['High']
        low = data['Low']
        close = data['Close']
        
        # Calculate +DM and -DM
        high_diff = high - high.shift(1)
        low_diff = low.shift(1) - low
        
        plus_dm = np.where((high_diff > low_diff) & (high_diff > 0), high_diff, 0)
        minus_dm = np.where((low_diff > high_diff) & (low_diff > 0), low_diff, 0)
        
        # Calculate TR
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        # Smooth the values
        plus_di = 100 * pd.Series(plus_dm).rolling(window=period).mean() / tr.rolling(window=period).mean()
        minus_di = 100 * pd.Series(minus_dm).rolling(window=period).mean() / tr.rolling(window=period).mean()
        
        # Calculate ADX
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(window=period).mean()
        
        return {
            'adx': adx.iloc[-1] if not adx.empty else 0,
            'plus_di': plus_di.iloc[-1] if not plus_di.empty else 0,
            'minus_di': minus_di.iloc[-1] if not minus_di.empty else 0
        }
    
    def _calculate_psar(self, data: pd.DataFrame, acceleration: float = 0.02, maximum: float = 0.2) -> float:
        """Calculate Parabolic SAR"""
        high = data['High'].values
        low = data['Low'].values
        close = data['Close'].values
        
        psar = np.zeros(len(data))
        af = acceleration
        ep = low[0]
        long = True
        
        for i in range(1, len(data)):
            if long:
                psar[i] = psar[i-1] + af * (ep - psar[i-1])
                if low[i] < psar[i]:
                    long = False
                    psar[i] = ep
                    ep = high[i]
                    af = acceleration
                else:
                    if high[i] > ep:
                        ep = high[i]
                        af = min(af + acceleration, maximum)
            else:
                psar[i] = psar[i-1] + af * (ep - psar[i-1])
                if high[i] > psar[i]:
                    long = True
                    psar[i] = ep
                    ep = low[i]
                    af = acceleration
                else:
                    if low[i] < ep:
                        ep = low[i]
                        af = min(af + acceleration, maximum)
        
        return psar[-1]
    
    def _calculate_ichimoku(self, data: pd.DataFrame) -> Dict:
        """Calculate Ichimoku Cloud components"""
        high = data['High']
        low = data['Low']
        
        # Tenkan-sen (Conversion Line)
        period9 = (high.rolling(window=9).max() + low.rolling(window=9).min()) / 2
        
        # Kijun-sen (Base Line)
        period26 = (high.rolling(window=26).max() + low.rolling(window=26).min()) / 2
        
        # Senkou Span A (Leading Span A)
        senkou_span_a = ((period9 + period26) / 2).shift(26)
        
        # Senkou Span B (Leading Span B)
        period52 = (high.rolling(window=52).max() + low.rolling(window=52).min()) / 2
        senkou_span_b = period52.shift(26)
        
        return {
            'ichimoku_tenkan': period9.iloc[-1] if not period9.empty else 0,
            'ichimoku_kijun': period26.iloc[-1] if not period26.empty else 0,
            'ichimoku_senkou_a': senkou_span_a.iloc[-1] if not senkou_span_a.empty else 0,
            'ichimoku_senkou_b': senkou_span_b.iloc[-1] if not senkou_span_b.empty else 0
        }
    
    def _detect_doji(self, data: pd.DataFrame) -> bool:
        """Detect Doji candlestick pattern"""
        if len(data) < 1:
            return False
        
        open_price = data['Open'].iloc[-1]
        close_price = data['Close'].iloc[-1]
        high_price = data['High'].iloc[-1]
        low_price = data['Low'].iloc[-1]
        
        body_size = abs(close_price - open_price)
        total_range = high_price - low_price
        
        return body_size <= (total_range * 0.1)  # Body is 10% or less of total range
    
    def _detect_hammer(self, data: pd.DataFrame) -> bool:
        """Detect Hammer candlestick pattern"""
        if len(data) < 1:
            return False
        
        open_price = data['Open'].iloc[-1]
        close_price = data['Close'].iloc[-1]
        high_price = data['High'].iloc[-1]
        low_price = data['Low'].iloc[-1]
        
        body_size = abs(close_price - open_price)
        lower_shadow = min(open_price, close_price) - low_price
        upper_shadow = high_price - max(open_price, close_price)
        
        return (lower_shadow > 2 * body_size) and (upper_shadow < body_size)
    
    def _detect_engulfing(self, data: pd.DataFrame) -> bool:
        """Detect Engulfing candlestick pattern"""
        if len(data) < 2:
            return False
        
        prev_open = data['Open'].iloc[-2]
        prev_close = data['Close'].iloc[-2]
        curr_open = data['Open'].iloc[-1]
        curr_close = data['Close'].iloc[-1]
        
        # Bullish engulfing
        if (prev_close < prev_open and  # Previous candle is bearish
            curr_close > curr_open and   # Current candle is bullish
            curr_open < prev_close and   # Current open below previous close
            curr_close > prev_open):     # Current close above previous open
            return True
        
        return False
    
    def _find_support_resistance(self, data: pd.DataFrame) -> Dict:
        """Find support and resistance levels"""
        if len(data) < 20:
            return {'support_level': 0, 'resistance_level': 0}
        
        # Simple pivot points
        high = data['High'].rolling(window=20).max()
        low = data['Low'].rolling(window=20).min()
        
        return {
            'support_level': low.iloc[-1] if not low.empty else 0,
            'resistance_level': high.iloc[-1] if not high.empty else 0
        }
    
    def _detect_rsi_divergence(self, data: pd.DataFrame) -> str:
        """Detect RSI divergence"""
        if len(data) < 30:
            return 'none'
        
        # Calculate RSI for last 30 periods
        rsi_values = []
        price_values = []
        
        for i in range(20, len(data)):
            rsi = self._calculate_rsi(data['Close'].iloc[:i+1])
            rsi_values.append(rsi)
            price_values.append(data['Close'].iloc[i])
        
        if len(rsi_values) < 10:
            return 'none'
        
        # Check for divergence
        price_trend = price_values[-1] > price_values[0]
        rsi_trend = rsi_values[-1] > rsi_values[0]
        
        if price_trend and not rsi_trend:
            return 'bearish'
        elif not price_trend and rsi_trend:
            return 'bullish'
        
        return 'none'
    
    def _calculate_volume_profile(self, data: pd.DataFrame) -> Dict:
        """Calculate volume profile"""
        if len(data) < 20:
            return {'volume_heavy': False, 'volume_light': False}
        
        recent_volume = data['Volume'].iloc[-5:].mean()
        avg_volume = data['Volume'].iloc[-20:].mean()
        
        return {
            'volume_heavy': recent_volume > avg_volume * 1.5,
            'volume_light': recent_volume < avg_volume * 0.5
        }
    
    def _get_default_indicators(self) -> Dict:
        """Get default indicator values"""
        return {
            'current_price': 0,
            'rsi': 50,
            'macd': 0,
            'macd_signal': 0,
            'volume_ratio': 1,
            'price_change_pct': 0,
            'atr': 0,
            'bb_width': 0
        }

# Global instance for backward compatibility
indicators_calculator = OptimizedIndicators()

def calc_indicators(data):
    """Backward compatibility function"""
    return indicators_calculator.calc_indicators(data)

def calculate_rsi(prices, period=14):
    """Backward compatibility function"""
    return indicators_calculator._calculate_rsi(prices, period)

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Backward compatibility function"""
    return indicators_calculator._calculate_macd(prices, fast, slow, signal)

def calculate_bollinger_bands(prices, period=20, std_dev=2):
    """Backward compatibility function"""
    return indicators_calculator._calculate_bollinger_bands(prices, period, std_dev)

def calculate_atr(data, period=14):
    """Backward compatibility function"""
    return indicators_calculator._calculate_atr(data, period) 