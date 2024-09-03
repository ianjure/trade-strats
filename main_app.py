import streamlit as st

st.title("Main Menu")

main = st.Page(page="main_app.py", title="Home", icon="🏠", default=True),
markov = st.Page(page="markov/markov_app.py", title="Markov", icon="1️⃣"),
meanrev = st.Page(page="mean-reversion/meanrev_app.py", title="Mean Reversion", icon="🔥")
