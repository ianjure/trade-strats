import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

def create_transition_matrix(stock):
    # Count all occurences of each states
    up_count = len(stock.query('CurrentState == "Up"'))
    neutral_count = len(stock.query('CurrentState == "Neutral"'))
    down_count = len(stock.query('CurrentState == "Down"'))

    # Count all transitions from up to other states
    up_to_up = len(stock.query('CurrentState == "Up" and FutureState == "Up"'))
    up_to_neutral = len(stock.query('CurrentState == "Up" and FutureState == "Neutral"'))
    up_to_down = len(stock.query('CurrentState == "Up" and FutureState == "Down"'))

    # Count all transitions from neutral to other states
    neutral_to_up = len(stock.query('CurrentState == "Neutral" and FutureState == "Up"'))
    neutral_to_neutral = len(stock.query('CurrentState == "Neutral" and FutureState == "Neutral"'))
    neutral_to_down = len(stock.query('CurrentState == "Neutral" and FutureState == "Down"'))

    # Count all transitions from down to other states
    down_to_up = len(stock.query('CurrentState == "Down" and FutureState == "Up"'))
    down_to_neutral = len(stock.query('CurrentState == "Down" and FutureState == "Neutral"'))
    down_to_down = len(stock.query('CurrentState == "Down" and FutureState == "Down"'))

    # Calculate the transition probabilities from up
    prob_up_to_up = up_to_up / up_count
    prob_up_to_neutral = up_to_neutral / up_count
    prob_up_to_down = up_to_down / up_count

    # Calculate the transition probabilities from neutral
    prob_neutral_to_up = neutral_to_up / neutral_count
    prob_neutral_to_neutral = neutral_to_neutral / neutral_count
    prob_neutral_to_down = neutral_to_down / neutral_count

    # Calculate the transition probabilities from neutral
    prob_down_to_up = down_to_up / down_count
    prob_down_to_neutral = down_to_neutral / down_count
    prob_down_to_down = down_to_down / down_count

    # Create the transition matrix
    up_prob_list = [prob_up_to_up, prob_up_to_neutral, prob_up_to_down]
    neutral_prob_list = [prob_neutral_to_up, prob_neutral_to_neutral, prob_neutral_to_down]
    down_prob_list = [prob_down_to_up, prob_down_to_neutral, prob_down_to_down]

    transition_matrix = pd.DataFrame([up_prob_list, neutral_prob_list, down_prob_list],
                                    columns=['Up', 'Neutral', 'Down'],
                                    index=['Up', 'Neutral', 'Down'])

    return transition_matrix

def run_simulation(amount, premium, shares, stock, threshold, interval="1d", verbose=False):

    """
    Simulates the execution of the strategy within an options trading environment.

    Args:
        amount (int): The initial capital available for investment.
        premium (int): The premium price for each option contract.
        shares (int): The number of shares per option contract to trade.
        stock (pd.DataFrame): Historical stock data used for simulation. The DataFrame should be from Yahoo Finance.
        threshold (float): The probability threshold for making a trade decision. Trades are executed when this threshold is met or exceeded.
        interval (str): The time interval between trades, specified in days. Valid options are '1d', '2d', '5d', or '10d'.
        verbose (bool): If True, detailed information about the simulation is shown.

    Returns:
        None: The function displays a plot of the simulated trades and their corresponding expected returns.
    """

    # Initialize trading variables
    initial_amount = amount
    total_amount = amount

    # Preprocess the stock data
    stock = preprocess(stock)

    # Initialize starting date (must be 1 year before the present date)
    latest_date = stock.index[-1]
    start_year = int(str(latest_date)[0:4]) - 1
    start_date = f"{start_year}" + str(latest_date)[4:]

    # Convert the start date to a datetime object
    start_date = pd.to_datetime(start_date)
    stock = stock.loc[start_date:]

    # Initialize the plot
    plt.figure(figsize = (20, 5), facecolor='white')
    plt.title(f"{ticker} Stock Price", fontsize=20, color='black')
    plt.plot(stock["Close"])


    # Create a dictionary for trade actions
    trade_actions = {
        "Buy": 0,
        "Hold": 0,
        "Sell": 0,
        "Total Actions": 0
    }

    # Create a dictionary for trade status
    trade_status = {
        "Win": 0,
        "Lose": 0,
    }

    # Set the interval
    if interval == "1d":
        interval = 1
    elif interval == "2d":
        interval = 2
    elif interval == "5d":
        interval = 5
    elif interval == "10d":
        interval = 10
    else:
        raise ValueError("Invalid interval. Must be 1d, 2d, 5d, or 10d.")

    for i in range(50, stock.shape[0], interval):
        train = stock.iloc[0:i].copy()

        # Create transition matrix
        transition_matrix = create_transition_matrix(train)

        # Get the current state
        current_state = train.iloc[-1]["CurrentState"]

        # Get the probability of the transition from current to future state
        prob = transition_matrix.loc[current_state]

        # Check if the maximum probability of is higher than the threshold
        if max(prob) >= threshold:

            # Get the index of the maximum probability
            max_prob = prob.idxmax()

            # Draw trade lines, increment trade actions and status, and calculate the profit
            if max_prob == "Up":

                # Action: Buy or Call Option
                trade_actions["Buy"] += 1
                trade_actions["Total Actions"] += 1

                if np.isnan(stock.shift(-1).iloc[-2]["Open"]):
                    continue

                # Get today's closing price
                buying_price = stock.iloc[i]["Close"]

                # Get tomorrow's opening price
                market_price = stock.shift(-1).iloc[-2]["Open"]

                # Check if it is a losing or a winning trade
                if market_price < buying_price:

                    # In a Call Option: Market Price < Buying Price is a losing trade
                    plt.axvline(x=train.index[-1], color = 'r', lw=0.5)

                    # Pay for the premium
                    total_amount = total_amount - (premium * shares)

                    # Update trade status
                    trade_status["Lose"] += 1

                else:
                    # In a Call Option: Market Price > Buying Price is a winning trade
                    plt.axvline(x=train.index[-1], color = 'g', lw=0.5)

                    # Calculate the profit
                    gross_profit = market_price - buying_price
                    net_profit = gross_profit - premium
                    trade_profit = net_profit * shares
                    total_amount = total_amount + trade_profit

                    # Update trade status
                    trade_status["Win"] += 1

            elif max_prob == "Neutral":

                # Action: Hold or None
                trade_actions["Hold"] += 1
                trade_actions["Total Actions"] += 1

            elif max_prob == "Down":

                # Action: Sell or Put Option
                trade_actions["Sell"] += 1
                trade_actions["Total Actions"] += 1

                if np.isnan(stock.shift(-1).iloc[-2]["Open"]):
                    continue

                # Get today's closing price
                selling_price = stock.iloc[i]["Close"]

                # Get tomorrow's opening price
                market_price = stock.shift(-1).iloc[-2]["Open"]

                # Check if it is a losing or a winning trade
                if market_price > selling_price:

                    # In a Put Option: Market Price > Selling Price is a losing trade
                    plt.axvline(x=train.index[-1], color = 'r', lw=0.5)

                    # Pay for the premium
                    total_amount = total_amount - (premium * shares)

                    # Update trade status
                    trade_status["Lose"] += 1

                else:
                    # In a Put Option: Market Price < Selling Price is a winning trade
                    plt.axvline(x=train.index[-1], color = 'g', lw=0.5)

                    # Calculate the profit
                    gross_profit = selling_price - market_price
                    net_profit = gross_profit - premium
                    trade_profit = net_profit * shares
                    total_amount = total_amount + trade_profit

                    # Update trade status
                    trade_status["Win"] += 1

    # Show the trade actions
    if verbose:

        plt.annotate(f'Buy: {trade_actions["Buy"]}', xy=(20, 370), xycoords='axes pixels', fontsize=12, ha='left', va='top')
        plt.annotate(f'Hold: {trade_actions["Hold"]}', xy=(20, 350), xycoords='axes pixels', fontsize=12, ha='left', va='top')
        plt.annotate(f'Sell: {trade_actions["Sell"]}', xy=(20, 330), xycoords='axes pixels', fontsize=12, ha='left', va='top')
        plt.annotate(f'Total Actions: {trade_actions["Total Actions"]}', xy=(20, 310), xycoords='axes pixels', fontsize=12, ha='left', va='top')

        if trade_status["Win"] == 0 and trade_status["Lose"] == 0 :
            plt.annotate(f'Win Rate: 0%', xy=(20, 270), xycoords='axes pixels', fontsize=12, ha='left', va='top')
            plt.annotate(f'Total Profit: {round(total_amount - initial_amount, 2)}$', xy=(20, 250), xycoords='axes pixels', fontsize=12, ha='left', va='top')
            plt.annotate(f'Total Amount: {round(total_amount, 2)}$', xy=(20, 230), xycoords='axes pixels', fontsize=12, ha='left', va='top')
        else:
            plt.annotate(f'Win Rate: {round((trade_status["Win"] / (trade_status["Win"] + trade_status["Lose"])) * 100, 2)}%', xy=(20, 270), xycoords='axes pixels', fontsize=12, ha='left', va='top')
            plt.annotate(f'Total Profit: {round(total_amount - initial_amount, 2)}$', xy=(20, 250), xycoords='axes pixels', fontsize=12, ha='left', va='top')
            plt.annotate(f'Total Amount: {round(total_amount, 2)}$', xy=(20, 230), xycoords='axes pixels', fontsize=12, ha='left', va='top')

    else:
        if trade_status["Win"] == 0 and trade_status["Lose"] == 0 :
            plt.annotate(f'Win Rate: 0%', xy=(20, 370), xycoords='axes pixels', fontsize=12, ha='left', va='top')
            plt.annotate(f'Total Actions: {trade_actions["Total Actions"]}', xy=(20, 350), xycoords='axes pixels', fontsize=12, ha='left', va='top')
            plt.annotate(f'Total Profit: {round(total_amount - initial_amount, 2)}$', xy=(20, 330), xycoords='axes pixels', fontsize=12, ha='left', va='top')
            plt.annotate(f'Total Amount: {round(total_amount, 2)}$', xy=(20, 310), xycoords='axes pixels', fontsize=12, ha='left', va='top')
        else:
            plt.annotate(f'Win Rate: {round((trade_status["Win"] / (trade_status["Win"] + trade_status["Lose"])) * 100, 2)}%', xy=(20, 370), xycoords='axes pixels', fontsize=12, ha='left', va='top')
            plt.annotate(f'Total Actions: {trade_actions["Total Actions"]}', xy=(20, 350), xycoords='axes pixels', fontsize=12, ha='left', va='top')
            plt.annotate(f'Total Profit: {round(total_amount - initial_amount, 2)}$', xy=(20, 330), xycoords='axes pixels', fontsize=12, ha='left', va='top')
            plt.annotate(f'Total Amount: {round(total_amount, 2)}$', xy=(20, 310), xycoords='axes pixels', fontsize=12, ha='left', va='top')

    return plt.show()
