import streamlit as st
import yfinance as yf
from meanreversion_functions import preprocess, run_simulation

# PAGE CONFIGURATIONS
hide = """
    <style>
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide, unsafe_allow_html=True)

# TITLE
st.markdown("<p style='text-align: center; font-size: 3.4rem; font-weight: 800; line-height: 0.8;'>Mean Reversion</p>", unsafe_allow_html=True)

# SUBTITLE
st.markdown("<p style='text-align: center; font-size: 1rem; font-weight: 500; line-height: 1.2;'>A trading algorithm based on a popular financial theory.</p>", unsafe_allow_html=True)

# GET ALL TICKER SYMBOLS
text = open("assets/stocks_clean.txt", "r")
all_stocks = text.read().split("|")
text.close()

# MAIN UI
with st.container(border=True):
    tickers = st.selectbox("**STOCK**", all_stocks)
    amount = st.number_input("**INITIAL AMOUNT**", value=100)
    btn1, btn2 = st.columns(2)

with btn1:
    chart_btn = st.button("**SHOW INFO**", type="secondary", use_container_width=True)
with btn2:
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
            info_1.write(f"**Company Name:** {stock_name}")
            info_1.write(f"**Website:** {stock_website}")
            info_2.write(f"**Sector:** {stock_sector}")
            info_2.write(f"**Industry:** {stock_industry}")
                
        st.dataframe(stock.tail(), use_container_width=True)
        st.line_chart(data=stock, x=None, y='Close', x_label='Years', y_label='Price', use_container_width=True)

if sim_btn:
    with st.spinner('Calculating expected returns...'):
        ticker = tickers.split("-")[0].replace(" ", "")
        stock = yf.Ticker(ticker)
        stock = stock.history(period="max")

        fig, actions, total_earnings, equity, ROI = run_simulation(stock=stock, amount=amount)
        
        with st.container(border=True):
            st.pyplot(fig)
        
        with st.container(border=True):
            buy_col, sell_col, total_col = st.columns(3)
            buy_col.metric("Buy", f"{actions['Buy']}")
            sell_col.metric("Sell", f"{actions['Sell']}")
            total_col.metric("Total Actions", f"{actions['Total Actions']}")
          
            te_col, eq_col, roi_col = st.columns(3)
            te_col.metric("Total Earnings", f"{round(total_earnings, 2)}$")
            eq_col.metric("Total Amount", f"{round(equity, 2)}$")
            roi_col.metric("Return on Investment", f"{round(ROI, 2)}%")
