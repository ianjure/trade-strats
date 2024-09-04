import streamlit as st
import yfinance as yf
from streamlit_extras.stylable_container import stylable_container
from markov_functions import preprocess, create_transition_matrix, run_simulation

# PAGE CONFIGURATIONS
hide = """
    <style>
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide, unsafe_allow_html=True)

# TITLE
st.markdown("<p style='text-align: center; font-size: 3.4rem; font-weight: 800; line-height: 0.8;'>Markov Chain</p>", unsafe_allow_html=True)

# SUBTITLE
st.markdown("<p style='text-align: center; font-size: 1rem; font-weight: 500; line-height: 1.2;'>A trading algorithm based on Markov probability theory.</p>", unsafe_allow_html=True)

# GET ALL TICKER SYMBOLS
text = open("assets/stocks_clean.txt", "r")
all_stocks = text.read().split("|")
text.close()

# MAIN UI
with st.container(border=True):
    tickers = st.selectbox("**STOCK**", all_stocks)
    c1, c2, c3 = st.columns(3)
    col1, col2 = st.columns(2)

with c1:
    amount = st.number_input("**INITIAL AMOUNT**", value=100)

with c2:
    premium = st.number_input("**PREMIUM PRICE**", value=5)
    
with c3:
    shares = st.number_input("**SHARES PER OPTION**", value=5, step=1)
        
with col1:
    threshold = st.number_input("**THRESHOLD**", value=0.45, min_value=0.01, max_value=1.00)
    chart_btn = st.button("**SHOW INFO**", type="secondary", use_container_width=True)
        
with col2:
    interval = st.selectbox("**TRADE INTERVAL**", ("1d", "2d", "5d", "10d"))
    sim_btn = st.button("**SIMULATE RETURNS**", type="primary", use_container_width=True)

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

if sim_btn:
    with st.spinner('Calculating state probabilities...'):
        ticker = tickers.split("-")[0].replace(" ", "")
        stock = yf.Ticker(ticker)
        stock_name = stock.info['shortName']
        stock_ticker = stock.info['symbol']
        stock = stock.history(period="max")

        fig, actions, status, total_amount = run_simulation(amount=amount, premium=premium, shares=shares, stock=stock, threshold=threshold, interval=interval)
        st.pyplot(fig)
        
        with st.container(border=True):
            buy_col, hold_col, sell_col, total_col = st.columns(4)
            wr_col, profit_col, amount_col = st.columns(3)

        with buy_col:
            st.write(f'Buy: {actions["Buy"]}')
        with hold_col:
            st.write(f'Hold: {actions["Hold"]}')
        with sell_col:
            st.write(f'Sell: {actions["Sell"]}')
        with total_col:
            st.write(f'Total Actions: {actions["Total Actions"]}')

        if status["Win"] == 0 and status["Lose"] == 0:
            with wr_col:
                st.write('Win Rate: 0%')
            with profit_col:
                st.write(f'Total Profit: {round(total_amount - amount, 2)}$')
            with amount_col:
                st.write(f'Total Amount: {round(total_amount, 2)}$')
        else:
            with wr_col:
                st.write(f'Win Rate: {round((status["Win"] / (status["Win"] + status["Lose"])) * 100, 2)}%')
            with profit_col:
                st.write(f'Total Profit: {round(total_amount - amount, 2)}$')
            with amount_col:
                st.write(f'Total Amount: {round(total_amount, 2)}$')
