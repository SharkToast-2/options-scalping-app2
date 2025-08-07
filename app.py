#!/usr/bin/env python3
"""
Options Scalping Bot - Main Application (Simple Version)
"""

import streamlit as st
from modules.data_fetcher import get_minute_data
from modules.indicators import calc_indicators
from modules.signal_engine import check_signals
from modules.trade_executor import execute_trade, check_total_loss, get_open_trades, trade_active
from modules.risk_manager import check_exit_conditions
from modules.logger import log_trade
import datetime
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("config/.env")

# Page configuration
st.set_page_config(page_title="Options Scalping Bot", layout="wide")
st.title("📈 Options Scalping Bot")

# Sidebar configuration
st.sidebar.header("⚙️ Bot Configuration")
TICKER = st.sidebar.text_input("Stock Ticker", value="META")
TRADE_SIZE = st.sidebar.slider("Max Price Per Trade ($)", min_value=100, max_value=1000, value=500, step=50)
DAILY_LIMIT = st.sidebar.slider("Max Daily Loss ($)", min_value=100, max_value=1000, value=500, step=50)
PROFIT_TARGET = st.sidebar.slider("Profit % Target", min_value=1, max_value=10, value=3, step=1)
STOP_LOSS = st.sidebar.slider("Stop Loss %", min_value=1, max_value=10, value=3, step=1)

st.sidebar.success("✅ Config loaded")

# Main bot control
running = st.sidebar.toggle("Run Bot")

if running:
    st.info("Bot is actively monitoring trades...")

    # Simulated trading loop (in production, this would be more sophisticated)
    try:
        # Get market data
        data = get_minute_data(TICKER)
        if data.empty:
            st.warning("⚠️ No market data available")
        else:
            # Calculate indicators
            indicators = calc_indicators(data)
            if not indicators:
                st.warning("⚠️ Unable to calculate indicators")
            else:
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
                    
                    # Execute trade
                    if not trade_active():
                        contract = f"{TICKER}_OPTION_CALL"
                        
                        if execute_trade(contract, TRADE_SIZE):
                            log_trade(TICKER, contract, "BUY", data.iloc[-1]['Close'], TRADE_SIZE)
                            st.success(f"✅ Trade executed: {contract}")
                        else:
                            st.error("❌ Trade execution failed")
                else:
                    st.info("⏳ Waiting for optimal signals...")
                
                # Check exit conditions for open trades
                open_trades = get_open_trades()
                if open_trades:
                    check_exit_conditions(open_trades, PROFIT_TARGET, STOP_LOSS)
                    
    except Exception as e:
        st.error(f"❌ Error in trading loop: {e}")

else:
    st.info("Bot is idle. Toggle switch in sidebar to start.")

# Display current status
st.header("📊 Current Status")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Daily P&L", f"${check_total_loss():.2f}")
    
with col2:
    st.metric("Active Trades", len(get_open_trades()))
    
with col3:
    st.metric("Bot Status", "🟢 Running" if running else "🔴 Stopped")

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

# Market hours check
now = datetime.datetime.now()
if now.hour >= 14:
    st.warning("⚠️ Trading window closed (after 2 PM).")
elif now.hour < 9:
    st.info("ℹ️ Market opens at 9 AM.") 