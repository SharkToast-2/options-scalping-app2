#!/usr/bin/env python3
"""
Automated Options Scalping Bot
Real-time momentum-based options trading with Schwab API integration
"""

import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd

# Import our modules
from config.env_config import get_config
from data.market_data import MarketData
from modules.schwab_auth import SchwabAuth
from signals.technical_indicators import TechnicalIndicators
from signals.sentiment_analysis import SentimentAnalyzer
from utils.logger import setup_logger

class OptionsScalpingBot:
    def __init__(self):
        """Initialize the options scalping bot"""
        self.config = get_config()
        self.logger = setup_logger('options_bot')
        
        # Initialize components
        self.market_data = MarketData()
        self.schwab_auth = SchwabAuth()
        self.indicators = TechnicalIndicators()
        self.sentiment = SentimentAnalyzer()
        
        # Trading parameters
        self.max_trade_amount = 500  # $500 per trade
        self.daily_loss_limit = 500  # $500 daily loss limit
        self.profit_target = 0.05    # 5% profit target
        self.stop_loss = 0.03        # 3% stop loss
        self.max_trade_duration = 5  # 5 minutes max
        
        # Target tickers for options trading
        self.target_tickers = ['META', 'AAPL', 'TSLA', 'NVDA', 'SPY', 'QQQ']
        
        # Bot state
        self.is_running = False
        self.current_position = None
        self.daily_pnl = 0.0
        self.trades_today = []
        self.last_trade_time = None
        
        # Performance tracking
        self.total_trades = 0
        self.winning_trades = 0
        self.total_pnl = 0.0
        
        self.logger.info("Options Scalping Bot initialized")
    
    def start(self):
        """Start the automated trading bot"""
        if not self.check_auth():
            self.logger.error("Schwab authentication required")
            return False
        
        if not self.check_market_hours():
            self.logger.warning("Market is closed")
            return False
        
        self.is_running = True
        self.logger.info("Bot started - monitoring for opportunities")
        
        try:
            while self.is_running:
                self.run_trading_cycle()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            self.logger.info("Bot stopped by user")
            self.stop()
        except Exception as e:
            self.logger.error(f"Bot error: {e}")
            self.stop()
    
    def stop(self):
        """Stop the bot"""
        self.is_running = False
        self.logger.info("Bot stopped")
    
    def check_auth(self) -> bool:
        """Check if Schwab authentication is valid"""
        try:
            auth_status = self.schwab_auth.get_auth_status()
            return auth_status.get('authenticated', False)
        except Exception as e:
            self.logger.error(f"Auth check failed: {e}")
            return False
    
    def check_market_hours(self) -> bool:
        """Check if market is open"""
        now = datetime.now()
        # Simple check - can be enhanced with market calendar
        if now.weekday() >= 5:  # Weekend
            return False
        
        market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
        market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
        
        return market_open <= now <= market_close
    
    def run_trading_cycle(self):
        """Run one trading cycle"""
        try:
            # Check daily limits
            if self.daily_pnl <= -self.daily_loss_limit:
                self.logger.warning(f"Daily loss limit reached: ${self.daily_pnl}")
                self.stop()
                return
            
            # Check if we have an open position
            if self.current_position:
                self.manage_current_position()
            else:
                self.scan_for_opportunities()
                
        except Exception as e:
            self.logger.error(f"Trading cycle error: {e}")
    
    def scan_for_opportunities(self):
        """Scan for trading opportunities"""
        for ticker in self.target_tickers:
            try:
                signal = self.analyze_ticker(ticker)
                if signal['action'] == 'BUY':
                    self.execute_trade(ticker, signal)
                    break  # Only one trade at a time
                    
            except Exception as e:
                self.logger.error(f"Error analyzing {ticker}: {e}")
    
    def analyze_ticker(self, ticker: str) -> Dict:
        """Analyze a ticker for trading signals"""
        try:
            # Get market data
            data = self.market_data.get_stock_data(ticker, "1d")
            if data is None or data.empty:
                return {'action': 'HOLD', 'confidence': 0, 'reason': 'No data'}
            
            # Calculate technical indicators
            indicators = self.indicators.calculate_all_indicators(data)
            
            # Get sentiment
            sentiment_score = self.sentiment.get_sentiment_score(ticker)
            
            # Generate signal
            signal = self.generate_signal(indicators, sentiment_score)
            
            self.logger.info(f"{ticker} analysis: {signal}")
            return signal
            
        except Exception as e:
            self.logger.error(f"Analysis error for {ticker}: {e}")
            return {'action': 'HOLD', 'confidence': 0, 'reason': f'Error: {e}'}
    
    def generate_signal(self, indicators: Dict, sentiment_score: float) -> Dict:
        """Generate trading signal from indicators"""
        try:
            rsi = indicators.get('rsi', 50)
            macd = indicators.get('macd', 0)
            macd_signal = indicators.get('macd_signal', 0)
            bb_upper = indicators.get('bb_upper', 0)
            bb_lower = indicators.get('bb_lower', 0)
            current_price = indicators.get('current_price', 0)
            volume_sma = indicators.get('volume_sma', 1)
            
            confidence = 0
            reasons = []
            
            # Buy signals
            if rsi < 30:
                confidence += 25
                reasons.append("RSI oversold")
            
            if macd > macd_signal:
                confidence += 20
                reasons.append("MACD bullish")
            
            if current_price < bb_lower:
                confidence += 20
                reasons.append("Price below BB")
            
            if volume_sma > 1.5:
                confidence += 15
                reasons.append("High volume")
            
            if sentiment_score > 0.1:
                confidence += 10
                reasons.append("Positive sentiment")
            
            # Sell signals
            if rsi > 70:
                confidence -= 25
                reasons.append("RSI overbought")
            
            if macd < macd_signal:
                confidence -= 20
                reasons.append("MACD bearish")
            
            if current_price > bb_upper:
                confidence -= 20
                reasons.append("Price above BB")
            
            if sentiment_score < -0.1:
                confidence -= 10
                reasons.append("Negative sentiment")
            
            # Determine action
            if confidence >= 50:
                action = 'BUY'
            elif confidence <= -50:
                action = 'SELL'
            else:
                action = 'HOLD'
            
            return {
                'action': action,
                'confidence': abs(confidence),
                'reasons': reasons,
                'indicators': indicators,
                'sentiment': sentiment_score
            }
            
        except Exception as e:
            self.logger.error(f"Signal generation error: {e}")
            return {'action': 'HOLD', 'confidence': 0, 'reason': f'Error: {e}'}
    
    def execute_trade(self, ticker: str, signal: Dict):
        """Execute a trade"""
        try:
            if self.current_position:
                self.logger.warning("Already have a position, skipping trade")
                return
            
            # Calculate position size
            position_size = self.calculate_position_size(ticker)
            
            # Create position record
            self.current_position = {
                'ticker': ticker,
                'entry_time': datetime.now(),
                'entry_price': signal['indicators']['current_price'],
                'position_size': position_size,
                'signal': signal,
                'stop_loss': signal['indicators']['current_price'] * (1 - self.stop_loss),
                'profit_target': signal['indicators']['current_price'] * (1 + self.profit_target)
            }
            
            # Log the trade
            self.logger.info(f"Opening position: {ticker} at ${self.current_position['entry_price']:.2f}")
            
            # Here you would call Schwab API to place the actual order
            # For now, we'll simulate the trade
            self.simulate_order_placement(ticker, position_size, 'BUY')
            
        except Exception as e:
            self.logger.error(f"Trade execution error: {e}")
    
    def manage_current_position(self):
        """Manage the current open position"""
        try:
            if not self.current_position:
                return
            
            ticker = self.current_position['ticker']
            current_data = self.market_data.get_stock_data(ticker, "1d")
            
            if current_data is None or current_data.empty:
                return
            
            current_price = current_data['Close'].iloc[-1]
            entry_price = self.current_position['entry_price']
            entry_time = self.current_position['entry_time']
            
            # Calculate P&L
            pnl_pct = (current_price - entry_price) / entry_price
            pnl_dollar = pnl_pct * self.current_position['position_size']
            
            # Check exit conditions
            should_exit = False
            exit_reason = ""
            
            # Profit target
            if pnl_pct >= self.profit_target:
                should_exit = True
                exit_reason = "Profit target reached"
            
            # Stop loss
            elif pnl_pct <= -self.stop_loss:
                should_exit = True
                exit_reason = "Stop loss triggered"
            
            # Time-based exit
            elif (datetime.now() - entry_time).minutes >= self.max_trade_duration:
                should_exit = True
                exit_reason = "Time limit reached"
            
            # Signal reversal
            elif self.check_signal_reversal(ticker):
                should_exit = True
                exit_reason = "Signal reversal"
            
            if should_exit:
                self.close_position(exit_reason, current_price, pnl_dollar)
            
        except Exception as e:
            self.logger.error(f"Position management error: {e}")
    
    def check_signal_reversal(self, ticker: str) -> bool:
        """Check if the signal has reversed"""
        try:
            signal = self.analyze_ticker(ticker)
            original_action = self.current_position['signal']['action']
            
            # If original was BUY and now is SELL, or vice versa
            return signal['action'] != original_action and signal['confidence'] > 30
            
        except Exception as e:
            self.logger.error(f"Signal reversal check error: {e}")
            return False
    
    def close_position(self, reason: str, exit_price: float, pnl: float):
        """Close the current position"""
        try:
            ticker = self.current_position['ticker']
            
            # Log the exit
            self.logger.info(f"Closing position: {ticker} at ${exit_price:.2f} - {reason}")
            self.logger.info(f"P&L: ${pnl:.2f}")
            
            # Update performance metrics
            self.total_trades += 1
            self.daily_pnl += pnl
            self.total_pnl += pnl
            
            if pnl > 0:
                self.winning_trades += 1
            
            # Record the trade
            trade_record = {
                'ticker': ticker,
                'entry_time': self.current_position['entry_time'],
                'exit_time': datetime.now(),
                'entry_price': self.current_position['entry_price'],
                'exit_price': exit_price,
                'pnl': pnl,
                'reason': reason
            }
            self.trades_today.append(trade_record)
            
            # Here you would call Schwab API to close the actual position
            self.simulate_order_placement(ticker, self.current_position['position_size'], 'SELL')
            
            # Clear current position
            self.current_position = None
            
        except Exception as e:
            self.logger.error(f"Position close error: {e}")
    
    def calculate_position_size(self, ticker: str) -> float:
        """Calculate position size based on risk management"""
        try:
            # Simple position sizing - can be enhanced
            account_balance = 10000  # Would get from Schwab API
            risk_per_trade = min(self.max_trade_amount, account_balance * 0.05)
            
            return risk_per_trade
            
        except Exception as e:
            self.logger.error(f"Position size calculation error: {e}")
            return self.max_trade_amount
    
    def simulate_order_placement(self, ticker: str, size: float, side: str):
        """Simulate order placement (replace with actual Schwab API calls)"""
        self.logger.info(f"SIMULATION: {side} {size} shares of {ticker}")
        # TODO: Implement actual Schwab API order placement
    
    def get_performance_summary(self) -> Dict:
        """Get performance summary"""
        win_rate = (self.winning_trades / self.total_trades * 100) if self.total_trades > 0 else 0
        
        return {
            'total_trades': self.total_trades,
            'winning_trades': self.winning_trades,
            'win_rate': win_rate,
            'total_pnl': self.total_pnl,
            'daily_pnl': self.daily_pnl,
            'current_position': self.current_position,
            'is_running': self.is_running
        }

def main():
    """Main function to run the bot"""
    print("🚀 Starting Options Scalping Bot...")
    
    bot = OptionsScalpingBot()
    
    try:
        bot.start()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot error: {e}")
    finally:
        # Print performance summary
        summary = bot.get_performance_summary()
        print("\n📊 Performance Summary:")
        print(f"Total Trades: {summary['total_trades']}")
        print(f"Win Rate: {summary['win_rate']:.1f}%")
        print(f"Total P&L: ${summary['total_pnl']:.2f}")
        print(f"Daily P&L: ${summary['daily_pnl']:.2f}")

if __name__ == "__main__":
    main() 