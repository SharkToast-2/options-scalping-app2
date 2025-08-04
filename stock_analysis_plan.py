#!/usr/bin/env python3
"""
Stock Analysis Plan - Comprehensive Analysis Script
This script demonstrates the key functionality of the stock analysis environment.
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
import time
warnings.filterwarnings('ignore')

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def create_mock_data(symbol, days=252):
    """Create mock stock data for demonstration"""
    np.random.seed(42)  # For reproducible results
    
    # Generate realistic stock data
    start_price = 150.0
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    # Generate price movements
    returns = np.random.normal(0.0005, 0.02, days)  # Daily returns
    prices = [start_price]
    
    for i in range(1, days):
        new_price = prices[-1] * (1 + returns[i])
        prices.append(new_price)
    
    # Create DataFrame
    data = pd.DataFrame({
        'Open': [p * (1 + np.random.normal(0, 0.005)) for p in prices],
        'High': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
        'Low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
        'Close': prices,
        'Volume': np.random.randint(1000000, 10000000, days)
    }, index=dates)
    
    return data

def get_stock_data(symbol, period="1y"):
    """Fetch stock data from Yahoo Finance with fallback to mock data"""
    print(f"Fetching data for {symbol}...")
    
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period=period)
        
        if data.empty:
            print(f"⚠️  No data found for {symbol}, using mock data")
            return None, create_mock_data(symbol)
        
        return stock, data
        
    except Exception as e:
        print(f"⚠️  Error fetching data for {symbol}: {e}")
        print("📊 Using mock data for demonstration...")
        return None, create_mock_data(symbol)

def analyze_stock(symbol="AAPL"):
    """Perform comprehensive stock analysis"""
    print_header(f"STOCK ANALYSIS PLAN - {symbol}")
    
    # 1. Fetch Data
    stock, data = get_stock_data(symbol)
    
    print(f"✅ Successfully loaded {len(data)} days of data")
    
    # 2. Basic Statistics
    print_header("BASIC STATISTICS")
    latest_price = data['Close'].iloc[-1]
    price_change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
    price_change_pct = (price_change / data['Close'].iloc[-2]) * 100
    
    print(f"Current Price: ${latest_price:.2f}")
    print(f"Daily Change: ${price_change:.2f} ({price_change_pct:+.2f}%)")
    print(f"52-Week High: ${data['High'].max():.2f}")
    print(f"52-Week Low: ${data['Low'].min():.2f}")
    print(f"Average Volume: {data['Volume'].mean():,.0f}")
    
    # 3. Technical Indicators
    print_header("TECHNICAL INDICATORS")
    
    # Moving Averages
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['MA200'] = data['Close'].rolling(window=200).mean()
    
    current_ma20 = data['MA20'].iloc[-1]
    current_ma50 = data['MA50'].iloc[-1]
    current_ma200 = data['MA200'].iloc[-1]
    
    print(f"20-Day MA: ${current_ma20:.2f}")
    print(f"50-Day MA: ${current_ma50:.2f}")
    print(f"200-Day MA: ${current_ma200:.2f}")
    
    # RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    current_rsi = data['RSI'].iloc[-1]
    print(f"RSI (14): {current_rsi:.2f}")
    
    # 4. Volatility Analysis
    print_header("VOLATILITY ANALYSIS")
    daily_returns = data['Close'].pct_change()
    volatility = daily_returns.std() * np.sqrt(252) * 100  # Annualized
    print(f"Annualized Volatility: {volatility:.2f}%")
    
    # 5. Performance Metrics
    print_header("PERFORMANCE METRICS")
    total_return = ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100
    print(f"Total Return (1Y): {total_return:.2f}%")
    
    # Sharpe Ratio (assuming risk-free rate of 2%)
    excess_returns = daily_returns - 0.02/252
    sharpe_ratio = excess_returns.mean() / daily_returns.std() * np.sqrt(252)
    print(f"Sharpe Ratio: {sharpe_ratio:.3f}")
    
    # 6. Company Information
    print_header("COMPANY INFORMATION")
    if stock:
        try:
            info = stock.info
            print(f"Company: {info.get('longName', 'N/A')}")
            print(f"Sector: {info.get('sector', 'N/A')}")
            print(f"Industry: {info.get('industry', 'N/A')}")
            print(f"Market Cap: ${info.get('marketCap', 0):,.0f}")
            print(f"P/E Ratio: {info.get('trailingPE', 'N/A')}")
            print(f"Dividend Yield: {info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else "Dividend Yield: N/A")
        except Exception as e:
            print(f"Could not fetch company info: {e}")
    else:
        print("📊 Using mock data - company info not available")
        print("Company: Apple Inc. (Mock Data)")
        print("Sector: Technology")
        print("Industry: Consumer Electronics")
        print("Market Cap: $2,500,000,000,000")
        print("P/E Ratio: 25.5")
        print("Dividend Yield: 0.50%")
    
    # 7. Recent News
    print_header("RECENT NEWS")
    if stock:
        try:
            news = stock.news[:3]  # Get last 3 news items
            for i, item in enumerate(news, 1):
                print(f"{i}. {item['title']}")
                print(f"   Published: {datetime.fromtimestamp(item['providerPublishTime']).strftime('%Y-%m-%d %H:%M')}")
                print()
        except Exception as e:
            print(f"Could not fetch news: {e}")
    else:
        print("📊 Mock News Headlines:")
        print("1. Apple Reports Strong Q3 Earnings")
        print("   Published: 2025-07-30 14:30")
        print()
        print("2. New iPhone Model Expected in September")
        print("   Published: 2025-07-29 09:15")
        print()
        print("3. Apple Expands AI Capabilities")
        print("   Published: 2025-07-28 16:45")
        print()
    
    print_header("ANALYSIS COMPLETE")
    print("✅ Stock analysis plan executed successfully!")
    
    return data

def run_portfolio_analysis():
    """Run analysis on multiple stocks"""
    print_header("PORTFOLIO ANALYSIS")
    
    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
    portfolio_data = {}
    
    for symbol in symbols:
        try:
            stock, data = get_stock_data(symbol, "6mo")
            if not data.empty:
                portfolio_data[symbol] = data
                print(f"✅ {symbol}: ${data['Close'].iloc[-1]:.2f}")
            time.sleep(1)  # Rate limiting
        except Exception as e:
            print(f"❌ {symbol}: Error - {e}")
    
    if portfolio_data:
        print(f"\n📊 Portfolio Analysis Complete - {len(portfolio_data)} stocks analyzed")
    
    return portfolio_data

def create_streamlit_app():
    """Create a Streamlit app for interactive analysis"""
    streamlit_code = '''
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
'''
    
    with open("streamlit_dashboard.py", "w") as f:
        f.write(streamlit_code)
    
    print("📱 Streamlit dashboard created: streamlit_dashboard.py")
    print("   Run with: streamlit run streamlit_dashboard.py")

def main():
    """Main execution function"""
    print("🚀 Starting Stock Analysis Plan...")
    print(f"📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run individual stock analysis
    analyze_stock("AAPL")
    
    # Run portfolio analysis
    run_portfolio_analysis()
    
    # Create Streamlit app
    create_streamlit_app()
    
    print("\n🎉 Stock Analysis Plan completed successfully!")
    print("💡 Next steps:")
    print("   - Run 'streamlit run streamlit_dashboard.py' for interactive dashboard")
    print("   - Modify symbols in the script for different stocks")
    print("   - Add more technical indicators as needed")
    print("   - Consider using real-time data feeds for live analysis")

if __name__ == "__main__":
    main() 