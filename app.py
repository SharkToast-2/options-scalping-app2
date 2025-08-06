#!/usr/bin/env python3
"""
Options Scalping Bot - Main Application
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

    while True:
        now = datetime.datetime.now()
        if now.hour >= 14:
            st.warning("Trading window closed.")
            break

        if check_total_loss() >= DAILY_LIMIT:
            st.error("Daily loss limit reached. Halting trading.")
            break

        if not trade_active():
            data = get_minute_data(TICKER)
            indicators = calc_indicators(data)
            signals = check_signals(indicators)

            if all(signals.values()):
                contract = f"{TICKER}_OPTION_CALL"
                execute_trade(contract, TRADE_SIZE)
                log_trade(TICKER, contract, "BUY", data.iloc[-1]['Close'])

        open_trades = get_open_trades()
        if open_trades:
            check_exit_conditions(open_trades, PROFIT_TARGET, STOP_LOSS)

        time.sleep(60)

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
# TODO: Add trade history display 