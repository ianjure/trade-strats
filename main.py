import streamlit as st

# PAGE SETUP
about_page = st.Page(
    "about.py",
    title="TradeStrats",
    icon=":material/home:",
    default=True,
)
markov_page = st.Page(
    "markovchain.py",
    title="Markov Chain - TradeStrats",
    icon=":material/link:",
)
meanrev_page = st.Page(
    "meanreversion.py",
    title="Mean Reversion - TradeStrats",
    icon=":material/history:",
)

# NAVIGATION SETUP
pg = st.navigation(
    {
        "Home": [about_page],
        "Algorithms": [markov_page, meanrev_page],
    }
)

# RUN NAVIGATION
pg.run()
