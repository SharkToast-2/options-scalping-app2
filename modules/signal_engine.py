#!/usr/bin/env python3
"""
Optimized Signal Engine Module
Generates trading signals based on technical indicators with enhanced scalping logic
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class SignalResult:
    """Structured signal result"""
    should_buy: bool
    should_sell: bool
    signal_strength: int
    confidence: float
    signals: Dict[str, bool]
    indicators: Dict[str, float]
    timestamp: datetime

class OptimizedSignalEngine:
    """Optimized signal engine with enhanced scalping capabilities"""
    
    def __init__(self):
        self.signal_history = []
        self.performance_metrics = {
            'total_signals': 0,
            'successful_signals': 0,
            'false_positives': 0
        }
    
    def check_signals(self, indicators: Dict) -> Dict[str, bool]:
        """
        Enhanced signal checking with optimized logic for scalping
        
        Args:
            indicators (dict): Dictionary of technical indicators
        
        Returns:
            dict: Dictionary of signal conditions (True/False)
        """
        if not indicators:
            return self._get_default_signals()
        
        signals = {}
        
        # Enhanced RSI signal with momentum confirmation
        rsi = indicators.get('rsi', 50)
        rsi_momentum = indicators.get('rsi_momentum', 0)
        signals['rsi_signal'] = self._check_rsi_signal(rsi, rsi_momentum)
        
        # Enhanced MACD signal with volume confirmation
        macd = indicators.get('macd', 0)
        macd_signal = indicators.get('macd_signal', 0)
        macd_histogram = indicators.get('macd_histogram', 0)
        volume_ratio = indicators.get('volume_ratio', 1)
        signals['macd_signal'] = self._check_macd_signal(macd, macd_signal, macd_histogram, volume_ratio)
        
        # Enhanced volume signal with price action
        price_change_pct = indicators.get('price_change_pct', 0)
        signals['volume_signal'] = self._check_volume_signal(volume_ratio, price_change_pct)
        
        # Enhanced momentum signal with multiple confirmations
        sma_20 = indicators.get('sma_20', 0)
        sma_50 = indicators.get('sma_50', 0)
        current_price = indicators.get('current_price', 0)
        signals['momentum_signal'] = self._check_momentum_signal(
            price_change_pct, sma_20, sma_50, current_price
        )
        
        # New: Volatility signal for scalping
        atr = indicators.get('atr', 0)
        bb_width = indicators.get('bb_width', 0)
        signals['volatility_signal'] = self._check_volatility_signal(atr, bb_width)
        
        # New: Support/Resistance signal
        bb_upper = indicators.get('bb_upper', 0)
        bb_lower = indicators.get('bb_lower', 0)
        signals['support_resistance_signal'] = self._check_support_resistance_signal(
            current_price, bb_upper, bb_lower
        )
        
        return signals
    
    def _check_rsi_signal(self, rsi: float, rsi_momentum: float) -> bool:
        """Enhanced RSI signal with momentum confirmation"""
        # Oversold condition with positive momentum
        if rsi < 35 and rsi_momentum > 0:
            return True
        # RSI crossing above 30 with volume
        if 30 <= rsi <= 40 and rsi_momentum > 2:
            return True
        return False
    
    def _check_macd_signal(self, macd: float, macd_signal: float, 
                          macd_histogram: float, volume_ratio: float) -> bool:
        """Enhanced MACD signal with volume confirmation"""
        # Positive crossover with increasing histogram
        if macd > macd_signal and macd_histogram > 0 and volume_ratio > 1.2:
            return True
        # MACD above signal line and positive
        if macd > 0 and macd > macd_signal and volume_ratio > 1.5:
            return True
        return False
    
    def _check_volume_signal(self, volume_ratio: float, price_change_pct: float) -> bool:
        """Enhanced volume signal with price action confirmation"""
        # High volume with positive price action
        if volume_ratio > 1.3 and price_change_pct > 0.3:
            return True
        # Very high volume (potential breakout)
        if volume_ratio > 2.0:
            return True
        return False
    
    def _check_momentum_signal(self, price_change_pct: float, sma_20: float, 
                              sma_50: float, current_price: float) -> bool:
        """Enhanced momentum signal with multiple confirmations"""
        # Price above both moving averages with positive momentum
        if (current_price > sma_20 > sma_50 and price_change_pct > 0.2):
            return True
        # Strong positive momentum
        if price_change_pct > 0.5:
            return True
        return False
    
    def _check_volatility_signal(self, atr: float, bb_width: float) -> bool:
        """Volatility signal for scalping opportunities"""
        # Moderate volatility (good for scalping)
        if 0.01 <= atr <= 0.05 and bb_width > 0.02:
            return True
        return False
    
    def _check_support_resistance_signal(self, current_price: float, 
                                       bb_upper: float, bb_lower: float) -> bool:
        """Support/Resistance signal based on Bollinger Bands"""
        # Price near lower band (potential bounce)
        if current_price <= bb_lower * 1.01:
            return True
        # Price breaking above upper band with momentum
        if current_price > bb_upper:
            return True
        return False
    
    def _get_default_signals(self) -> Dict[str, bool]:
        """Get default signal values"""
        return {
            'rsi_signal': False,
            'macd_signal': False,
            'volume_signal': False,
            'momentum_signal': False,
            'volatility_signal': False,
            'support_resistance_signal': False
        }
    
    def get_signal_strength(self, indicators: Dict) -> int:
        """
        Enhanced signal strength calculation (0-100)
        
        Args:
            indicators (dict): Dictionary of technical indicators
        
        Returns:
            int: Signal strength (0-100)
        """
        if not indicators:
            return 0
        
        strength = 0
        signals = self.check_signals(indicators)
        
        # Base strength from signal count
        signal_count = sum(signals.values())
        strength += signal_count * 15  # 15 points per signal
        
        # RSI contribution (0-20 points)
        rsi = indicators.get('rsi', 50)
        if rsi < 25:
            strength += 20
        elif rsi < 30:
            strength += 15
        elif rsi < 35:
            strength += 10
        
        # MACD contribution (0-20 points)
        macd = indicators.get('macd', 0)
        macd_signal = indicators.get('macd_signal', 0)
        if macd > macd_signal and macd > 0:
            strength += 20
        elif macd > macd_signal:
            strength += 15
        
        # Volume contribution (0-20 points)
        volume_ratio = indicators.get('volume_ratio', 1)
        if volume_ratio > 2.5:
            strength += 20
        elif volume_ratio > 2.0:
            strength += 15
        elif volume_ratio > 1.5:
            strength += 10
        
        # Momentum contribution (0-20 points)
        price_change_pct = indicators.get('price_change_pct', 0)
        if price_change_pct > 1.0:
            strength += 20
        elif price_change_pct > 0.5:
            strength += 15
        elif price_change_pct > 0.2:
            strength += 10
        
        return min(strength, 100)
    
    def should_buy(self, indicators: Dict, min_strength: int = 60) -> bool:
        """
        Enhanced buy decision with optimized logic
        
        Args:
            indicators (dict): Dictionary of technical indicators
            min_strength (int): Minimum signal strength required
        
        Returns:
            bool: True if should buy, False otherwise
        """
        signals = self.check_signals(indicators)
        strength = self.get_signal_strength(indicators)
        
        # Require at least 3 positive signals and strength above threshold
        positive_signals = sum(signals.values())
        return positive_signals >= 3 and strength >= min_strength
    
    def should_sell(self, indicators: Dict, entry_price: float, 
                   current_price: float, profit_target: float = 3, 
                   stop_loss: float = 3, time_in_trade: timedelta = None) -> bool:
        """
        Enhanced sell decision with multiple exit conditions
        
        Args:
            indicators (dict): Dictionary of technical indicators
            entry_price (float): Entry price
            current_price (float): Current price
            profit_target (float): Profit target percentage
            stop_loss (float): Stop loss percentage
            time_in_trade (timedelta): Time spent in trade
        
        Returns:
            bool: True if should sell, False otherwise
        """
        if not entry_price or not current_price:
            return False
        
        # Calculate price change
        price_change_pct = ((current_price - entry_price) / entry_price) * 100
        
        # Check profit target
        if price_change_pct >= profit_target:
            return True
        
        # Check stop loss
        if price_change_pct <= -stop_loss:
            return True
        
        # Time-based exit (3 minutes for scalping)
        if time_in_trade and time_in_trade >= timedelta(minutes=3):
            return True
        
        # Technical exit signals
        rsi = indicators.get('rsi', 50)
        if rsi > 75:  # Overbought condition
            return True
        
        # MACD bearish crossover
        macd = indicators.get('macd', 0)
        macd_signal = indicators.get('macd_signal', 0)
        if macd < macd_signal and macd < 0:
            return True
        
        # Volume drying up
        volume_ratio = indicators.get('volume_ratio', 1)
        if volume_ratio < 0.7:
            return True
        
        return False
    
    def get_signal_confidence(self, indicators: Dict) -> float:
        """
        Calculate signal confidence (0.0-1.0)
        
        Args:
            indicators (dict): Dictionary of technical indicators
        
        Returns:
            float: Confidence level (0.0-1.0)
        """
        strength = self.get_signal_strength(indicators)
        signals = self.check_signals(indicators)
        
        # Base confidence from strength
        confidence = strength / 100.0
        
        # Boost confidence based on signal alignment
        positive_signals = sum(signals.values())
        if positive_signals >= 4:
            confidence *= 1.2
        elif positive_signals >= 3:
            confidence *= 1.1
        
        # Reduce confidence for extreme conditions
        rsi = indicators.get('rsi', 50)
        if rsi < 20 or rsi > 80:
            confidence *= 0.8
        
        return min(confidence, 1.0)
    
    def update_performance_metrics(self, signal_result: SignalResult, 
                                 trade_outcome: str):
        """Update performance metrics based on trade outcome"""
        self.performance_metrics['total_signals'] += 1
        
        if trade_outcome == 'profit':
            self.performance_metrics['successful_signals'] += 1
        elif trade_outcome == 'loss':
            self.performance_metrics['false_positives'] += 1

# Global instance for backward compatibility
signal_engine = OptimizedSignalEngine()

def check_signals(indicators):
    """Backward compatibility function"""
    return signal_engine.check_signals(indicators)

def get_signal_strength(indicators):
    """Backward compatibility function"""
    return signal_engine.get_signal_strength(indicators)

def should_buy(indicators, min_strength=60):
    """Backward compatibility function"""
    return signal_engine.should_buy(indicators, min_strength)

def should_sell(indicators, entry_price, current_price, profit_target=3, stop_loss=3):
    """Backward compatibility function"""
    return signal_engine.should_sell(indicators, entry_price, current_price, profit_target, stop_loss) 