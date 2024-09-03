import streamlit as st

st.title("Main Menu")

pg = st.navigation([
    st.page_link("main_app.py", label="Home", icon="🏠")
    st.page_link("markov/markov_app.py", label="Markov", icon="1️⃣")
    st.page_link("mean-reversion/meanrev_app.py", label="Mean Reversion", icon="🔥")
])
