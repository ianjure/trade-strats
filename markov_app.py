import streamlit as st
import yfinance as yf
from streamlit_extras.stylable_container import stylable_container
from markov_functions import preprocess, create_transition_matrix, run_simulation

# PAGE CONFIGURATIONS
st.title("Markov Trading")
hide = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide, unsafe_allow_html=True)

# GET ALL TICKER SYMBOLS
text = open("assets/stocks_clean.txt", "r")
all_stocks = text.read().split("|")
text.close()

# MAIN UI
with st.container(border=True):
    tickers = st.selectbox("SELECT A STOCK", all_stocks)
    c1, c2, c3 = st.columns(3)
    col1, col2 = st.columns(2)

with c1:
    amount = st.number_input("INPUT INITIAL INVESTMENT", value=100)
    threshold = st.number_input("INPUT THRESHOLD", value=0.45, min_value=0.01, max_value=1.00)

with c2:
    premium = st.number_input("INPUT PREMIUM PRICE", value=5)
    interval = st.selectbox("CHOOSE AN INTERVAL", ("1d", "2d", "5d", "10d"))
    
with c3:
    shares = st.number_input("INPUT NUMBER OF SHARES", value=5, step=1)
    verbose = st.selectbox("SHOW ALL INFO", ("True", "False"))
        
with col1:
    chart_btn = st.button("**SHOW INFO**", type="secondary", use_container_width=True)
        
with col2:
    predict_btn = st.button("SIMULATE RETURNS", type="primary", use_container_width=True)

if chart_btn:
    with st.spinner('Fetching stock information...'):
        ticker = tickers.split("-")[0].replace(" ", "")
        stock = yf.Ticker(ticker)
        stock_name = stock.info['shortName']
        stock_website = stock.info['website']
        stock_sector = stock.info['sector']
        stock_industry = stock.info['industry']
        stock = stock.history(period="max")
            
        with st.container(border=True):
            info_1, info_2 = st.columns(2)
                
        with info_1:
            st.write(f"**Company Name:** {stock_name}")
            st.write(f"**Website:** {stock_website}")
                
        with info_2:
            st.write(f"**Sector:** {stock_sector}")
            st.write(f"**Industry:** {stock_industry}")
                
        st.dataframe(stock.tail(), use_container_width=True)
        st.line_chart(data=stock, x=None, y='Close', x_label='Years', y_label='Price', use_container_width=True)

if predict_btn:
    with st.spinner('Calculating state probabilities...'):
        ticker = tickers.split("-")[0].replace(" ", "")
        stock = yf.Ticker(ticker)
        stock_name = stock.info['shortName']
        stock_ticker = stock.info['symbol']
        stock = stock.history(period="max")
        stock_processed = preprocess(stock)
        transition_matrix = create_transition_matrix(stock_processed)
        st.dataframe(transition_matrix)

        if verbose == "True":
            result = run_simulation(amount=amount, premium=premium, shares=shares, stock=stock, threshold=threshold, interval=interval, verbose=True)
        else:
            result = run_simulation(amount=amount, premium=premium, shares=shares, stock=stock, threshold=threshold, interval=interval, verbose=False)
        st.write(result)
