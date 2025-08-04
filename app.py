#!/usr/bin/env python3
"""
Streamlit Cloud Entry Point for Options Scalping Application
"""

import streamlit as st
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the main Streamlit app
from ui.streamlit_app import main

if __name__ == "__main__":
    main() 