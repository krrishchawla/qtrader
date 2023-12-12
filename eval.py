import csv
import numpy as np
import random
import os


def extract_column_values(csv_file, header_name):
    values_list = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if header_name in row:
                value = row[header_name]
                values_list.append(float(value))
    return values_list


class Trader:
    def __init__(self, prices, bank_balance=1000, stock_position=20, value=0) -> None:
        self.bank_balance = bank_balance
        self.stock_position = stock_position
        self.value = value
        self.prices = prices

    def reset(self) -> None:
        self.bank_balance = 1000
        self.stock_position = 20
        self.old_value = 0
        self.value = 0

    def evaluate_policy(self, policy, invested=True):
        if not invested:
            self.stock_position = 0
        for i in reversed(range(len(policy))): 
            price = self.prices[i]
            action = policy[i]
            if i == len(policy) - 1:
                self.old_value = self.bank_balance + self.stock_position * price
            if action == 1: # Buy
                self.bank_balance -= price
                self.stock_position += 1
            if action == 2: # Sell
                self.bank_balance += price
                self.stock_position -= 1
            self.value = self.bank_balance + self.stock_position * price
        change = self.value - self.old_value
        percent_change = change / self.old_value * 100
        print('Old Value = ', self.old_value)
        print('New Value = ', self.value)
        print('Percent Change = ', percent_change)
        print()
        self.reset()
        return percent_change
    

def evaluate():           
    prices = extract_column_values("Qtest.csv", 'ps')
    # print(prices)

    states = extract_column_values("Qtest.csv", 's')
    states = [int(state) for state in states]
    # print(len(states))

    optimal_policy = extract_column_values('Qtrainpolicy.csv', 'a')
    optimal_policy = np.array(optimal_policy)

    optimal_policy_for_states = optimal_policy[states].astype('int')
    print('optimal action = \t', list(optimal_policy_for_states)[::-1])

    random_policy = np.array([random.randint(0, 2) for i in range(len(optimal_policy_for_states))])
    print('random policy = \t', list(random_policy))

    all_hold_policy = np.zeros(random_policy.shape).astype('int')

    print('all hold policy = \t', list(all_hold_policy))
    print()
                
    trader = Trader(prices)
    print('Optimal Policy:')
    trader.evaluate_policy(optimal_policy_for_states)
    print('Random Policy:')
    trader.evaluate_policy(random_policy)
    print('All Hold Policy with initial position:')
    trader.evaluate_policy(all_hold_policy)
    print('All Hold Policy with no position:')
    trader.evaluate_policy(all_hold_policy, invested=False)
    # os.remove("Qtrain.csv")
    # os.remove("Qtest.csv")
    # os.remove("Qtrainpolicy.csv")
        



if __name__ == "__main__":
    evaluate()






