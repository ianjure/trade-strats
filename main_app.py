import streamlit as st

st.title("Main Menu")

st.Page(page="main_app.py", title="Home", icon="🏠"),
st.Page(page="markov/markov_app.py", title="Markov", icon="1️⃣"),
st.Page(page="mean-reversion/meanrev_app.py", title="Mean Reversion", icon="🔥")
