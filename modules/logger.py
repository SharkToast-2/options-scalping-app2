#!/usr/bin/env python3
"""
Logger Module
Handles logging of trades and events
"""

import json
from datetime import datetime
import os

def log_trade(ticker, contract, action, price, trade_size=None, pnl=None):
    """
    Log a trade event
    
    Args:
        ticker (str): Stock ticker
        contract (str): Contract symbol
        action (str): Trade action (BUY/SELL)
        price (float): Trade price
        trade_size (float): Trade size
        pnl (float): Profit/Loss
    """
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'ticker': ticker,
        'contract': contract,
        'action': action,
        'price': price,
        'trade_size': trade_size,
        'pnl': pnl
    }
    
    # Save to log file
    log_file = "trading_log.json"
    
    try:
        # Load existing logs
        logs = []
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        # Add new log entry
        logs.append(log_entry)
        
        # Save back to file
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        print(f"📝 Trade logged: {action} {contract} at ${price:.2f}")
        
    except Exception as e:
        print(f"❌ Error logging trade: {e}")

def log_signal(ticker, signal_type, strength, indicators):
    """
    Log a trading signal
    
    Args:
        ticker (str): Stock ticker
        signal_type (str): Type of signal
        strength (int): Signal strength
        indicators (dict): Technical indicators
    """
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'ticker': ticker,
        'signal_type': signal_type,
        'strength': strength,
        'indicators': indicators
    }
    
    # Save to signal log file
    log_file = "signal_log.json"
    
    try:
        # Load existing logs
        logs = []
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        # Add new log entry
        logs.append(log_entry)
        
        # Save back to file
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        print(f"📊 Signal logged: {signal_type} for {ticker} (strength: {strength})")
        
    except Exception as e:
        print(f"❌ Error logging signal: {e}")

def log_error(error_type, message, details=None):
    """
    Log an error
    
    Args:
        error_type (str): Type of error
        message (str): Error message
        details (dict): Additional error details
    """
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'error_type': error_type,
        'message': message,
        'details': details
    }
    
    # Save to error log file
    log_file = "error_log.json"
    
    try:
        # Load existing logs
        logs = []
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        # Add new log entry
        logs.append(log_entry)
        
        # Save back to file
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        print(f"❌ Error logged: {error_type} - {message}")
        
    except Exception as e:
        print(f"❌ Error logging error: {e}")

def get_trade_history(limit=50):
    """
    Get recent trade history
    
    Args:
        limit (int): Number of trades to return
    
    Returns:
        list: List of recent trades
    """
    log_file = "trading_log.json"
    
    try:
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
            
            # Return most recent trades
            return logs[-limit:] if len(logs) > limit else logs
        else:
            return []
            
    except Exception as e:
        print(f"❌ Error reading trade history: {e}")
        return []

def get_signal_history(limit=50):
    """
    Get recent signal history
    
    Args:
        limit (int): Number of signals to return
    
    Returns:
        list: List of recent signals
    """
    log_file = "signal_log.json"
    
    try:
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
            
            # Return most recent signals
            return logs[-limit:] if len(logs) > limit else logs
        else:
            return []
            
    except Exception as e:
        print(f"❌ Error reading signal history: {e}")
        return []

def clear_logs():
    """Clear all log files"""
    log_files = ["trading_log.json", "signal_log.json", "error_log.json"]
    
    for log_file in log_files:
        try:
            if os.path.exists(log_file):
                os.remove(log_file)
                print(f"🗑️ Cleared {log_file}")
        except Exception as e:
            print(f"❌ Error clearing {log_file}: {e}")

def export_logs(filename="trading_logs_export.json"):
    """
    Export all logs to a single file
    
    Args:
        filename (str): Export filename
    """
    try:
        export_data = {
            'trades': get_trade_history(1000),
            'signals': get_signal_history(1000),
            'export_timestamp': datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"📤 Logs exported to {filename}")
        
    except Exception as e:
        print(f"❌ Error exporting logs: {e}") 