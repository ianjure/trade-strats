import streamlit as st

# --- PAGE SETUP ---
home_page = st.Page(
    "home.py",
    title="Home",
    icon=":material/account_circle:",
    default=True,
)
markov_page = st.Page(
    "markov_app.py",
    title="Markov",
    icon=":material/bar_chart:",
)
meanrev_page = st.Page(
    "meanrev_app.py",
    title="Mean Reversion",
    icon=":material/smart_toy:",
)

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Info": [home_page],
        "Strategies": [markov_page, meanrev_page],
    }
)

# --- RUN NAVIGATION ---
pg.run()
