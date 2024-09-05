import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt
import math

def preprocess(stock):
    # Drop unnecessary columns
    del stock["Open"]
    del stock["High"]
    del stock["Low"]
    del stock["Volume"]
    del stock["Dividends"]
    del stock["Stock Splits"]

    # Rename 'Close' column to 'Price'
    stock.rename(columns={"Close": "Price"}, inplace=True)

    # Convert the index to a datetime object
    stock.index = stock.index.strftime('%Y-%m-%d')
    stock.index = pd.to_datetime(stock.index)

    # Calculate RSI 10 and SMA 200
    stock["RSI 10"] = ta.rsi(stock["Price"], length = 10)
    stock["SMA 200"] = ta.sma(stock["Price"], length = 200)

    return stock

def run_simulation(stock, amount):
    # Initialize trading variables
    in_position = False
    equity = amount

    # Preprocess the stock data
    stock = preprocess(stock)

    # Initialize starting date (2000-01-01)
    start_date = pd.to_datetime("2000-01-01")
    stock = stock.loc[start_date:]

    # Initialize the plot
    fig, ax = plt.subplots(figsize = (20, 5))
    ax.plot(stock["Price"], color="black")
    ax.plot(stock["RSI 10"], color="orange")
    ax.plot(stock["SMA 200"], color="blue")
    ax.legend(["Price", "RSI 10", "SMA 200"], loc="upper left")

    # Create a dictionary for trade actions
    trade_actions = {
        "Buy": 0,
        "Sell": 0,
        "Total Actions": 0
    }

    # Loop through the stock data
    for i in range(0, len(stock)):

        # Entry (Buy): RSI 10 < 30 and Price > SMA 200
        if stock.iloc[i]["RSI 10"] < 30 and stock.iloc[i]["Price"] > stock.iloc[i]["SMA 200"] and in_position == False:

              # Calculate the number of shares to buy
              shares = math.floor(equity / stock.iloc[i]["Price"])

              # Buy the stock shares and set in position to true
              equity = equity - (shares * stock.iloc[i]["Price"])
              in_position = True

              # Action: Buy
              trade_actions["Buy"] += 1
              trade_actions["Total Actions"] += 1

              # Draw buy line
              ax.axvline(x=stock.index[i], color = 'g', lw=0.5)

        # Exit (Sell): RSI 10 > 370 and Price < SMA 200.
        elif stock.iloc[i]["RSI 10"] > 70 and stock.iloc[i]["Price"] < stock.iloc[i]["SMA 200"] and in_position == True:
            
              # Sell the stock shares and set in position to false
              equity = equity + (shares * stock.iloc[i]["Price"])
              in_position = False

              # Action: Sell
              trade_actions["Sell"] += 1
              trade_actions["Total Actions"] += 1

              # Draw sell line
              ax.axvline(x=stock.index[i], color = 'r', lw=0.5)

    # Close positions
    if in_position == True:
        equity = equity + (shares * stock.iloc[i]["Price"])
        in_position = False

        # Action: Sell
        trade_actions["Sell"] += 1
        trade_actions["Total Actions"] += 1

        # Draw close position line
        ax.axvline(x=stock.index[i], color = 'y', lw=0.5)

    # Calculate total earnings and return on investment
    total_earnings = round(equity - amount, 2)
    ROI = round(total_earnings / amount * 100, 2)
    
    return fig, trade_actions, total_earnings, equity, ROI
