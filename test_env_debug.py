#!/usr/bin/env python3
"""
Simple Streamlit test for environment variables debugging
"""

import streamlit as st
import os
from dotenv import load_dotenv

st.title("🔧 Environment Variables Debug Test")

# Test 1: Direct loading
st.write("### Test 1: Direct Environment Variable Loading")
load_dotenv(".env")
schwab_id = os.getenv("SCHWAB_CLIENT_ID")
st.write(f"**Direct load result**: {'✅ Found' if schwab_id else '❌ NOT FOUND'}")
if schwab_id:
    st.write(f"**Value**: {schwab_id[:10]}...")

# Test 2: Check all environment variables
st.write("### Test 2: All Environment Variables")
env_vars = {k: v for k, v in os.environ.items() if 'SCHWAB' in k}
st.write("**Schwab-related environment variables:**")
for key, value in env_vars.items():
    st.write(f"- {key}: {'SET' if value else 'NOT SET'}")

# Test 3: Check .env file
st.write("### Test 3: .env File Check")
env_exists = os.path.exists(".env")
st.write(f"**.env file exists**: {'✅ Yes' if env_exists else '❌ No'}")
st.write(f"**Current working directory**: {os.getcwd()}")

# Test 4: Read .env file directly
if env_exists:
    st.write("### Test 4: .env File Contents")
    try:
        with open(".env", "r") as f:
            env_contents = f.read()
        st.code(env_contents, language="bash")
    except Exception as e:
        st.error(f"Error reading .env file: {e}")

# Test 5: Streamlit secrets
st.write("### Test 5: Streamlit Secrets")
if hasattr(st, 'secrets'):
    st.write("**Streamlit secrets available**: ✅ Yes")
    if 'SCHWAB_CLIENT_ID' in st.secrets:
        st.write("**SCHWAB_CLIENT_ID in secrets**: ✅ Found")
    else:
        st.write("**SCHWAB_CLIENT_ID in secrets**: ❌ Not found")
else:
    st.write("**Streamlit secrets available**: ❌ No")

# Test 6: Function test
def test_env_loading():
    load_dotenv(".env")
    return os.getenv("SCHWAB_CLIENT_ID")

st.write("### Test 6: Function Test")
result = test_env_loading()
st.write(f"**Function result**: {'✅ Found' if result else '❌ NOT FOUND'}")

# Test 7: Manual environment variable setting
st.write("### Test 7: Manual Environment Variable Setting")
if st.button("Set Environment Variable Manually"):
    os.environ['SCHWAB_CLIENT_ID'] = 'ldUA8vYfffffryNx194I5cWeWDSy2Jl1'
    st.success("Environment variable set manually!")
    st.write(f"**New value**: {os.getenv('SCHWAB_CLIENT_ID', 'NOT FOUND')}") 