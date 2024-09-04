import streamlit as st

# PAGE CONFIGURATIONS
hide = """
    <style>
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide, unsafe_allow_html=True)

# TITLE
st.markdown("<p style='text-align: center; font-size: 3.4rem; font-weight: 800; line-height: 0.8;'>TradeStrats</p>", unsafe_allow_html=True)

# SUBTITLE
st.markdown("<p style='text-align: center; font-size: 1rem; font-weight: 500; line-height: 1.2;'>A platform for testing trading algorithms, built with Streamlit.</p>", unsafe_allow_html=True)

