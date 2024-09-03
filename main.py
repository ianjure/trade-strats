import streamlit as st

st.title("Main Menu")

pages = {
    "Info": [
        st.Page("home/home.py", title="Home", icon="🏠")
    ],
    "Strategies": [
        st.Page("markov/markov_app.py", title="Markov", icon="1️⃣"),
        st.Page("mean-reversion/meanrev_app.py", title="Mean Reversion", icon="🔥")
    ],
}

pg = st.navigation(pages)
pg.run()
