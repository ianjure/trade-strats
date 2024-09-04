import streamlit as st

# PAGE SETUP
about_page = st.Page(
    "about.py",
    title="About",
    icon=":material/home:",
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

# NAVIGATION SETUP
pg = st.navigation(
    {
        "Home": [about_page],
        "Algorithms": [markov_page, meanrev_page],
    }
)

# RUN NAVIGATION
pg.run()
