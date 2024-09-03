import streamlit as st

st.title("Main Menu")

main_page = st.Page(page="main_app.py", title="Home", icon="🏠", default=True),
markov_page = st.Page(page="markov/markov_app.py", title="Markov", icon="1️⃣"),
meanrev_page = st.Page(page="mean-reversion/meanrev_app.py", title="Mean Reversion", icon="🔥")

pg = st.navigation(
    {
        "Info": [main_page],
        "Strategies": [markov_page, meanrev_page],
    }
)
pg.run()
