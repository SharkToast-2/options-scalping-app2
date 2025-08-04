"""
Signal processor module for options scalping
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import logging

from config.settings import TRADING_CONFIG, SIGNAL_WEIGHTS

logger = logging.getLogger(__name__)

class SignalProcessor:
    """Process and validate trading signals"""
    
    def __init__(self):
        self.config = TRADING_CONFIG
        self.weights = SIGNAL_WEIGHTS
        self.signal_history = []
    
    def process_signals(self, technical_signals: Dict, sentiment_signals: Dict, 
                       current_price: float, symbol: str) -> Dict:
        """Process and validate all signals"""
        try:
            # Combine all signals
            all_signals = self._combine_signals(technical_signals, sentiment_signals)
            
            # Calculate signal strength
            call_strength = self._calculate_signal_strength(all_signals, 'call')
            put_strength = self._calculate_signal_strength(all_signals, 'put')
            
            # Validate signals
            call_valid = self._validate_signals(all_signals, 'call')
            put_valid = self._validate_signals(all_signals, 'put')
            
            # Generate trading decision
            decision = self._generate_trading_decision(
                call_strength, put_strength, call_valid, put_valid, current_price, symbol
            )
            
            # Store signal history
            self._store_signal_history(all_signals, decision, symbol)
            
            return {
                'call_strength': call_strength,
                'put_strength': put_strength,
                'call_valid': call_valid,
                'put_valid': put_valid,
                'decision': decision,
                'signals': all_signals
            }
            
        except Exception as e:
            logger.error(f"Error processing signals: {e}")
            return {
                'call_strength': 0,
                'put_strength': 0,
                'call_valid': False,
                'put_valid': False,
                'decision': 'HOLD',
                'signals': {}
            }
    
    def _combine_signals(self, technical_signals: Dict, sentiment_signals: Dict) -> Dict:
        """Combine technical and sentiment signals"""
        try:
            combined = {}
            
            # Add technical signals
            for signal_name, signal_value in technical_signals.items():
                combined[f'technical_{signal_name}'] = signal_value
            
            # Add sentiment signals
            for signal_name, signal_value in sentiment_signals.items():
                combined[f'sentiment_{signal_name}'] = signal_value
            
            return combined
            
        except Exception as e:
            logger.error(f"Error combining signals: {e}")
            return {}
    
    def _calculate_signal_strength(self, signals: Dict, direction: str) -> int:
        """Calculate signal strength for call/put direction"""
        try:
            strength = 0
            
            if direction == 'call':
                # Call signals
                call_signals = [
                    'technical_rsi_spike',
                    'technical_macd_trending_up',
                    'technical_price_above_vwap',
                    'technical_ema_trend_up',
                    'technical_bb_width_ok',
                    'technical_adx_strong',
                    'technical_obv_rising',
                    'technical_atr_volatility_ok',
                    'technical_stoch_oversold',
                    'sentiment_call_signal'
                ]
                
                for signal in call_signals:
                    if signals.get(signal, False):
                        weight = self.weights.get(signal.replace('technical_', '').replace('sentiment_', ''), 1.0)
                        strength += weight
            
            elif direction == 'put':
                # Put signals
                put_signals = [
                    'technical_rsi_spike',
                    'technical_macd_trending_down',
                    'technical_price_below_vwap',
                    'technical_ema_trend_down',
                    'technical_bb_width_ok',
                    'technical_adx_strong',
                    'technical_obv_falling',
                    'technical_atr_volatility_ok',
                    'technical_stoch_overbought',
                    'sentiment_put_signal'
                ]
                
                for signal in put_signals:
                    if signals.get(signal, False):
                        weight = self.weights.get(signal.replace('technical_', '').replace('sentiment_', ''), 1.0)
                        strength += weight
            
            return int(strength)
            
        except Exception as e:
            logger.error(f"Error calculating signal strength: {e}")
            return 0
    
    def _validate_signals(self, signals: Dict, direction: str) -> bool:
        """Validate signals for trading"""
        try:
            min_strength = self.config.get('MIN_SIGNAL_STRENGTH', 7)
            
            # Check minimum signal strength
            strength = self._calculate_signal_strength(signals, direction)
            if strength < min_strength:
                return False
            
            # Check for conflicting signals
            if direction == 'call':
                # Check for bearish signals that might conflict
                bearish_conflicts = [
                    'technical_macd_trending_down',
                    'technical_price_below_vwap',
                    'technical_ema_trend_down',
                    'technical_obv_falling',
                    'sentiment_put_signal'
                ]
                
                conflict_count = sum(1 for signal in bearish_conflicts if signals.get(signal, False))
                if conflict_count > 2:  # Too many conflicting signals
                    return False
            
            elif direction == 'put':
                # Check for bullish signals that might conflict
                bullish_conflicts = [
                    'technical_macd_trending_up',
                    'technical_price_above_vwap',
                    'technical_ema_trend_up',
                    'technical_obv_rising',
                    'sentiment_call_signal'
                ]
                
                conflict_count = sum(1 for signal in bullish_conflicts if signals.get(signal, False))
                if conflict_count > 2:  # Too many conflicting signals
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating signals: {e}")
            return False
    
    def _generate_trading_decision(self, call_strength: int, put_strength: int,
                                 call_valid: bool, put_valid: bool,
                                 current_price: float, symbol: str) -> str:
        """Generate trading decision based on signal analysis"""
        try:
            min_strength = self.config.get('MIN_SIGNAL_STRENGTH', 7)
            
            # Check if we have valid signals
            if not call_valid and not put_valid:
                return 'HOLD'
            
            # Compare signal strengths
            if call_valid and put_valid:
                # Both valid, choose the stronger one
                if call_strength > put_strength:
                    return 'CALL'
                elif put_strength > call_strength:
                    return 'PUT'
                else:
                    # Equal strength, check additional criteria
                    return self._break_tie(call_strength, put_strength, current_price, symbol)
            
            elif call_valid:
                return 'CALL'
            elif put_valid:
                return 'PUT'
            else:
                return 'HOLD'
            
        except Exception as e:
            logger.error(f"Error generating trading decision: {e}")
            return 'HOLD'
    
    def _break_tie(self, call_strength: int, put_strength: int,
                  current_price: float, symbol: str) -> str:
        """Break ties when signal strengths are equal"""
        try:
            # Additional criteria for tie-breaking
            # 1. Check recent signal history
            recent_signals = self._get_recent_signals(symbol, hours=1)
            
            if recent_signals:
                call_count = sum(1 for s in recent_signals if s['decision'] == 'CALL')
                put_count = sum(1 for s in recent_signals if s['decision'] == 'PUT')
                
                # Avoid over-trading in one direction
                if call_count > put_count:
                    return 'PUT'
                elif put_count > call_count:
                    return 'CALL'
            
            # 2. Check time of day (avoid trading near market close)
            current_hour = datetime.now().hour
            if current_hour >= 15:  # After 3 PM
                return 'HOLD'  # Be more conservative near close
            
            # 3. Default to HOLD if no clear preference
            return 'HOLD'
            
        except Exception as e:
            logger.error(f"Error breaking tie: {e}")
            return 'HOLD'
    
    def _get_recent_signals(self, symbol: str, hours: int = 1) -> List[Dict]:
        """Get recent signal history for a symbol"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent = [
                signal for signal in self.signal_history
                if signal['symbol'] == symbol and signal['timestamp'] > cutoff_time
            ]
            return recent
        except Exception as e:
            logger.error(f"Error getting recent signals: {e}")
            return []
    
    def _store_signal_history(self, signals: Dict, decision: str, symbol: str):
        """Store signal history for analysis"""
        try:
            signal_record = {
                'timestamp': datetime.now(),
                'symbol': symbol,
                'signals': signals,
                'decision': decision
            }
            self.signal_history.append(signal_record)
            
            # Keep only last 1000 records
            if len(self.signal_history) > 1000:
                self.signal_history = self.signal_history[-1000:]
                
        except Exception as e:
            logger.error(f"Error storing signal history: {e}")
    
    def get_signal_quality_score(self, signals: Dict, direction: str) -> float:
        """Calculate signal quality score (0-1)"""
        try:
            strength = self._calculate_signal_strength(signals, direction)
            max_possible = sum(self.weights.values())
            
            if max_possible == 0:
                return 0.0
            
            quality_score = strength / max_possible
            
            # Apply additional quality factors
            quality_factors = []
            
            # Check signal consistency
            consistency = self._check_signal_consistency(signals, direction)
            quality_factors.append(consistency)
            
            # Check signal timing
            timing = self._check_signal_timing(signals)
            quality_factors.append(timing)
            
            # Average quality factors
            avg_quality = np.mean(quality_factors) if quality_factors else 1.0
            
            return quality_score * avg_quality
            
        except Exception as e:
            logger.error(f"Error calculating signal quality: {e}")
            return 0.0
    
    def _check_signal_consistency(self, signals: Dict, direction: str) -> float:
        """Check consistency of signals"""
        try:
            if direction == 'call':
                bullish_signals = [
                    'technical_macd_trending_up',
                    'technical_price_above_vwap',
                    'technical_ema_trend_up',
                    'technical_obv_rising',
                    'sentiment_call_signal'
                ]
                
                bullish_count = sum(1 for signal in bullish_signals if signals.get(signal, False))
                return bullish_count / len(bullish_signals)
            
            elif direction == 'put':
                bearish_signals = [
                    'technical_macd_trending_down',
                    'technical_price_below_vwap',
                    'technical_ema_trend_down',
                    'technical_obv_falling',
                    'sentiment_put_signal'
                ]
                
                bearish_count = sum(1 for signal in bearish_signals if signals.get(signal, False))
                return bearish_count / len(bearish_signals)
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Error checking signal consistency: {e}")
            return 0.0
    
    def _check_signal_timing(self, signals: Dict) -> float:
        """Check timing quality of signals"""
        try:
            # Check if signals are recent and relevant
            # This is a simplified version - in practice, you'd check actual timing
            
            # For now, return a default score
            return 0.8
            
        except Exception as e:
            logger.error(f"Error checking signal timing: {e}")
            return 0.0
    
    def get_signal_summary(self, symbol: str, hours: int = 24) -> Dict:
        """Get signal summary for analysis"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_signals = [
                signal for signal in self.signal_history
                if signal['symbol'] == symbol and signal['timestamp'] > cutoff_time
            ]
            
            if not recent_signals:
                return {
                    'total_signals': 0,
                    'call_signals': 0,
                    'put_signals': 0,
                    'hold_signals': 0,
                    'avg_signal_strength': 0.0
                }
            
            decisions = [signal['decision'] for signal in recent_signals]
            
            return {
                'total_signals': len(recent_signals),
                'call_signals': decisions.count('CALL'),
                'put_signals': decisions.count('PUT'),
                'hold_signals': decisions.count('HOLD'),
                'avg_signal_strength': np.mean([
                    self._calculate_signal_strength(signal['signals'], 'call') +
                    self._calculate_signal_strength(signal['signals'], 'put')
                    for signal in recent_signals
                ])
            }
            
        except Exception as e:
            logger.error(f"Error getting signal summary: {e}")
            return {
                'total_signals': 0,
                'call_signals': 0,
                'put_signals': 0,
                'hold_signals': 0,
                'avg_signal_strength': 0.0
            } 