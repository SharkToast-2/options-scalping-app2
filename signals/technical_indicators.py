"""
Optimized Technical Indicators Module for Options Scalping Signals
"""

import pandas as pd
import numpy as np
import time
from typing import Dict, List, Tuple, Optional
import logging
from functools import lru_cache
from ta.trend import MACD, ADXIndicator, EMAIndicator
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands
from ta.volume import OnBalanceVolumeIndicator
from ta.volatility import AverageTrueRange

from config.settings import INDICATOR_CONFIG

logger = logging.getLogger(__name__)

class OptimizedTechnicalIndicators:
    """Optimized technical indicators calculator with caching and vectorized operations"""
    
    def __init__(self):
        self.config = INDICATOR_CONFIG
        self._indicator_cache = {}
        self._cache_timestamps = {}
        self.cache_duration = 300  # 5 minutes
    
    def _check_cache(self, key: str, data_hash: str) -> Optional[Dict]:
        """Check if indicators are cached for this data"""
        if key in self._indicator_cache:
            cached_data = self._indicator_cache[key]
            if (cached_data.get('data_hash') == data_hash and 
                time.time() - cached_data.get('timestamp', 0) < self.cache_duration):
                return cached_data.get('indicators')
        return None
    
    def _update_cache(self, key: str, data_hash: str, indicators: Dict):
        """Update cache with calculated indicators"""
        self._indicator_cache[key] = {
            'indicators': indicators,
            'data_hash': data_hash,
            'timestamp': time.time()
        }
    
    def _get_data_hash(self, data: pd.DataFrame) -> str:
        """Generate hash for data to check if cache is valid"""
        return str(hash(str(data.tail(10).values.tobytes())))
    
    @lru_cache(maxsize=50)
    def calculate_all_indicators(self, data_key: str) -> Dict[str, pd.Series]:
        """Calculate all technical indicators with caching"""
        # This is a simplified version - in practice, you'd pass the actual data
        # and use the data hash for caching
        return self._calculate_indicators_vectorized(data_key)
    
    def _calculate_indicators_vectorized(self, data: pd.DataFrame) -> Dict[str, pd.Series]:
        """Calculate indicators using vectorized operations for better performance"""
        try:
            indicators = {}
            
            # Vectorized calculations for better performance
            close = data['Close']
            high = data['High']
            low = data['Low']
            volume = data['Volume']
            
            # Core indicators (vectorized)
            indicators['rsi'] = self._calculate_rsi_vectorized(close)
            indicators['macd'] = self._calculate_macd_vectorized(close)
            indicators['vwap'] = self._calculate_vwap_vectorized(high, low, close, volume)
            indicators['ema_trend'] = self._calculate_ema_trend_vectorized(close)
            indicators['bb_width'] = self._calculate_bollinger_vectorized(close)
            indicators['adx'] = self._calculate_adx_vectorized(high, low, close)
            
            # Enhanced indicators
            indicators['obv'] = self._calculate_obv_vectorized(close, volume)
            indicators['atr'] = self._calculate_atr_vectorized(high, low, close)
            indicators['stoch_rsi'] = self._calculate_stoch_rsi_vectorized(close)
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            return {}
    
    def _calculate_rsi_vectorized(self, close: pd.Series, period: int = 14) -> pd.Series:
        """Vectorized RSI calculation"""
        try:
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return pd.Series(dtype=float)
    
    def _calculate_macd_vectorized(self, close: pd.Series) -> Dict[str, pd.Series]:
        """Vectorized MACD calculation"""
        try:
            fast_period = self.config['MACD']['FAST_PERIOD']
            slow_period = self.config['MACD']['SLOW_PERIOD']
            signal_period = self.config['MACD']['SIGNAL_PERIOD']
            
            ema_fast = close.ewm(span=fast_period).mean()
            ema_slow = close.ewm(span=slow_period).mean()
            macd_line = ema_fast - ema_slow
            signal_line = macd_line.ewm(span=signal_period).mean()
            macd_histogram = macd_line - signal_line
            
            return {
                'macd': macd_line,
                'macd_signal': signal_line,
                'macd_diff': macd_histogram
            }
        except Exception as e:
            logger.error(f"Error calculating MACD: {e}")
            return {'macd': pd.Series(dtype=float), 'macd_signal': pd.Series(dtype=float), 'macd_diff': pd.Series(dtype=float)}
    
    def _calculate_vwap_vectorized(self, high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, period: int = 20) -> pd.Series:
        """Vectorized VWAP calculation"""
        try:
            typical_price = (high + low + close) / 3
            vwap = (typical_price * volume).rolling(window=period).sum() / volume.rolling(window=period).sum()
            return vwap
        except Exception as e:
            logger.error(f"Error calculating VWAP: {e}")
            return pd.Series(dtype=float)
    
    def _calculate_ema_trend_vectorized(self, close: pd.Series) -> Dict[str, pd.Series]:
        """Vectorized EMA trend calculation"""
        try:
            ema_20 = close.ewm(span=20).mean()
            ema_50 = close.ewm(span=50).mean()
            ema_200 = close.ewm(span=200).mean()
            
            # Trend signals
            trend_20_50 = ema_20 > ema_50
            trend_50_200 = ema_50 > ema_200
            strong_trend = trend_20_50 & trend_50_200
            
            return {
                'ema_20': ema_20,
                'ema_50': ema_50,
                'ema_200': ema_200,
                'trend_20_50': trend_20_50,
                'trend_50_200': trend_50_200,
                'strong_trend': strong_trend
            }
        except Exception as e:
            logger.error(f"Error calculating EMA trend: {e}")
            return {}
    
    def _calculate_bollinger_vectorized(self, close: pd.Series, period: int = 20, std_dev: float = 2.0) -> Dict[str, pd.Series]:
        """Vectorized Bollinger Bands calculation"""
        try:
            sma = close.rolling(window=period).mean()
            std = close.rolling(window=period).std()
            
            upper_band = sma + (std * std_dev)
            lower_band = sma - (std * std_dev)
            bandwidth = (upper_band - lower_band) / sma
            
            return {
                'upper': upper_band,
                'middle': sma,
                'lower': lower_band,
                'bandwidth': bandwidth
            }
        except Exception as e:
            logger.error(f"Error calculating Bollinger Bands: {e}")
            return {}
    
    def _calculate_adx_vectorized(self, high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> Dict[str, pd.Series]:
        """Vectorized ADX calculation"""
        try:
            # Calculate True Range
            tr1 = high - low
            tr2 = abs(high - close.shift())
            tr3 = abs(low - close.shift())
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = tr.rolling(window=period).mean()
            
            # Calculate Directional Movement
            dm_plus = (high - high.shift()).where((high - high.shift()) > (low.shift() - low), 0)
            dm_minus = (low.shift() - low).where((low.shift() - low) > (high - high.shift()), 0)
            
            # Smooth the directional movement
            di_plus = 100 * (dm_plus.rolling(window=period).mean() / atr)
            di_minus = 100 * (dm_minus.rolling(window=period).mean() / atr)
            
            # Calculate ADX
            dx = 100 * abs(di_plus - di_minus) / (di_plus + di_minus)
            adx = dx.rolling(window=period).mean()
            
            return {
                'adx': adx,
                'di_plus': di_plus,
                'di_minus': di_minus
            }
        except Exception as e:
            logger.error(f"Error calculating ADX: {e}")
            return {}
    
    def _calculate_obv_vectorized(self, close: pd.Series, volume: pd.Series) -> pd.Series:
        """Vectorized OBV calculation"""
        try:
            price_change = close.diff()
            obv = pd.Series(index=close.index, dtype=float)
            obv.iloc[0] = volume.iloc[0]
            
            for i in range(1, len(close)):
                if price_change.iloc[i] > 0:
                    obv.iloc[i] = obv.iloc[i-1] + volume.iloc[i]
                elif price_change.iloc[i] < 0:
                    obv.iloc[i] = obv.iloc[i-1] - volume.iloc[i]
                else:
                    obv.iloc[i] = obv.iloc[i-1]
            
            return obv
        except Exception as e:
            logger.error(f"Error calculating OBV: {e}")
            return pd.Series(dtype=float)
    
    def _calculate_atr_vectorized(self, high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """Vectorized ATR calculation"""
        try:
            tr1 = high - low
            tr2 = abs(high - close.shift())
            tr3 = abs(low - close.shift())
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = tr.rolling(window=period).mean()
            return atr
        except Exception as e:
            logger.error(f"Error calculating ATR: {e}")
            return pd.Series(dtype=float)
    
    def _calculate_stoch_rsi_vectorized(self, close: pd.Series, rsi_period: int = 14, stoch_period: int = 14) -> Dict[str, pd.Series]:
        """Vectorized Stochastic RSI calculation"""
        try:
            rsi = self._calculate_rsi_vectorized(close, rsi_period)
            
            # Calculate Stochastic RSI
            rsi_min = rsi.rolling(window=stoch_period).min()
            rsi_max = rsi.rolling(window=stoch_period).max()
            stoch_rsi = (rsi - rsi_min) / (rsi_max - rsi_min)
            
            # Calculate signal line
            signal_line = stoch_rsi.rolling(window=3).mean()
            
            return {
                'stoch_rsi': stoch_rsi,
                'signal_line': signal_line
            }
        except Exception as e:
            logger.error(f"Error calculating Stochastic RSI: {e}")
            return {}
    
    def calculate_signal_strength(self, signals: Dict[str, bool]) -> int:
        """Calculate overall signal strength"""
        try:
            strength = 0
            
            # Weight different signals
            signal_weights = {
                'rsi_oversold': 15,
                'rsi_overbought': 15,
                'macd_bullish': 20,
                'macd_bearish': 20,
                'vwap_bullish': 10,
                'vwap_bearish': 10,
                'ema_trend_bullish': 15,
                'ema_trend_bearish': 15,
                'bb_squeeze': 10,
                'adx_strong': 10,
                'obv_bullish': 5,
                'obv_bearish': 5
            }
            
            for signal, weight in signal_weights.items():
                if signals.get(signal, False):
                    strength += weight
            
            return min(strength, 100)  # Cap at 100
            
        except Exception as e:
            logger.error(f"Error calculating signal strength: {e}")
            return 0
    
    def calculate_stock_scalping_score(self, data: pd.DataFrame, indicators: Dict[str, pd.Series], current_price: float) -> Dict[str, float]:
        """Calculate comprehensive scalping score for a stock"""
        try:
            if data.empty or not indicators:
                return {'overall_score': 0, 'volatility': 0, 'momentum': 0, 'trend': 0, 'volume': 0}
            
            # Get latest values
            latest_close = data['Close'].iloc[-1]
            latest_volume = data['Volume'].iloc[-1]
            
            # Volatility score (0-25 points)
            volatility_score = self._calculate_volatility_score(data, indicators)
            
            # Momentum score (0-25 points)
            momentum_score = self._calculate_momentum_score(indicators)
            
            # Trend score (0-25 points)
            trend_score = self._calculate_trend_score(indicators)
            
            # Volume score (0-25 points)
            volume_score = self._calculate_volume_score(data, indicators)
            
            # Overall score
            overall_score = volatility_score + momentum_score + trend_score + volume_score
            
            return {
                'overall_score': overall_score,
                'volatility': volatility_score,
                'momentum': momentum_score,
                'trend': trend_score,
                'volume': volume_score
            }
            
        except Exception as e:
            logger.error(f"Error calculating scalping score: {e}")
            return {'overall_score': 0, 'volatility': 0, 'momentum': 0, 'trend': 0, 'volume': 0}
    
    def _calculate_volatility_score(self, data: pd.DataFrame, indicators: Dict[str, pd.Series]) -> float:
        """Calculate volatility score (0-25 points)"""
        try:
            # Use ATR for volatility measurement
            atr = indicators.get('atr', pd.Series(dtype=float))
            if atr.empty:
                return 0
            
            latest_atr = atr.iloc[-1]
            avg_atr = atr.mean()
            
            # Higher volatility is better for scalping (up to a point)
            volatility_ratio = latest_atr / avg_atr if avg_atr > 0 else 0
            
            if 0.5 <= volatility_ratio <= 2.0:
                return min(25, volatility_ratio * 12.5)
            else:
                return max(0, 25 - abs(volatility_ratio - 1.25) * 10)
                
        except Exception as e:
            logger.error(f"Error calculating volatility score: {e}")
            return 0
    
    def _calculate_momentum_score(self, indicators: Dict[str, pd.Series]) -> float:
        """Calculate momentum score (0-25 points)"""
        try:
            score = 0
            
            # RSI momentum
            rsi = indicators.get('rsi', pd.Series(dtype=float))
            if not rsi.empty:
                latest_rsi = rsi.iloc[-1]
                if 30 <= latest_rsi <= 70:  # Not overbought/oversold
                    score += 10
                elif 40 <= latest_rsi <= 60:  # Neutral zone
                    score += 15
            
            # MACD momentum
            macd_data = indicators.get('macd', {})
            if isinstance(macd_data, dict) and 'macd_diff' in macd_data:
                macd_diff = macd_data['macd_diff']
                if not macd_diff.empty:
                    latest_diff = macd_diff.iloc[-1]
                    if abs(latest_diff) > 0:  # Some momentum
                        score += 10
            
            return min(25, score)
            
        except Exception as e:
            logger.error(f"Error calculating momentum score: {e}")
            return 0
    
    def _calculate_trend_score(self, indicators: Dict[str, pd.Series]) -> float:
        """Calculate trend score (0-25 points)"""
        try:
            score = 0
            
            # EMA trend
            ema_data = indicators.get('ema_trend', {})
            if isinstance(ema_data, dict) and 'strong_trend' in ema_data:
                strong_trend = ema_data['strong_trend']
                if not strong_trend.empty and strong_trend.iloc[-1]:
                    score += 15
            
            # ADX trend strength
            adx_data = indicators.get('adx', {})
            if isinstance(adx_data, dict) and 'adx' in adx_data:
                adx = adx_data['adx']
                if not adx.empty:
                    latest_adx = adx.iloc[-1]
                    if latest_adx > 25:  # Strong trend
                        score += 10
            
            return min(25, score)
            
        except Exception as e:
            logger.error(f"Error calculating trend score: {e}")
            return 0
    
    def _calculate_volume_score(self, data: pd.DataFrame, indicators: Dict[str, pd.Series]) -> float:
        """Calculate volume score (0-25 points)"""
        try:
            score = 0
            
            # Volume analysis
            volume = data['Volume']
            if not volume.empty:
                latest_volume = volume.iloc[-1]
                avg_volume = volume.mean()
                
                if latest_volume > avg_volume:  # Above average volume
                    score += 15
                elif latest_volume > avg_volume * 0.8:  # Near average volume
                    score += 10
            
            # OBV trend
            obv = indicators.get('obv', pd.Series(dtype=float))
            if not obv.empty and len(obv) > 1:
                obv_trend = obv.iloc[-1] - obv.iloc[-2]
                if obv_trend > 0:  # Positive OBV trend
                    score += 10
            
            return min(25, score)
            
        except Exception as e:
            logger.error(f"Error calculating volume score: {e}")
            return 0
    
    def rank_stocks_for_scalping(self, stock_data: Dict[str, pd.DataFrame], indicators_data: Dict[str, Dict[str, pd.Series]], current_prices: Dict[str, float]) -> List[Dict]:
        """Rank stocks for scalping opportunities"""
        try:
            rankings = []
            
            for symbol in stock_data.keys():
                data = stock_data[symbol]
                indicators = indicators_data.get(symbol, {})
                current_price = current_prices.get(symbol, 0)
                
                if data.empty or not indicators or current_price == 0:
                    continue
                
                # Calculate scores
                scores = self.calculate_stock_scalping_score(data, indicators, current_price)
                
                # Determine signal direction
                signal_direction = self._determine_signal_direction(indicators)
                
                # Calculate signal strength
                signal_strength = self._calculate_signal_strength_from_indicators(indicators)
                
                # Calculate volatility
                volatility = self._calculate_volatility_metric(data, indicators)
                
                rankings.append({
                    'symbol': symbol,
                    'overall_score': scores['overall_score'],
                    'volatility_score': scores['volatility'],
                    'momentum_score': scores['momentum'],
                    'trend_score': scores['trend'],
                    'volume_score': scores['volume'],
                    'signal_direction': signal_direction,
                    'signal_strength': signal_strength,
                    'volatility': volatility,
                    'current_price': current_price
                })
            
            # Sort by overall score (descending)
            rankings.sort(key=lambda x: x['overall_score'], reverse=True)
            
            return rankings
            
        except Exception as e:
            logger.error(f"Error ranking stocks: {e}")
            return []
    
    def _determine_signal_direction(self, indicators: Dict[str, pd.Series]) -> str:
        """Determine signal direction based on indicators"""
        try:
            bullish_signals = 0
            bearish_signals = 0
            
            # RSI signals
            rsi = indicators.get('rsi', pd.Series(dtype=float))
            if not rsi.empty:
                latest_rsi = rsi.iloc[-1]
                if latest_rsi < 30:
                    bullish_signals += 1
                elif latest_rsi > 70:
                    bearish_signals += 1
            
            # MACD signals
            macd_data = indicators.get('macd', {})
            if isinstance(macd_data, dict) and 'macd_diff' in macd_data:
                macd_diff = macd_data['macd_diff']
                if not macd_diff.empty:
                    latest_diff = macd_diff.iloc[-1]
                    if latest_diff > 0:
                        bullish_signals += 1
                    else:
                        bearish_signals += 1
            
            # EMA trend signals
            ema_data = indicators.get('ema_trend', {})
            if isinstance(ema_data, dict) and 'strong_trend' in ema_data:
                strong_trend = ema_data['strong_trend']
                if not strong_trend.empty and strong_trend.iloc[-1]:
                    bullish_signals += 1
            
            if bullish_signals > bearish_signals:
                return 'bullish'
            elif bearish_signals > bullish_signals:
                return 'bearish'
            else:
                return 'neutral'
                
        except Exception as e:
            logger.error(f"Error determining signal direction: {e}")
            return 'neutral'
    
    def _calculate_signal_strength_from_indicators(self, indicators: Dict[str, pd.Series]) -> float:
        """Calculate signal strength from indicators"""
        try:
            strength = 0
            
            # RSI strength
            rsi = indicators.get('rsi', pd.Series(dtype=float))
            if not rsi.empty:
                latest_rsi = rsi.iloc[-1]
                if 30 <= latest_rsi <= 70:
                    strength += 25
                elif 40 <= latest_rsi <= 60:
                    strength += 35
            
            # MACD strength
            macd_data = indicators.get('macd', {})
            if isinstance(macd_data, dict) and 'macd_diff' in macd_data:
                macd_diff = macd_data['macd_diff']
                if not macd_diff.empty:
                    latest_diff = abs(macd_diff.iloc[-1])
                    strength += min(25, latest_diff * 10)
            
            # ADX strength
            adx_data = indicators.get('adx', {})
            if isinstance(adx_data, dict) and 'adx' in adx_data:
                adx = adx_data['adx']
                if not adx.empty:
                    latest_adx = adx.iloc[-1]
                    strength += min(25, latest_adx)
            
            return min(100, strength)
            
        except Exception as e:
            logger.error(f"Error calculating signal strength: {e}")
            return 0
    
    def _calculate_volatility_metric(self, data: pd.DataFrame, indicators: Dict[str, pd.Series]) -> float:
        """Calculate volatility metric"""
        try:
            atr = indicators.get('atr', pd.Series(dtype=float))
            if not atr.empty:
                latest_atr = atr.iloc[-1]
                avg_atr = atr.mean()
                return (latest_atr / avg_atr) if avg_atr > 0 else 1.0
            return 1.0
        except Exception as e:
            logger.error(f"Error calculating volatility metric: {e}")
            return 1.0
    
    def clear_cache(self):
        """Clear indicator cache"""
        self._indicator_cache.clear()
        self._cache_timestamps.clear()
        logger.info("Technical indicators cache cleared")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics"""
        return {
            "cached_items": len(self._indicator_cache),
            "cache_hits": 0,  # TODO: Implement cache hit tracking
            "cache_misses": 0  # TODO: Implement cache miss tracking
        }

# Backward compatibility
TechnicalIndicators = OptimizedTechnicalIndicators 