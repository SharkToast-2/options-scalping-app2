#!/usr/bin/env python3
"""
Simple Streamlit test for environment variables
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")

st.title("🔧 Environment Variables Test")

# Test environment variables
schwab_client_id = os.getenv("SCHWAB_CLIENT_ID")
schwab_client_secret = os.getenv("SCHWAB_CLIENT_SECRET")

st.write("### Environment Variables Status:")
st.write(f"**SCHWAB_CLIENT_ID**: {'✅ Found' if schwab_client_id else '❌ NOT FOUND'}")
if schwab_client_id:
    st.write(f"**Value**: {schwab_client_id[:10]}...")
st.write(f"**SCHWAB_CLIENT_SECRET**: {'✅ Found' if schwab_client_secret else '❌ NOT FOUND'}")

# Test market status
try:
    from modules.data_fetcher import data_fetcher
    market_status = data_fetcher.get_market_status()
    st.write("### Market Status Test:")
    st.write(f"**Is Open**: {'✅ YES' if market_status['is_open'] else '❌ NO'}")
    st.write(f"**Time to Close**: {market_status['time_to_close']/3600:.1f} hours")
    st.write(f"**Time to Open**: {market_status['time_to_open']/3600:.1f} hours")
except Exception as e:
    st.error(f"❌ Error testing market status: {e}")

st.write("### Raw Environment Variables:")
for key, value in os.environ.items():
    if 'SCHWAB' in key:
        st.write(f"**{key}**: {value[:10]}..." if value else "NOT SET") 