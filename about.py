import streamlit as st

# PAGE CONFIGURATIONS
hide = """
    <style>
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide, unsafe_allow_html=True)

# TITLE
st.markdown("<p style='text-align: center; padding-top: 3.5rem; font-size: 5rem; font-weight: 800; line-height: 0.8;'>Tradestrats</p>", unsafe_allow_html=True)

# SUBTITLE
st.markdown("<p style='text-align: center; font-size: 1.4rem; font-weight: 500; line-height: 1.4;'>A platform for testing trading algorithms,</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.4rem; font-weight: 500; line-height: 1.4;'>built with Streamlit.</p>", unsafe_allow_html=True)
