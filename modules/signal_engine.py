#!/usr/bin/env python3
"""
Signal Engine Module
Generates trading signals based on technical indicators
"""

def check_signals(indicators):
    """
    Check for trading signals based on indicators
    
    Args:
        indicators (dict): Dictionary of technical indicators
    
    Returns:
        dict: Dictionary of signal conditions (True/False)
    """
    if not indicators:
        return {
            'rsi_signal': False,
            'macd_signal': False,
            'volume_signal': False,
            'momentum_signal': False
        }
    
    signals = {}
    
    # RSI signal (oversold condition for buying)
    rsi = indicators.get('rsi', 50)
    signals['rsi_signal'] = rsi < 30  # Oversold condition
    
    # MACD signal (positive crossover)
    macd = indicators.get('macd', 0)
    macd_signal = indicators.get('macd_signal', 0)
    signals['macd_signal'] = macd > macd_signal and macd > 0
    
    # Volume signal (high volume)
    volume_ratio = indicators.get('volume_ratio', 1)
    signals['volume_signal'] = volume_ratio > 1.5  # 50% above average
    
    # Momentum signal (positive price change)
    price_change_pct = indicators.get('price_change_pct', 0)
    signals['momentum_signal'] = price_change_pct > 0.5  # 0.5% positive change
    
    return signals

def get_signal_strength(indicators):
    """
    Calculate signal strength (0-100)
    
    Args:
        indicators (dict): Dictionary of technical indicators
    
    Returns:
        int: Signal strength (0-100)
    """
    if not indicators:
        return 0
    
    strength = 0
    
    # RSI contribution (0-25 points)
    rsi = indicators.get('rsi', 50)
    if rsi < 30:
        strength += 25
    elif rsi < 40:
        strength += 15
    elif rsi < 50:
        strength += 5
    
    # MACD contribution (0-25 points)
    macd = indicators.get('macd', 0)
    macd_signal = indicators.get('macd_signal', 0)
    if macd > macd_signal and macd > 0:
        strength += 25
    elif macd > macd_signal:
        strength += 15
    
    # Volume contribution (0-25 points)
    volume_ratio = indicators.get('volume_ratio', 1)
    if volume_ratio > 2.0:
        strength += 25
    elif volume_ratio > 1.5:
        strength += 15
    elif volume_ratio > 1.2:
        strength += 10
    
    # Momentum contribution (0-25 points)
    price_change_pct = indicators.get('price_change_pct', 0)
    if price_change_pct > 1.0:
        strength += 25
    elif price_change_pct > 0.5:
        strength += 15
    elif price_change_pct > 0.2:
        strength += 10
    
    return min(strength, 100)

def should_buy(indicators, min_strength=70):
    """
    Determine if we should buy based on indicators
    
    Args:
        indicators (dict): Dictionary of technical indicators
        min_strength (int): Minimum signal strength required
    
    Returns:
        bool: True if should buy, False otherwise
    """
    signals = check_signals(indicators)
    strength = get_signal_strength(indicators)
    
    # All signals must be positive and strength above threshold
    return all(signals.values()) and strength >= min_strength

def should_sell(indicators, entry_price, current_price, profit_target=3, stop_loss=3):
    """
    Determine if we should sell based on indicators and price action
    
    Args:
        indicators (dict): Dictionary of technical indicators
        entry_price (float): Entry price
        current_price (float): Current price
        profit_target (float): Profit target percentage
        stop_loss (float): Stop loss percentage
    
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
    
    # Check technical indicators for exit signals
    rsi = indicators.get('rsi', 50)
    if rsi > 70:  # Overbought condition
        return True
    
    return False 