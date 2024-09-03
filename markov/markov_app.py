import streamlit as st

st.title("Markov")

# GET ALL TICKER SYMBOLS
text = open("assets/stocks_clean.txt", "r")
all_stocks = text.read().split("|")
text.close()

# MAIN UI
with st.container(border=True):
    tickers = st.selectbox("SELECT A STOCK", all_stocks)
    timeframe = st.selectbox("CHOOSE A TIMEFRAME", ("Week", "Month"))
    col1, col2 = st.columns(2)
        
with col1:
    chart_btn = st.button("**SHOW INFO**", type="secondary", use_container_width=True)
        
with col2:
    with stylable_container(
        key = "pred_button",
        css_styles = """
        button[data-testid="stBaseButton-primary"] {
            color: black;
        }
        """
        ):
        predict_btn = st.button("PREDICT TREND", type="primary", use_container_width=True)

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
    with st.spinner('Calculating the prediction...'):
        ticker = tickers.split("-")[0].replace(" ", "")
        stock = yf.Ticker(ticker)
        stock_name = stock.info['shortName']
        stock_ticker = stock.info['symbol']
        stock = stock.history(period="max")
        stock = format_week(stock) if timeframe == 'Week' else format_month(stock)
        
        if timeframe == 'Week':
            predictors = ['Close_Ratio_4', 'Trend_4', 'Close_Ratio_13', 'Trend_13', 'Close_Ratio_26', 'Trend_26', 'Close_Ratio_52', 'Trend_52', 'Close_Ratio_208', 'Trend_208', 'Crude Oil', 'Effective Rate', 'Interest Rate']
        else:
            predictors = ['Close_Ratio_2', 'Trend_2', 'Close_Ratio_6', 'Trend_6', 'Close_Ratio_12', 'Trend_12', 'Close_Ratio_30', 'Trend_30', 'Close_Ratio_60', 'Trend_60', 'Crude Oil', 'Effective Rate', 'Interest Rate']
            
        model = LogisticRegression(random_state=1)
        result = backtest(stock, model, predictors, timeframe)
        
        with st.container(border=True):
            if timeframe == 'Week':
                if result['Predictions'][-1] > 0:
                    st.success(f"**{stock_name} ({stock_ticker})** stock price will go up next week.", icon="✔️")
                    st.info(f"**Confidence:** {round(result['Confidence'][-1] * 100)}%")
                else:
                    st.error(f"**{stock_name} ({stock_ticker})** stock price will go down next week.", icon="🔻")
                    st.info(f"**Confidence:** {round((1 - result['Confidence'][-1]) * 100)}%")
            else:
                if result['Predictions'][-1] > 0:
                    st.success(f"**{stock_name} ({stock_ticker})** stock price will go up next month.", icon="✔️")
                    st.info(f"**Confidence:** {round(result['Confidence'][-1] * 100)}%")
                else:
                    st.error(f"**{stock_name} ({stock_ticker})** stock price will go down next month.", icon="🔻")
                    st.info(f"**Confidence:** {round((1 - result['Confidence'][-1]) * 100)}%")
