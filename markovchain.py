import streamlit as st
import yfinance as yf
from markovchain_functions import preprocess, create_transition_matrix, run_simulation

# PAGE CONFIGURATIONS
st.set_page_config(page_title="Markov Chain - TradeStrats", page_icon="📈")

hide = """
    <style>
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide, unsafe_allow_html=True)

# DESIGN COMPONENT
metric = """
        <style>
        label[data-testid="stMetricLabel"] {
            display: flex;
        }
        div[data-testid="stMetric"] {
            text-align: center;
        }
        </style>
        """
st.markdown(metric, unsafe_allow_html=True)

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
    btn1, btn2 = st.columns(2)

with c1:
    amount = st.number_input("**INITIAL AMOUNT**", value=100)
with c2:
    threshold = st.number_input("**THRESHOLD**", value=0.45, min_value=0.01, max_value=1.00)
with c3:
    interval = st.selectbox("**TRADE INTERVAL**", ("1d", "2d", "5d", "10d"))

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
    with st.spinner('Calculating state probabilities...'):
        ticker = tickers.split("-")[0].replace(" ", "")
        stock = yf.Ticker(ticker)
        stock = stock.history(period="max")

        fig, actions, status, total_amount = run_simulation(stock=stock, amount=amount, threshold=threshold, interval=interval)
        
        with st.container(border=True):
            st.pyplot(fig)

        with st.container(border=True):
            buy_col, hold_col, sell_col, total_col = st.columns(4)
            wr_col, profit_col, amount_col = st.columns(3)
            
        buy_col.metric("Buy", f"{actions['Buy']}")
        hold_col.metric("Hold", f"{actions['Hold']}")
        sell_col.metric("Sell", f"{actions['Sell']}")
        total_col.metric("Total Actions", f"{actions['Total Actions']}")
        
        if status["Win"] == 0 and status["Lose"] == 0:
            wr_col.metric("Win Rate", "0%")
        else:
            wr_col.metric("Win Rate", f"{round((status['Win'] / (status['Win'] + status['Lose'])) * 100, 2)}%")
        profit_col.metric("Total Profit", f"{round(total_amount - amount, 2)}$")
        with st.container(border=True):
            amount_col.metric("Total Amount", f"{round(total_amount, 2)}$")
