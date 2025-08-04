"""
Risk management module for options scalping
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

from config.settings import TRADING_CONFIG, RISK_CONFIG

logger = logging.getLogger(__name__)

class RiskManager:
    """Risk management for options trading"""
    
    def __init__(self):
        self.config = TRADING_CONFIG
        self.risk_config = RISK_CONFIG
        self.daily_pnl = 0.0
        self.position_history = []
        self.initial_balance = 27200.0  # Default initial balance
        self.current_balance = 27200.0  # Current account balance
        self.trading_enabled = True     # Trading status
        self.balance_protection_triggered = False  # Balance protection status
    
    def calculate_position_size(self, option_price: float, max_size: float = None) -> int:
        """Calculate position size based on risk parameters"""
        try:
            max_size = max_size or self.config["MAX_POSITION_SIZE"]
            
            # Calculate quantity based on max position size
            quantity = int(max_size / option_price)
            
            # Ensure minimum quantity
            if quantity < 1:
                return 0
            
            return quantity
            
        except Exception as e:
            logger.error(f"Error calculating position size: {e}")
            return 0
    
    def check_risk_limits(self, symbol: str, option_type: str, quantity: int, 
                         option_price: float) -> Dict:
        """Check if trade meets risk limits"""
        try:
            checks = {
                'position_size_ok': True,
                'daily_loss_ok': True,
                'concurrent_positions_ok': True,
                'liquidity_ok': True,
                'spread_ok': True,
                'account_balance_ok': True,
                'trading_enabled': True
            }
            
            # Check if trading is enabled
            if not self.trading_enabled:
                checks['trading_enabled'] = False
            
            # Check position size
            position_value = quantity * option_price
            if position_value > self.config["MAX_POSITION_SIZE"]:
                checks['position_size_ok'] = False
            
            # Check daily loss limit
            if self.daily_pnl < -self.config["MAX_DAILY_LOSS"]:
                checks['daily_loss_ok'] = False
            
            # Check concurrent positions
            active_positions = self.get_active_positions()
            if len(active_positions) >= self.config["MAX_CONCURRENT_POSITIONS"]:
                checks['concurrent_positions_ok'] = False
            
            # Check account balance protection
            min_balance = self.config["MIN_ACCOUNT_BALANCE"]
            buffer = self.config["ACCOUNT_BALANCE_BUFFER"]
            required_balance = min_balance + buffer
            
            if self.current_balance < required_balance:
                checks['account_balance_ok'] = False
                if not self.balance_protection_triggered:
                    self.balance_protection_triggered = True
                    self.trading_enabled = False
                    logger.warning(f"Account balance protection triggered! Current: ${self.current_balance:.2f}, Required: ${required_balance:.2f}")
            
            # All checks passed
            all_ok = all(checks.values())
            
            return {
                'trade_allowed': all_ok,
                'checks': checks,
                'position_value': position_value,
                'current_balance': self.current_balance,
                'required_balance': required_balance
            }
            
        except Exception as e:
            logger.error(f"Error checking risk limits: {e}")
            return {
                'trade_allowed': False,
                'checks': {},
                'position_value': 0,
                'current_balance': self.current_balance,
                'required_balance': 0
            }
    
    def get_active_positions(self) -> List[Dict]:
        """Get currently active positions"""
        try:
            return [pos for pos in self.position_history if pos['status'] == 'open']
        except Exception as e:
            logger.error(f"Error getting active positions: {e}")
            return []
    
    def update_daily_pnl(self, pnl: float):
        """Update daily P&L"""
        try:
            self.daily_pnl += pnl
        except Exception as e:
            logger.error(f"Error updating daily P&L: {e}")
    
    def reset_daily_pnl(self):
        """Reset daily P&L (call at start of new day)"""
        try:
            self.daily_pnl = 0.0
        except Exception as e:
            logger.error(f"Error resetting daily P&L: {e}")
    
    def add_position(self, position: Dict):
        """Add new position to history"""
        try:
            self.position_history.append(position)
        except Exception as e:
            logger.error(f"Error adding position: {e}")
    
    def close_position(self, position_id: str, exit_price: float, exit_time: datetime):
        """Close a position"""
        try:
            for position in self.position_history:
                if position.get('id') == position_id and position['status'] == 'open':
                    position['status'] = 'closed'
                    position['exit_price'] = exit_price
                    position['exit_time'] = exit_time
                    position['realized_pnl'] = self.calculate_pnl(position, exit_price)
                    break
        except Exception as e:
            logger.error(f"Error closing position: {e}")
    
    def calculate_pnl(self, position: Dict, current_price: float) -> float:
        """Calculate P&L for a position"""
        try:
            if position['option_type'] == 'call':
                pnl = (current_price - position['entry_price']) * position['quantity']
            else:  # put
                pnl = (position['entry_price'] - current_price) * position['quantity']
            
            return pnl
            
        except Exception as e:
            logger.error(f"Error calculating P&L: {e}")
            return 0.0
    
    def set_initial_balance(self, balance: float):
        """Set the initial account balance"""
        try:
            self.initial_balance = balance
            self.current_balance = balance
            logger.info(f"Initial account balance set to: ${balance:.2f}")
        except Exception as e:
            logger.error(f"Error setting initial balance: {e}")
    
    def update_account_balance(self, pnl: float):
        """Update account balance with P&L"""
        try:
            self.current_balance += pnl
            self.daily_pnl += pnl
            
            # Check if balance protection should be triggered
            min_balance = self.config["MIN_ACCOUNT_BALANCE"]
            buffer = self.config["ACCOUNT_BALANCE_BUFFER"]
            required_balance = min_balance + buffer
            
            if self.current_balance < required_balance and not self.balance_protection_triggered:
                self.balance_protection_triggered = True
                self.trading_enabled = False
                logger.warning(f"🚨 ACCOUNT BALANCE PROTECTION TRIGGERED!")
                logger.warning(f"Current balance: ${self.current_balance:.2f}")
                logger.warning(f"Required minimum: ${required_balance:.2f}")
                logger.warning(f"Trading has been DISABLED for your protection!")
            
            logger.info(f"Account balance updated: ${self.current_balance:.2f} (P&L: ${pnl:.2f})")
            
        except Exception as e:
            logger.error(f"Error updating account balance: {e}")
    
    def get_account_status(self) -> Dict:
        """Get current account status"""
        try:
            min_balance = self.config["MIN_ACCOUNT_BALANCE"]
            buffer = self.config["ACCOUNT_BALANCE_BUFFER"]
            required_balance = min_balance + buffer
            
            return {
                'initial_balance': self.initial_balance,
                'current_balance': self.current_balance,
                'daily_pnl': self.daily_pnl,
                'total_pnl': self.current_balance - self.initial_balance,
                'min_required_balance': required_balance,
                'trading_enabled': self.trading_enabled,
                'balance_protection_triggered': self.balance_protection_triggered,
                'balance_safe': self.current_balance >= required_balance,
                'available_for_trading': self.current_balance - required_balance
            }
        except Exception as e:
            logger.error(f"Error getting account status: {e}")
            return {}
    
    def enable_trading(self):
        """Manually enable trading (use with caution)"""
        try:
            if self.balance_protection_triggered:
                logger.warning("⚠️ Manually enabling trading despite balance protection!")
                logger.warning("This should only be done after careful consideration!")
            
            self.trading_enabled = True
            logger.info("Trading manually enabled")
            
        except Exception as e:
            logger.error(f"Error enabling trading: {e}")
    
    def disable_trading(self):
        """Disable trading"""
        try:
            self.trading_enabled = False
            logger.info("Trading manually disabled")
            
        except Exception as e:
            logger.error(f"Error disabling trading: {e}")
    
    def reset_balance_protection(self, new_balance: float = None):
        """Reset balance protection (use when adding funds)"""
        try:
            if new_balance:
                self.current_balance = new_balance
                logger.info(f"Account balance reset to: ${new_balance:.2f}")
            
            self.balance_protection_triggered = False
            self.trading_enabled = True
            logger.info("Balance protection reset - trading enabled")
            
        except Exception as e:
            logger.error(f"Error resetting balance protection: {e}")
    
    def get_balance_warning_level(self) -> str:
        """Get balance warning level"""
        try:
            min_balance = self.config["MIN_ACCOUNT_BALANCE"]
            buffer = self.config["ACCOUNT_BALANCE_BUFFER"]
            required_balance = min_balance + buffer
            
            if self.current_balance < min_balance:
                return "CRITICAL"
            elif self.current_balance < required_balance:
                return "WARNING"
            elif self.current_balance < (required_balance + buffer):
                return "CAUTION"
            else:
                return "SAFE"
                
        except Exception as e:
            logger.error(f"Error getting balance warning level: {e}")
            return "UNKNOWN" 