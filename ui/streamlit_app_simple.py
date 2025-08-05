#!/usr/bin/env python3
"""
Simplified Options Scalping Dashboard
Focuses on core functionality without complex platform detection issues
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
from typing import Dict, List, Optional
import concurrent.futures
import requests
import json

# Import our modules
from data.data_fetcher import OptimizedDataFetcher
from signals.technical_indicators import TechnicalIndicators
from modules.simple_schwab_auth import SimpleSchwabAuth

class SimpleOptionsScalpingDashboard:
    def __init__(self):
        # Initialize core components
        self.data_fetcher = OptimizedDataFetcher()
        self.indicators = TechnicalIndicators()
        self.schwab_auth = SimpleSchwabAuth()
        
        # Initialize session state
        self._init_session_state()
        
        # Target symbols for analysis
        self.target_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX', 'AMD', 'INTC']
    
    def _init_session_state(self):
        """Initialize Streamlit session state"""
        if 'selected_symbols' not in st.session_state:
            st.session_state.selected_symbols = self.target_symbols[:5]
        
        if 'auto_refresh' not in st.session_state:
            st.session_state.auto_refresh = False
        
        if 'refresh_interval' not in st.session_state:
            st.session_state.refresh_interval = 30
    
    def run(self):
        """Main app runner"""
        st.set_page_config(
            page_title="Simple Options Scalping Dashboard",
            page_icon="📈",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.title("📈 Simple Options Scalping Dashboard")
        st.markdown("---")
        
        # Setup sidebar
        self.setup_sidebar()
        
        # Main content
        self.show_main_content()
    
    def setup_sidebar(self):
        """Setup sidebar with basic controls"""
        with st.sidebar:
            st.header("⚙️ Controls")
            
            # Symbol selection
            st.subheader("📊 Stock Selection")
            selected_symbols = st.multiselect(
                "Select stocks to analyze:",
                self.target_symbols,
                default=st.session_state.selected_symbols,
                max_selections=10
            )
            st.session_state.selected_symbols = selected_symbols
            
            # Auto-refresh settings
            st.subheader("🔄 Auto-Refresh")
            auto_refresh = st.checkbox("Enable auto-refresh", value=st.session_state.auto_refresh)
            st.session_state.auto_refresh = auto_refresh
            
            if auto_refresh:
                interval = st.slider("Refresh interval (seconds)", 10, 120, st.session_state.refresh_interval)
                st.session_state.refresh_interval = interval
                
                # Auto-refresh logic
                if st.session_state.auto_refresh:
                    time.sleep(st.session_state.refresh_interval)
                    st.rerun()
            
            # Manual refresh button
            if st.button("🔄 Refresh Data", type="primary"):
                st.rerun()
            
            st.markdown("---")
            
            # Data source info
            st.subheader("📡 Data Sources")
            st.info("• Polygon.io (Primary)")
            st.info("• Yahoo Finance (Fallback)")
            st.info("• Mock Data (Emergency)")
    
    def show_main_content(self):
        """Show main dashboard content"""
        if not st.session_state.selected_symbols:
            st.warning("⚠️ Please select at least one stock to analyze")
            return
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Real-Time Data", "📈 Stock Rankings", "🎯 Scalping Signals", "🔐 Schwab Auth"])
        
        with tab1:
            self.show_real_time_data()
        
        with tab2:
            self.show_stock_rankings()
        
        with tab3:
            self.show_scalping_signals()
        
        with tab4:
            self.show_schwab_auth()
    
    def show_real_time_data(self):
        """Show real-time stock data"""
        st.subheader("📊 Real-Time Market Data")
        
        # Get market data
        symbols = st.session_state.selected_symbols
        market_data = self.get_market_data(symbols)
        
        if not market_data:
            st.warning("⚠️ No market data available")
            return
        
        # Display data in columns
        cols = st.columns(min(len(symbols), 3))
        
        for i, symbol in enumerate(symbols):
            col_idx = i % 3
            with cols[col_idx]:
                self.display_stock_card(symbol, market_data.get(symbol, {}))
    
    def show_stock_rankings(self):
        """Show stock rankings based on technical indicators"""
        st.subheader("📈 Stock Rankings")
        
        # Get rankings
        rankings = self.calculate_rankings()
        
        if not rankings:
            st.warning("⚠️ No ranking data available")
            return
        
        # Display rankings table
        df = pd.DataFrame(rankings)
        st.dataframe(df, use_container_width=True)
    
    def show_scalping_signals(self):
        """Show scalping opportunities"""
        st.subheader("🎯 Scalping Opportunities")
        
        # Get scalping signals
        signals = self.get_scalping_signals()
        
        if not signals:
            st.info("📊 No strong scalping signals at the moment")
            return
        
        # Display signals
        for signal in signals:
            with st.expander(f"🎯 {signal['symbol']} - {signal['signal']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Score", f"{signal['score']:.1f}")
                
                with col2:
                    st.metric("Price", f"${signal['price']:.2f}")
                
                with col3:
                    st.metric("Signal", signal['signal'])
    
    def get_market_data(self, symbols: List[str]) -> Dict:
        """Get market data for symbols"""
        try:
            data = {}
            for symbol in symbols:
                quote = self.data_fetcher.get_real_time_quote(symbol)
                if quote:
                    data[symbol] = quote
            return data
        except Exception as e:
            st.error(f"Error fetching market data: {e}")
            return {}
    
    def calculate_rankings(self) -> List[Dict]:
        """Calculate stock rankings"""
        try:
            rankings = []
            symbols = st.session_state.selected_symbols
            
            for symbol in symbols:
                # Get stock data
                stock_data = self.data_fetcher.get_stock_data(symbol)
                if stock_data is None or stock_data.empty:
                    continue
                
                # Calculate indicators
                indicators = self.indicators.calculate_all_indicators(stock_data)
                
                # Calculate score
                score = self.calculate_score(indicators)
                
                # Get current price
                quote = self.data_fetcher.get_real_time_quote(symbol)
                price = quote.get('price', 0) if quote else 0
                
                rankings.append({
                    'Symbol': symbol,
                    'Price': f"${price:.2f}",
                    'Score': f"{score:.1f}",
                    'RSI': f"{indicators.get('rsi', 0):.1f}",
                    'MACD': f"{indicators.get('macd', 0):.3f}",
                    'Signal': self.get_signal(score)
                })
            
            # Sort by score
            rankings.sort(key=lambda x: float(x['Score']), reverse=True)
            return rankings
            
        except Exception as e:
            st.error(f"Error calculating rankings: {e}")
            return []
    
    def get_scalping_signals(self) -> List[Dict]:
        """Get scalping signals"""
        try:
            signals = []
            symbols = st.session_state.selected_symbols
            
            for symbol in symbols:
                # Get stock data
                stock_data = self.data_fetcher.get_stock_data(symbol)
                if stock_data is None or stock_data.empty:
                    continue
                
                # Calculate indicators
                indicators = self.indicators.calculate_all_indicators(stock_data)
                
                # Check for scalping opportunities
                signal = self.check_scalping_opportunity(indicators)
                
                if signal['opportunity']:
                    quote = self.data_fetcher.get_real_time_quote(symbol)
                    price = quote.get('price', 0) if quote else 0
                    
                    signals.append({
                        'symbol': symbol,
                        'signal': signal['signal'],
                        'score': signal['score'],
                        'price': price,
                        'reason': signal['reason']
                    })
            
            return signals
            
        except Exception as e:
            st.error(f"Error getting scalping signals: {e}")
            return []
    
    def display_stock_card(self, symbol: str, data: Dict):
        """Display a stock card"""
        with st.container():
            st.subheader(symbol)
            
            if not data:
                st.warning("No data available")
                return
            
            # Price info
            price = data.get('price', 0)
            change = data.get('change', 0)
            change_pct = data.get('change_percent', 0)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Price", f"${price:.2f}")
            
            with col2:
                color = "green" if change >= 0 else "red"
                st.markdown(f"<span style='color: {color}; font-size: 1.2em;'>{change:+.2f} ({change_pct:+.2f}%)</span>", unsafe_allow_html=True)
            
            # Volume
            volume = data.get('volume', 0)
            st.caption(f"Volume: {volume:,}")
    
    def calculate_score(self, indicators: Dict) -> float:
        """Calculate overall score from indicators"""
        try:
            score = 50.0  # Base score
            
            # RSI contribution
            rsi = indicators.get('rsi', 50)
            if rsi < 30:
                score += 20  # Oversold - bullish
            elif rsi > 70:
                score -= 20  # Overbought - bearish
            
            # MACD contribution
            macd = indicators.get('macd', 0)
            if macd > 0:
                score += 15  # Positive MACD
            else:
                score -= 15  # Negative MACD
            
            # Volume contribution
            volume_sma = indicators.get('volume_sma', 1)
            if volume_sma > 1.5:
                score += 10  # High volume
            elif volume_sma < 0.5:
                score -= 10  # Low volume
            
            return max(0, min(100, score))
            
        except Exception:
            return 50.0
    
    def get_signal(self, score: float) -> str:
        """Get trading signal based on score"""
        if score >= 70:
            return "🟢 BUY"
        elif score <= 30:
            return "🔴 SELL"
        else:
            return "🟡 HOLD"
    
    def check_scalping_opportunity(self, indicators: Dict) -> Dict:
        """Check for scalping opportunities"""
        try:
            score = self.calculate_score(indicators)
            
            # Define scalping criteria
            rsi = indicators.get('rsi', 50)
            macd = indicators.get('macd', 0)
            atr = indicators.get('atr', 0)
            
            opportunity = False
            signal = "HOLD"
            reason = ""
            
            # Strong buy signal
            if score >= 75 and rsi < 40 and macd > 0:
                opportunity = True
                signal = "BUY"
                reason = "Strong bullish indicators"
            
            # Strong sell signal
            elif score <= 25 and rsi > 60 and macd < 0:
                opportunity = True
                signal = "SELL"
                reason = "Strong bearish indicators"
            
            return {
                'opportunity': opportunity,
                'signal': signal,
                'score': score,
                'reason': reason
            }
            
        except Exception:
            return {
                'opportunity': False,
                'signal': 'HOLD',
                'score': 50,
                'reason': 'Error calculating signals'
            }
    
    def show_schwab_auth(self):
        """Show Schwab authentication interface"""
        self.schwab_auth.show_auth_interface()

def main():
    """Main function"""
    try:
        dashboard = SimpleOptionsScalpingDashboard()
        dashboard.run()
    except Exception as e:
        st.error(f"Application error: {e}")
        st.info("Please refresh the page or contact support if the issue persists.")

if __name__ == "__main__":
    main() 