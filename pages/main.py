import streamlit as st

st.title("Main Menu")

pages = {
    "Info": [
        st.Page("pages/main.py", title="Home", icon="🏠")
    ],
    "Strategies": [
        st.Page("pages/markov_app.py", title="Markov", icon="1️⃣"),
        st.Page("pages/meanrev_app.py", title="Mean Reversion", icon="🔥")
    ],
}

pg = st.navigation(pages)
pg.run()
