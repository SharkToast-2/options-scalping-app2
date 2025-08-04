"""
Trade logging module for options scalping
"""

import pandas as pd
import csv
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
import numpy as np

from config.settings import DB_CONFIG

logger = logging.getLogger(__name__)

class TradeLogger:
    """Trade logging and CSV export functionality"""
    
    def __init__(self):
        self.log_file = DB_CONFIG["PATH"]
        self.trade_history = []
        
        # Create log file if it doesn't exist
        self._initialize_log_file()
    
    def _initialize_log_file(self):
        """Initialize the CSV log file with headers"""
        try:
            if not os.path.exists(self.log_file):
                headers = [
                    'timestamp', 'symbol', 'option_type', 'strike_price', 'expiration',
                    'entry_price', 'exit_price', 'quantity', 'entry_time', 'exit_time',
                    'realized_pnl', 'unrealized_pnl', 'status', 'signal_strength',
                    'profit_target', 'stop_loss', 'exit_reason'
                ]
                
                with open(self.log_file, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                
                logger.info(f"Created trade log file: {self.log_file}")
                
        except Exception as e:
            logger.error(f"Error initializing log file: {e}")
    
    def log_trade(self, trade: Dict, action: str, additional_data: Dict = None):
        """Log a trade action"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action': action,
                'trade_data': trade.copy(),
                'additional_data': additional_data or {}
            }
            
            # Add to in-memory history
            self.trade_history.append(log_entry)
            
            # Write to CSV file
            self._write_to_csv(trade, action, additional_data)
            
            logger.info(f"Logged {action} for {trade.get('symbol', 'Unknown')}")
            
        except Exception as e:
            logger.error(f"Error logging trade: {e}")
    
    def _write_to_csv(self, trade: Dict, action: str, additional_data: Dict = None):
        """Write trade data to CSV file"""
        try:
            row = [
                datetime.now().isoformat(),
                trade.get('symbol', ''),
                trade.get('option_type', ''),
                trade.get('strike_price', ''),
                trade.get('expiration', ''),
                trade.get('entry_price', ''),
                trade.get('exit_price', ''),
                trade.get('quantity', ''),
                trade.get('entry_time', ''),
                trade.get('exit_time', ''),
                trade.get('realized_pnl', ''),
                trade.get('unrealized_pnl', ''),
                trade.get('status', ''),
                additional_data.get('signal_strength', '') if additional_data else '',
                additional_data.get('profit_target', '') if additional_data else '',
                additional_data.get('stop_loss', '') if additional_data else '',
                additional_data.get('exit_reason', '') if additional_data else ''
            ]
            
            with open(self.log_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(row)
                
        except Exception as e:
            logger.error(f"Error writing to CSV: {e}")
    
    def get_trade_history(self, symbol: str = None, days: int = None) -> List[Dict]:
        """Get trade history with optional filters"""
        try:
            history = self.trade_history.copy()
            
            # Filter by symbol
            if symbol:
                history = [trade for trade in history if trade['trade_data'].get('symbol') == symbol]
            
            # Filter by days
            if days:
                cutoff_date = datetime.now() - timedelta(days=days)
                history = [
                    trade for trade in history 
                    if datetime.fromisoformat(trade['timestamp']) > cutoff_date
                ]
            
            return history
            
        except Exception as e:
            logger.error(f"Error getting trade history: {e}")
            return []
    
    def export_trades_to_csv(self, filename: str = None, symbol: str = None, days: int = None):
        """Export trades to a new CSV file"""
        try:
            if not filename:
                filename = f"trade_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            history = self.get_trade_history(symbol, days)
            
            if not history:
                logger.warning("No trades to export")
                return None
            
            # Convert to DataFrame
            df_data = []
            for entry in history:
                trade_data = entry['trade_data'].copy()
                trade_data['action'] = entry['action']
                trade_data['log_timestamp'] = entry['timestamp']
                df_data.append(trade_data)
            
            df = pd.DataFrame(df_data)
            
            # Export to CSV
            df.to_csv(filename, index=False)
            
            logger.info(f"Exported {len(history)} trades to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error exporting trades: {e}")
            return None
    
    def get_performance_summary(self, symbol: str = None, days: int = None) -> Dict:
        """Get performance summary from trade history"""
        try:
            history = self.get_trade_history(symbol, days)
            
            if not history:
                return {
                    'total_trades': 0,
                    'winning_trades': 0,
                    'losing_trades': 0,
                    'win_rate': 0.0,
                    'total_pnl': 0.0,
                    'avg_win': 0.0,
                    'avg_loss': 0.0,
                    'max_win': 0.0,
                    'max_loss': 0.0
                }
            
            # Calculate metrics
            total_trades = len(history)
            pnl_values = [trade['trade_data'].get('realized_pnl', 0) for trade in history]
            
            winning_trades = len([pnl for pnl in pnl_values if pnl > 0])
            losing_trades = len([pnl for pnl in pnl_values if pnl < 0])
            
            win_rate = winning_trades / total_trades if total_trades > 0 else 0
            total_pnl = sum(pnl_values)
            
            wins = [pnl for pnl in pnl_values if pnl > 0]
            losses = [pnl for pnl in pnl_values if pnl < 0]
            
            avg_win = np.mean(wins) if wins else 0
            avg_loss = np.mean(losses) if losses else 0
            max_win = max(wins) if wins else 0
            max_loss = min(losses) if losses else 0
            
            return {
                'total_trades': total_trades,
                'winning_trades': winning_trades,
                'losing_trades': losing_trades,
                'win_rate': win_rate,
                'total_pnl': total_pnl,
                'avg_win': avg_win,
                'avg_loss': avg_loss,
                'max_win': max_win,
                'max_loss': max_loss
            }
            
        except Exception as e:
            logger.error(f"Error getting performance summary: {e}")
            return {}
    
    def log_signal(self, symbol: str, signals: Dict, decision: str):
        """Log signal analysis"""
        try:
            signal_log = {
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol,
                'signals': signals,
                'decision': decision
            }
            
            # Store in memory (could also write to separate signal log file)
            if not hasattr(self, 'signal_logs'):
                self.signal_logs = []
            
            self.signal_logs.append(signal_log)
            
            # Keep only last 1000 signal logs
            if len(self.signal_logs) > 1000:
                self.signal_logs = self.signal_logs[-1000:]
                
        except Exception as e:
            logger.error(f"Error logging signal: {e}")
    
    def get_signal_history(self, symbol: str = None, hours: int = 24) -> List[Dict]:
        """Get signal history"""
        try:
            if not hasattr(self, 'signal_logs'):
                return []
            
            history = self.signal_logs.copy()
            
            # Filter by symbol
            if symbol:
                history = [log for log in history if log.get('symbol') == symbol]
            
            # Filter by time
            if hours:
                cutoff_time = datetime.now() - timedelta(hours=hours)
                history = [
                    log for log in history 
                    if datetime.fromisoformat(log['timestamp']) > cutoff_time
                ]
            
            return history
            
        except Exception as e:
            logger.error(f"Error getting signal history: {e}")
            return [] 