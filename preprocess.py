import csv
import os

BUCKET_SIZE = 150

SENTIMENT_WEIGHT = 0
PRICE_WEIGHT = 100

SENTIMENT_SCORE = 30

def extract_column_values(csv_file, header_name):
    values_list = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if header_name in row:
                
                value = row[header_name]
                if len(value) > 0:
                    # print(value)
                    values_list.append(float(value))
    return values_list


def bucket_values(input_list, min_val, max_val, n_buckets=BUCKET_SIZE):
    # min_value = min(input_list)
    # max_value = max(input_list)

    min_value = min_val
    max_value = max_val

    print(min_value)
    print(max_value)
    
    # Calculate the bucket size
    bucket_size = (max_value - min_value) / n_buckets
    
    # Assign each value to the appropriate bucket index
    bucket_indices = [int((value - min_value) // bucket_size) for value in input_list]
    # Ensure the last bucket includes the maximum value
    bucket_indices = [min(index, n_buckets - 1) for index in bucket_indices]
    
    return bucket_indices


def assign_unique_id(metric1, metric2, metric3):
    # Assuming metrics range from 0 to 149
    max_value = BUCKET_SIZE - 1

    # Ensure metrics are within the valid range
    metric1 = max(0, min(metric1, max_value))
    metric2 = max(0, min(metric2, max_value))
    metric3 = max(0, min(metric3, max_value))
    # Calculate unique ID as a base-BUCKET_SIZE number
    unique_id = metric1 * (max_value + 1) ** 2 + metric2 * (max_value + 1) + metric3
    return unique_id



def compute(EMA, RSI, ATR, PRICES):
    state_list = []
    next_state_list = []
    price_list = []
    next_state_price_list = []

    for i in range(len(EMA) - 1):
        cur_ema = EMA[i]
        cur_rsi = RSI[i]
        cur_atr = ATR[i]
        next_ema = EMA[i+1]
        next_rsi = RSI[i+1]
        next_atr = ATR[i+1]

        cur_state = assign_unique_id(cur_ema, cur_rsi, cur_atr)
        next_state = assign_unique_id(next_ema, next_rsi, next_atr)
        price = PRICES[i]
        next_price = PRICES[i+1]

        state_list.append(cur_state)
        next_state_list.append(next_state)
        price_list.append(price)
        next_state_price_list.append(next_price)
    return state_list, next_state_list, price_list, next_state_price_list


def generate_and_expand_csv(file_path, list1, list2, list3, list4, header1, header2, header3, header4):
    # Combine lists into a list of rows
    rows = list(zip(list1, list2, list3, list4))

    # Write to CSV file
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write headers
        csv_writer.writerow([header1, header2, header3, header4, 'a'])

        # Write data rows and expand actions
        for row in rows:
            csv_writer.writerow(list(row) + [0])
            if 'test' not in file_path:
                csv_writer.writerow(list(row) + [1])
                csv_writer.writerow(list(row) + [2])


def preprocess_prelim(input_file_path, output_file_path):
    csv_file = input_file_path

    EMA = extract_column_values(csv_file, 'EMA')
    EMA_bucketed = bucket_values(EMA, min_val=5.2522, max_val=47.5585)

    RSI = extract_column_values(csv_file, 'RSI')
    RSI_bucketed = bucket_values(RSI, min_val=13.8411, max_val=85.6669)

    ATR = extract_column_values(csv_file, 'ATR')
    ATR_bucketed = bucket_values(ATR, min_val=0.6191, max_val=3.4024)

    PRICES = extract_column_values(csv_file, 'close')  

    state_list, next_state_list, price_list, next_state_price_list = compute(EMA_bucketed, 
                                                                             RSI_bucketed, 
                                                                             ATR_bucketed, 
                                                                             PRICES)

    generate_and_expand_csv(file_path=output_file_path, 
                 list1= state_list, 
                 list2=next_state_list, 
                 list3=price_list, 
                 list4=next_state_price_list, 
                 header1='s', 
                 header2='sp', 
                 header3='ps', 
                 header4='psp')


def normalize_sentiment(original_score):
    normalized_score = (original_score / 50) - 1
    return normalized_score


# Sentiment score should be between 0 and 100
def reward_fn(price, next_price, action, sentiment_score):
    # Calculate the price change percentage
    price_change = (next_price - price) / price
    sentiment_score = normalize_sentiment(sentiment_score)
    sentiment_score *= SENTIMENT_WEIGHT
    price_weight = PRICE_WEIGHT

    # Set default reward to 0
    reward1 = 0
    reward2 = 0

    # Define multipliers for buy and sell actions
    buy_multiplier = 1
    sell_multiplier = -1

    # Calculate reward based on action and price change
    if action == 1:  # Buy
        reward1 = price_change * buy_multiplier * price_weight
        reward2 = sentiment_score * buy_multiplier
    elif action == 2:  # Sell
        reward1 = price_change * sell_multiplier * price_weight
        reward2 = sentiment_score * sell_multiplier
    elif action == 0:  # Hold
        reward1 = 0
        reward2 = 0
    return reward1 + reward2


def preprocess_final(input_file_path, output_file_path):

    # Open the input CSV file
    with open(input_file_path, 'r') as input_file:
        # Create a CSV reader
        csv_reader = csv.DictReader(input_file)

        # Get the fieldnames from the existing CSV
        fieldnames = csv_reader.fieldnames + ['r']

        # Open the output CSV file
        with open(output_file_path, 'w', newline='') as output_file:
            # Create a CSV writer with the updated fieldnames
            csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)

            # Write the header to the output CSV file
            csv_writer.writeheader()

            # Iterate through each row in the input CSV
            for row in csv_reader:
                # Call the reward function and add the result to the row
                row['r'] = reward_fn(float(row['ps']), float(row['psp']), float(row['a']), float(SENTIMENT_SCORE))

                # Write the updated row to the output CSV file
                csv_writer.writerow(row)


if __name__ == "__main__":
    preprocess_prelim(input_file_path='MACY_train.csv', output_file_path='prelim_train.csv')
    preprocess_final(input_file_path='prelim_train.csv', output_file_path="Qtrain.csv")
    # os.remove('prelim_train.csv')

    preprocess_prelim(input_file_path='MACY_test.csv', output_file_path='prelim_test.csv')
    preprocess_final(input_file_path='prelim_test.csv', output_file_path="Qtest.csv")
    # os.remove('prelim_test.csv')



