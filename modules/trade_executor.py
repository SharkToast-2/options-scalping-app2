#!/usr/bin/env python3
"""
Trade Executor Module
Handles trade execution and management
"""

import json
from datetime import datetime
from modules.data_fetcher import get_real_time_price

# Global variables for trade management
active_trade = False
open_trades = []
daily_pnl = 0.0
total_trades = 0

def execute_trade(contract, trade_size):
    """
    Execute a trade
    
    Args:
        contract (str): Contract symbol
        trade_size (float): Trade size in dollars
    
    Returns:
        bool: True if trade executed successfully
    """
    global active_trade, open_trades, total_trades
    
    if active_trade:
        print("❌ Already have an active trade")
        return False
    
    try:
        # Get current price
        ticker = contract.split('_')[0]
        current_price = get_real_time_price(ticker)
        
        if current_price == 0:
            print("❌ Could not get current price")
            return False
        
        # Create trade record
        trade = {
            'id': total_trades + 1,
            'symbol': contract,
            'entry_price': current_price,
            'current_price': current_price,
            'trade_size': trade_size,
            'entry_time': datetime.now().isoformat(),
            'status': 'open'
        }
        
        # Add to open trades
        open_trades.append(trade)
        active_trade = True
        total_trades += 1
        
        print(f"✅ Trade executed: {contract} at ${current_price:.2f}")
        print(f"   Trade size: ${trade_size}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error executing trade: {e}")
        return False

def close_trade(trade_id, reason="manual"):
    """
    Close a trade
    
    Args:
        trade_id (int): Trade ID to close
        reason (str): Reason for closing
    
    Returns:
        bool: True if trade closed successfully
    """
    global active_trade, open_trades, daily_pnl
    
    # Find the trade
    trade = None
    for t in open_trades:
        if t['id'] == trade_id:
            trade = t
            break
    
    if not trade:
        print(f"❌ Trade {trade_id} not found")
        return False
    
    try:
        # Get current price
        ticker = trade['symbol'].split('_')[0]
        current_price = get_real_time_price(ticker)
        
        if current_price == 0:
            print("❌ Could not get current price")
            return False
        
        # Calculate P&L
        entry_price = trade['entry_price']
        pnl = ((current_price - entry_price) / entry_price) * trade['trade_size']
        
        # Update trade
        trade['exit_price'] = current_price
        trade['exit_time'] = datetime.now().isoformat()
        trade['status'] = 'closed'
        trade['pnl'] = pnl
        trade['reason'] = reason
        
        # Update daily P&L
        daily_pnl += pnl
        
        # Remove from open trades
        open_trades = [t for t in open_trades if t['id'] != trade_id]
        
        # Update active trade status
        if not open_trades:
            active_trade = False
        
        print(f"✅ Trade closed: {trade['symbol']}")
        print(f"   Entry: ${entry_price:.2f}, Exit: ${current_price:.2f}")
        print(f"   P&L: ${pnl:.2f}")
        print(f"   Reason: {reason}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error closing trade: {e}")
        return False

def get_open_trades():
    """
    Get list of open trades
    
    Returns:
        list: List of open trades
    """
    return open_trades

def trade_active():
    """
    Check if there's an active trade
    
    Returns:
        bool: True if there's an active trade
    """
    return active_trade

def check_total_loss():
    """
    Get total daily loss
    
    Returns:
        float: Total daily P&L
    """
    return daily_pnl

def reset_daily_pnl():
    """Reset daily P&L"""
    global daily_pnl
    daily_pnl = 0.0
    print("✅ Daily P&L reset")

def get_trade_history():
    """
    Get complete trade history
    
    Returns:
        list: List of all trades (open and closed)
    """
    # In a real implementation, this would load from a database
    return open_trades

def update_trade_prices():
    """Update current prices for all open trades"""
    global open_trades
    
    for trade in open_trades:
        if trade['status'] == 'open':
            ticker = trade['symbol'].split('_')[0]
            current_price = get_real_time_price(ticker)
            if current_price > 0:
                trade['current_price'] = current_price 