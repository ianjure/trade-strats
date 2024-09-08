import streamlit as st

# PAGE CONFIGURATIONS
hide = """
    <style>
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide, unsafe_allow_html=True)

# TITLE
st.image(image="assets/logo.svg", width=200, use_column_width="auto")

# SUBTITLE
st.markdown("<p style='text-align: center; font-size: 1.2rem; font-weight: 500; line-height: 1.2;'>A platform for testing trading algorithms, built with Streamlit.</p>", unsafe_allow_html=True)
