#!/usr/bin/env python3
"""
Simple Options Scalping Dashboard
A clean, streamlined version for options trading analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import requests

class SimpleOptionsScalper:
    def __init__(self):
        self.symbols = ['SPY', 'QQQ', 'IWM', 'AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA', 'META', 'NFLX']
        self.setup_page()
    
    def setup_page(self):
        """Setup Streamlit page configuration"""
        st.set_page_config(
            page_title="Simple Options Scalper",
            page_icon="📈",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.title("📈 Simple Options Scalper")
        st.markdown("---")
    
    def load_schwab_config(self):
        """Load Schwab configuration from backup"""
        try:
            with open('schwab_backup.json', 'r') as f:
                config = json.load(f)
                self.schwab_creds = config['schwab_credentials']
                self.schwab_urls = config['schwab_urls']
        except Exception as e:
            st.error(f"Error loading Schwab config: {e}")
            self.schwab_creds = {}
            self.schwab_urls = {}
    
    def get_stock_data(self, symbol, period="1mo"):
        """Get stock data using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            return data
        except Exception as e:
            st.error(f"Error fetching data for {symbol}: {e}")
            return None
    
    def calculate_indicators(self, data):
        """Calculate basic technical indicators"""
        if data is None or data.empty:
            return {}
        
        # RSI
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # Moving averages
        sma_20 = data['Close'].rolling(window=20).mean()
        sma_50 = data['Close'].rolling(window=50).mean()
        
        # Bollinger Bands
        bb_middle = data['Close'].rolling(window=20).mean()
        bb_std = data['Close'].rolling(window=20).std()
        bb_upper = bb_middle + (bb_std * 2)
        bb_lower = bb_middle - (bb_std * 2)
        
        # Volume SMA
        volume_sma = data['Volume'].rolling(window=20).mean()
        
        return {
            'rsi': rsi.iloc[-1] if not rsi.empty else 50,
            'sma_20': sma_20.iloc[-1] if not sma_20.empty else 0,
            'sma_50': sma_50.iloc[-1] if not sma_50.empty else 0,
            'bb_upper': bb_upper.iloc[-1] if not bb_upper.empty else 0,
            'bb_lower': bb_lower.iloc[-1] if not bb_lower.empty else 0,
            'volume_sma': volume_sma.iloc[-1] if not volume_sma.empty else 0,
            'current_price': data['Close'].iloc[-1],
            'price_change': data['Close'].iloc[-1] - data['Close'].iloc[-2] if len(data) > 1 else 0,
            'price_change_pct': ((data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2] * 100) if len(data) > 1 else 0
        }
    
    def get_signal(self, indicators):
        """Generate trading signal based on indicators"""
        rsi = indicators.get('rsi', 50)
        current_price = indicators.get('current_price', 0)
        sma_20 = indicators.get('sma_20', 0)
        bb_upper = indicators.get('bb_upper', 0)
        bb_lower = indicators.get('bb_lower', 0)
        
        signal = "HOLD"
        confidence = 0
        
        # RSI signals
        if rsi < 30:
            signal = "BUY"
            confidence += 30
        elif rsi > 70:
            signal = "SELL"
            confidence += 30
        
        # Moving average signals
        if current_price > sma_20:
            confidence += 20
        else:
            confidence -= 20
        
        # Bollinger Band signals
        if current_price < bb_lower:
            signal = "BUY"
            confidence += 25
        elif current_price > bb_upper:
            signal = "SELL"
            confidence += 25
        
        return signal, confidence
    
    def create_chart(self, symbol, data):
        """Create interactive chart with indicators"""
        if data is None or data.empty:
            return None
        
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=(f'{symbol} Price', 'Volume', 'RSI'),
            row_heights=[0.6, 0.2, 0.2]
        )
        
        # Price candlestick
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Price'
            ),
            row=1, col=1
        )
        
        # Moving averages
        sma_20 = data['Close'].rolling(window=20).mean()
        sma_50 = data['Close'].rolling(window=50).mean()
        
        fig.add_trace(
            go.Scatter(x=data.index, y=sma_20, name='SMA 20', line=dict(color='orange')),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=data.index, y=sma_50, name='SMA 50', line=dict(color='blue')),
            row=1, col=1
        )
        
        # Volume
        fig.add_trace(
            go.Bar(x=data.index, y=data['Volume'], name='Volume'),
            row=2, col=1
        )
        
        # RSI
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        fig.add_trace(
            go.Scatter(x=data.index, y=rsi, name='RSI', line=dict(color='purple')),
            row=3, col=1
        )
        
        # RSI overbought/oversold lines
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
        
        fig.update_layout(
            title=f'{symbol} Analysis',
            xaxis_rangeslider_visible=False,
            height=600
        )
        
        return fig
    
    def run(self):
        """Main app runner"""
        # Sidebar
        with st.sidebar:
            st.header("⚙️ Settings")
            
            # Symbol selection
            selected_symbols = st.multiselect(
                "Select symbols:",
                self.symbols,
                default=['SPY', 'QQQ', 'AAPL']
            )
            
            # Time period
            period = st.selectbox(
                "Time period:",
                ["1d", "5d", "1mo", "3mo", "6mo", "1y"],
                index=2
            )
            
            # Refresh button
            if st.button("🔄 Refresh Data", type="primary"):
                st.rerun()
        
        # Main content
        if not selected_symbols:
            st.warning("Please select at least one symbol")
            return
        
        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Data", "📈 Analysis", "🎯 Signals", "🔐 Schwab Auth"])
        
        with tab1:
            self.show_market_data(selected_symbols, period)
        
        with tab2:
            self.show_analysis(selected_symbols, period)
        
        with tab3:
            self.show_signals(selected_symbols, period)
        
        with tab4:
            self.show_schwab_auth()
    
    def show_market_data(self, symbols, period):
        """Show market data overview"""
        st.subheader("📊 Market Data")
        
        # Create columns for symbols
        cols = st.columns(min(len(symbols), 3))
        
        for i, symbol in enumerate(symbols):
            col_idx = i % 3
            with cols[col_idx]:
                data = self.get_stock_data(symbol, period)
                if data is not None and not data.empty:
                    indicators = self.calculate_indicators(data)
                    
                    # Display metrics
                    st.metric(
                        label=symbol,
                        value=f"${indicators['current_price']:.2f}",
                        delta=f"{indicators['price_change_pct']:.2f}%"
                    )
                    
                    # Additional info
                    st.caption(f"RSI: {indicators['rsi']:.1f}")
                    st.caption(f"Volume: {data['Volume'].iloc[-1]:,.0f}")
    
    def show_analysis(self, symbols, period):
        """Show detailed analysis charts"""
        st.subheader("📈 Technical Analysis")
        
        for symbol in symbols:
            with st.expander(f"📊 {symbol} Analysis"):
                data = self.get_stock_data(symbol, period)
                if data is not None and not data.empty:
                    chart = self.create_chart(symbol, data)
                    if chart:
                        st.plotly_chart(chart, use_container_width=True)
                else:
                    st.error(f"No data available for {symbol}")
    
    def show_signals(self, symbols, period):
        """Show trading signals"""
        st.subheader("🎯 Trading Signals")
        
        signals_data = []
        
        for symbol in symbols:
            data = self.get_stock_data(symbol, period)
            if data is not None and not data.empty:
                indicators = self.calculate_indicators(data)
                signal, confidence = self.get_signal(indicators)
                
                signals_data.append({
                    'Symbol': symbol,
                    'Price': f"${indicators['current_price']:.2f}",
                    'Change': f"{indicators['price_change_pct']:.2f}%",
                    'RSI': f"{indicators['rsi']:.1f}",
                    'Signal': signal,
                    'Confidence': f"{confidence}%"
                })
        
        if signals_data:
            df = pd.DataFrame(signals_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No signal data available")
    
    def show_schwab_auth(self):
        """Show Schwab authentication interface"""
        try:
            from modules.schwab_auth import SchwabAuth
            schwab_auth = SchwabAuth()
            schwab_auth.show_auth_interface()
        except Exception as e:
            st.error(f"Error loading Schwab authentication: {e}")
            st.info("Please ensure the Schwab authentication module is properly configured.")

def main():
    """Main function"""
    try:
        app = SimpleOptionsScalper()
        app.run()
    except Exception as e:
        st.error(f"Application error: {e}")
        st.info("Please refresh the page or check your internet connection.")

if __name__ == "__main__":
    main() 