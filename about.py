import streamlit as st

# PAGE CONFIGURATIONS
hide = """
    <style>
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide, unsafe_allow_html=True)

# TITLE
st.markdown("<p style='text-align: center; font-size: 3.8rem; font-weight: 800; line-height: 0.8;'>Trade Strats</p>", unsafe_allow_html=True)

# SUBTITLE
st.markdown("<p style='text-align: center; font-size: 1.2rem; font-weight: 500;'>A platform for testing trading algorithms,</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem; font-weight: 500;'>built with Streamlit.</p>", unsafe_allow_html=True)
