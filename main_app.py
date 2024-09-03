import streamlit as st

st.title("Main Menu")

pg = st.navigation([
    st.Page("main_app.py", title="Main Menu", icon="🔥"),
    st.Page("markov/markov_app.py", title="Markov", icon="🔥"),
    st.Page("mean-reversion/meanrev_app.py", title="Mean Reversion", icon="🔥")
])
pg.run()
