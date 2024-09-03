import pandas as pd

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
