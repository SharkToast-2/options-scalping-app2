#!/usr/bin/env python3
"""
Options Scalping Bot - Main Application (Secure Version)
"""

import streamlit as st
from modules.data_fetcher import get_minute_data
from modules.indicators import calc_indicators
from modules.signal_engine import check_signals
from modules.trade_executor import execute_trade, check_total_loss, get_open_trades, trade_active
from modules.risk_manager import check_exit_conditions
from modules.logger import log_trade
from modules.secure_auth import SecureAuth
from config.security_config import get_security_manager
import datetime
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("config/.env")

# Initialize security manager
security_manager = get_security_manager()

# Page configuration
st.set_page_config(
    page_title="Options Scalping Bot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize secure authentication
secure_auth = SecureAuth()

# Main app
def main():
    st.title("📈 Options Scalping Bot (Secure)")
    
    # Check authentication first
    if not secure_auth.show_secure_interface():
        return
    
    # Show security status
    st.sidebar.header("🔒 Security Status")
    st.sidebar.success("✅ Secure Session Active")
    
    # Sidebar configuration with validation
    st.sidebar.header("⚙️ Bot Configuration")
    
    # Input validation for ticker
    ticker_input = st.sidebar.text_input("Stock Ticker", value="META", max_chars=5).upper()
    if not security_manager.validate_ticker(ticker_input):
        st.sidebar.error("❌ Invalid ticker format")
        return
    
    # Input validation for trade parameters
    trade_size = st.sidebar.slider("Max Price Per Trade ($)", min_value=100, max_value=1000, value=500, step=50)
    if not security_manager.validate_trade_size(trade_size):
        st.sidebar.error("❌ Invalid trade size")
        return
    
    daily_limit = st.sidebar.slider("Max Daily Loss ($)", min_value=100, max_value=1000, value=500, step=50)
    profit_target = st.sidebar.slider("Profit % Target", min_value=1, max_value=10, value=3, step=1)
    stop_loss = st.sidebar.slider("Stop Loss %", min_value=1, max_value=10, value=3, step=1)
    
    st.sidebar.success("✅ Config validated")
    
    # Main bot control
    running = st.sidebar.toggle("Run Bot")
    
    if running:
        # Security check before running
        if not security_manager.check_rate_limit("user", "trade"):
            st.error("⚠️ Rate limit exceeded. Please wait.")
            return
        
        st.info("Bot is actively monitoring trades...")
        
        # Simulated trading loop (in production, this would be more sophisticated)
        try:
            # Get market data
            data = get_minute_data(ticker_input)
            if data.empty:
                st.warning("⚠️ No market data available")
                return
            
            # Calculate indicators
            indicators = calc_indicators(data)
            if not indicators:
                st.warning("⚠️ Unable to calculate indicators")
                return
            
            # Check signals
            signals = check_signals(indicators)
            
            # Display signal status
            st.subheader("📊 Signal Analysis")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("RSI Signal", "✅" if signals.get('rsi_signal') else "❌")
            with col2:
                st.metric("MACD Signal", "✅" if signals.get('macd_signal') else "❌")
            with col3:
                st.metric("Volume Signal", "✅" if signals.get('volume_signal') else "❌")
            with col4:
                st.metric("Momentum Signal", "✅" if signals.get('momentum_signal') else "❌")
            
            # Check if all signals are positive
            if all(signals.values()):
                st.success("🎯 All signals positive - Trade opportunity detected!")
                
                # Execute trade with security validation
                if not trade_active():
                    contract = f"{ticker_input}_OPTION_CALL"
                    
                    # Log the trade attempt
                    security_manager.log_security_event("trade_attempt", f"Attempting trade: {contract}", "user")
                    
                    if execute_trade(contract, trade_size):
                        log_trade(ticker_input, contract, "BUY", data.iloc[-1]['Close'], trade_size)
                        st.success(f"✅ Trade executed: {contract}")
                    else:
                        st.error("❌ Trade execution failed")
            else:
                st.info("⏳ Waiting for optimal signals...")
            
            # Check exit conditions for open trades
            open_trades = get_open_trades()
            if open_trades:
                check_exit_conditions(open_trades, profit_target, stop_loss)
                
        except Exception as e:
            st.error(f"❌ Error in trading loop: {e}")
            security_manager.log_security_event("trading_error", str(e), "user")
    
    else:
        st.info("Bot is idle. Toggle switch in sidebar to start.")
    
    # Display current status
    st.header("📊 Current Status")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Daily P&L", f"${check_total_loss():.2f}")
        
    with col2:
        st.metric("Active Trades", len(get_open_trades()))
        
    with col3:
        st.metric("Bot Status", "🟢 Running" if running else "🔴 Stopped")
    
    with col4:
        risk_summary = security_manager.get_risk_summary()
        st.metric("Risk Level", f"{risk_summary['exposure_ratio']:.1%}")
    
    # Display recent trades
    st.header("📋 Recent Trades")
    open_trades = get_open_trades()
    
    if open_trades:
        for trade in open_trades:
            with st.expander(f"Trade {trade['id']}: {trade['symbol']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Entry Price:** ${trade['entry_price']:.2f}")
                with col2:
                    st.write(f"**Current Price:** ${trade['current_price']:.2f}")
                with col3:
                    change_pct = ((trade['current_price'] - trade['entry_price']) / trade['entry_price']) * 100
                    st.write(f"**Change:** {change_pct:.2f}%")
    else:
        st.info("No active trades")
    
    # Security footer
    st.markdown("---")
    st.caption("🔒 This application uses secure authentication and encryption. All trades are logged for audit purposes.")

if __name__ == "__main__":
    main() 