import streamlit as st

# --- PAGE SETUP ---
home_page = st.Page(
    "home.py",
    title="Home",
    icon=":material/home:"
    default=True,
)
markov_page = st.Page(
    "markov_app.py",
    title="Markov Chain",
    icon=":material/link:",
)
meanrev_page = st.Page(
    "meanrev_app.py",
    title="Mean Reversion",
    icon=":material/history:",
)

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "About": [home_page],
        "Trading Algorithms": [markov_page, meanrev_page],
    }
)

# --- RUN NAVIGATION ---
pg.run()
