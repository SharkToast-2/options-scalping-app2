#!/usr/bin/env python3
"""
Risk Manager Module
Manages risk and exit conditions for trades
"""

from modules.trade_executor import active_trade, close_trade, get_open_trades
from modules.data_fetcher import get_real_time_price
from datetime import datetime, timedelta

def check_exit_conditions(open_trades, profit_target=3, stop_loss=3):
    """
    Check exit conditions for all open trades
    
    Args:
        open_trades (list): List of open trades
        profit_target (float): Profit target percentage
        stop_loss (float): Stop loss percentage
    """
    for trade in open_trades:
        if trade['status'] != 'open':
            continue
        
        # Get current price
        ticker = trade['symbol'].split('_')[0]
        current_price = get_real_time_price(ticker)
        
        if current_price == 0:
            continue
        
        # Calculate price change
        entry_price = trade['entry_price']
        price_change_pct = ((current_price - entry_price) / entry_price) * 100
        
        # Check profit target
        if price_change_pct >= profit_target:
            close_trade(trade['id'], f"profit_target_{profit_target}%")
            continue
        
        # Check stop loss
        if price_change_pct <= -stop_loss:
            close_trade(trade['id'], f"stop_loss_{stop_loss}%")
            continue
        
        # Check time-based exit (5 minutes max)
        entry_time = datetime.fromisoformat(trade['entry_time'])
        current_time = datetime.now()
        time_in_trade = current_time - entry_time
        
        if time_in_trade >= timedelta(minutes=5):
            close_trade(trade['id'], "time_limit_5min")
            continue

def check_daily_loss_limit(daily_pnl, max_daily_loss=500):
    """
    Check if daily loss limit has been reached
    
    Args:
        daily_pnl (float): Current daily P&L
        max_daily_loss (float): Maximum daily loss allowed
    
    Returns:
        bool: True if loss limit reached
    """
    return daily_pnl <= -max_daily_loss

def check_position_size(trade_size, max_position_size=500):
    """
    Check if position size is within limits
    
    Args:
        trade_size (float): Proposed trade size
        max_position_size (float): Maximum position size allowed
    
    Returns:
        bool: True if position size is acceptable
    """
    return trade_size <= max_position_size

def calculate_position_size(account_balance, risk_per_trade=0.02):
    """
    Calculate position size based on account balance and risk
    
    Args:
        account_balance (float): Account balance
        risk_per_trade (float): Risk per trade as percentage of account
    
    Returns:
        float: Recommended position size
    """
    return account_balance * risk_per_trade

def check_market_conditions(ticker):
    """
    Check if market conditions are suitable for trading
    
    Args:
        ticker (str): Stock ticker
    
    Returns:
        bool: True if market conditions are good
    """
    try:
        # Get current price
        current_price = get_real_time_price(ticker)
        
        if current_price == 0:
            return False
        
        # Check if market is open (simplified check)
        now = datetime.now()
        if now.hour < 9 or now.hour >= 16:  # Outside market hours
            return False
        
        # Check if it's a weekend
        if now.weekday() >= 5:  # Saturday = 5, Sunday = 6
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking market conditions: {e}")
        return False

def validate_trade_parameters(ticker, trade_size, max_trade_size=500):
    """
    Validate trade parameters before execution
    
    Args:
        ticker (str): Stock ticker
        trade_size (float): Trade size
        max_trade_size (float): Maximum trade size
    
    Returns:
        tuple: (is_valid, error_message)
    """
    # Check if already have an active trade
    if active_trade:
        return False, "Already have an active trade"
    
    # Check position size
    if not check_position_size(trade_size, max_trade_size):
        return False, f"Trade size ${trade_size} exceeds maximum ${max_trade_size}"
    
    # Check market conditions
    if not check_market_conditions(ticker):
        return False, "Market conditions not suitable for trading"
    
    return True, "Trade parameters valid"

def get_risk_summary():
    """
    Get current risk summary
    
    Returns:
        dict: Risk summary information
    """
    open_trades = get_open_trades()
    
    total_exposure = sum(trade['trade_size'] for trade in open_trades)
    num_open_trades = len(open_trades)
    
    return {
        'open_trades': num_open_trades,
        'total_exposure': total_exposure,
        'max_exposure': 500,  # Maximum allowed exposure
        'exposure_ratio': total_exposure / 500 if 500 > 0 else 0
    } 