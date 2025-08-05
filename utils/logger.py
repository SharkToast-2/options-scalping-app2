#!/usr/bin/env python3
"""
Logging utilities for Options Scalping Bot
"""

import logging
import os
from datetime import datetime
from typing import Optional

def setup_logger(name: str, level: int = logging.INFO, log_file: Optional[str] = None) -> logging.Logger:
    """Setup a logger with console and file handlers"""
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatters
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_bot_logger() -> logging.Logger:
    """Get the main bot logger"""
    log_file = f"logs/options_bot_{datetime.now().strftime('%Y%m%d')}.log"
    return setup_logger('options_bot', log_file=log_file)

def get_trade_logger() -> logging.Logger:
    """Get the trade logger"""
    log_file = f"logs/trades_{datetime.now().strftime('%Y%m%d')}.log"
    return setup_logger('trades', log_file=log_file)

def log_trade(logger: logging.Logger, trade_data: dict):
    """Log a trade with structured data"""
    try:
        trade_info = (
            f"TRADE: {trade_data.get('action', 'UNKNOWN')} "
            f"{trade_data.get('ticker', 'UNKNOWN')} "
            f"@ ${trade_data.get('price', 0):.2f} "
            f"Size: {trade_data.get('size', 0)} "
            f"P&L: ${trade_data.get('pnl', 0):.2f} "
            f"Reason: {trade_data.get('reason', 'N/A')}"
        )
        logger.info(trade_info)
        
    except Exception as e:
        logger.error(f"Error logging trade: {e}")

def log_signal(logger: logging.Logger, signal_data: dict):
    """Log a trading signal"""
    try:
        signal_info = (
            f"SIGNAL: {signal_data.get('ticker', 'UNKNOWN')} "
            f"{signal_data.get('action', 'UNKNOWN')} "
            f"Confidence: {signal_data.get('confidence', 0)}% "
            f"Reasons: {', '.join(signal_data.get('reasons', []))}"
        )
        logger.info(signal_info)
        
    except Exception as e:
        logger.error(f"Error logging signal: {e}")

def log_performance(logger: logging.Logger, performance_data: dict):
    """Log performance metrics"""
    try:
        perf_info = (
            f"PERFORMANCE: "
            f"Trades: {performance_data.get('total_trades', 0)} "
            f"Win Rate: {performance_data.get('win_rate', 0):.1f}% "
            f"Total P&L: ${performance_data.get('total_pnl', 0):.2f} "
            f"Daily P&L: ${performance_data.get('daily_pnl', 0):.2f}"
        )
        logger.info(perf_info)
        
    except Exception as e:
        logger.error(f"Error logging performance: {e}")

def log_error(logger: logging.Logger, error: Exception, context: str = ""):
    """Log an error with context"""
    try:
        error_info = f"ERROR {context}: {type(error).__name__}: {str(error)}"
        logger.error(error_info, exc_info=True)
        
    except Exception as e:
        logger.error(f"Error logging error: {e}")

def log_warning(logger: logging.Logger, message: str, context: str = ""):
    """Log a warning with context"""
    try:
        warning_info = f"WARNING {context}: {message}"
        logger.warning(warning_info)
        
    except Exception as e:
        logger.error(f"Error logging warning: {e}")

def log_info(logger: logging.Logger, message: str, context: str = ""):
    """Log an info message with context"""
    try:
        info_message = f"INFO {context}: {message}"
        logger.info(info_message)
        
    except Exception as e:
        logger.error(f"Error logging info: {e}")

def log_debug(logger: logging.Logger, message: str, context: str = ""):
    """Log a debug message with context"""
    try:
        debug_message = f"DEBUG {context}: {message}"
        logger.debug(debug_message)
        
    except Exception as e:
        logger.error(f"Error logging debug: {e}")

def create_log_rotation():
    """Create log rotation for old log files"""
    try:
        import glob
        from datetime import datetime, timedelta
        
        # Keep logs for 7 days
        cutoff_date = datetime.now() - timedelta(days=7)
        
        # Find old log files
        log_patterns = [
            "logs/options_bot_*.log",
            "logs/trades_*.log",
            "logs/*.log"
        ]
        
        for pattern in log_patterns:
            for log_file in glob.glob(pattern):
                try:
                    # Extract date from filename
                    filename = os.path.basename(log_file)
                    if '_' in filename:
                        date_str = filename.split('_')[-1].replace('.log', '')
                        file_date = datetime.strptime(date_str, '%Y%m%d')
                        
                        # Remove old files
                        if file_date < cutoff_date:
                            os.remove(log_file)
                            print(f"Removed old log file: {log_file}")
                            
                except Exception as e:
                    print(f"Error processing log file {log_file}: {e}")
                    
    except Exception as e:
        print(f"Error in log rotation: {e}")

def get_log_stats(log_file: str) -> dict:
    """Get statistics about a log file"""
    try:
        if not os.path.exists(log_file):
            return {'error': 'Log file not found'}
        
        with open(log_file, 'r') as f:
            lines = f.readlines()
        
        stats = {
            'total_lines': len(lines),
            'error_count': 0,
            'warning_count': 0,
            'info_count': 0,
            'trade_count': 0,
            'signal_count': 0
        }
        
        for line in lines:
            if 'ERROR' in line:
                stats['error_count'] += 1
            elif 'WARNING' in line:
                stats['warning_count'] += 1
            elif 'INFO' in line:
                stats['info_count'] += 1
            
            if 'TRADE:' in line:
                stats['trade_count'] += 1
            elif 'SIGNAL:' in line:
                stats['signal_count'] += 1
        
        return stats
        
    except Exception as e:
        return {'error': str(e)} 