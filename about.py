import streamlit as st

# PAGE CONFIGURATIONS
hide = """
    <style>
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide, unsafe_allow_html=True)

# TITLE
st.markdown("<p style='text-align: center; padding-top: 3rem; font-size: 8rem; font-weight: 800;'>Tradestrats</p>", unsafe_allow_html=True)

# SUBTITLE
st.markdown("<p style='text-align: center; padding-top: 1rem; margin-left: 1rem; margin-right: 1rem; font-size: 2rem; font-weight: 500;'>A platform for testing trading algorithms, built with Streamlit.</p>", unsafe_allow_html=True)

