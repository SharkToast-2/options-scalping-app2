
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide")

st.title("📈 Stock Analysis Dashboard")
st.write("Interactive stock analysis using Streamlit")

# Sidebar
st.sidebar.header("Settings")
symbol = st.sidebar.text_input("Stock Symbol", "AAPL").upper()
period = st.sidebar.selectbox("Time Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"])

if st.sidebar.button("Analyze"):
    try:
        # Fetch data
        stock = yf.Ticker(symbol)
        data = stock.history(period=period)
        
        if not data.empty:
            # Display basic info
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Current Price", f"${data['Close'].iloc[-1]:.2f}")
            
            with col2:
                change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
                st.metric("Daily Change", f"${change:.2f}")
            
            with col3:
                st.metric("52-Week High", f"${data['High'].max():.2f}")
            
            with col4:
                st.metric("52-Week Low", f"${data['Low'].min():.2f}")
            
            # Price chart
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='OHLC'
            ))
            fig.update_layout(title=f"{symbol} Stock Price", xaxis_title="Date", yaxis_title="Price")
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.error("No data found for this symbol")
            
    except Exception as e:
        st.error(f"Error: {e}")

st.sidebar.markdown("---")
st.sidebar.markdown("**Instructions:**")
st.sidebar.markdown("1. Enter a stock symbol")
st.sidebar.markdown("2. Select time period")
st.sidebar.markdown("3. Click 'Analyze'")
