import pandas as pd
import numpy as np

def preprocess(stock):
    # Drop unnecessary columns
    del stock["Dividends"]
    del stock["Stock Splits"]

    # Convert the index to a datetime object
    stock.index = stock.index.strftime('%Y-%m-%d')
    stock.index = pd.to_datetime(stock.index)

    # Calculate daily returns
    stock["Daily Returns"] = stock["Close"].pct_change()

    # Create the current and future state columns
    conditions = [stock['Daily Returns'] > 0.005, stock['Daily Returns'] < 0]
    stock["CurrentState"] = np.select(conditions, ["Up", "Down"], default="Neutral")
    stock["FutureState"] = stock["CurrentState"].shift(-1)

    return stock
