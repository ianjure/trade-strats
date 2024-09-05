import streamlit as st
import yfinance as yf
from streamlit_extras.stylable_container import stylable_container
from meanreversion_functions import preprocess, run_simulation

# TITLE
st.markdown("<p style='text-align: center; font-size: 3.4rem; font-weight: 800; line-height: 0.8;'>Mean Reversion</p>", unsafe_allow_html=True)
