import numpy as np
import pandas as pd
import time
import csv

from models import QLearning

FILES = ['Qtrain.csv']

def process(model, data, csv_file):
    start_time = time.time()
    for iter in range(model.max_iters):
        print(f'iteration {iter} out of {model.max_iters}')
        for i in range(len(data)):
            state = data['s'][i]
            action = data['a'][i]
            reward = data['r'][i]
            next_state = data['sp'][i]
            model.update(state, action, reward, next_state)
    policy = np.argmax(model.Q, axis=1)
    print(np.sum(policy))
    # np.savetxt(f'{csv_file.replace(".csv", "")}policy.csv', policy, fmt='%i', delimiter=',')

    with open(csv_file.replace(".csv", "policy.csv"), mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(['a'])
        
        # Write the numbers as rows
        for number in policy:
            writer.writerow([number])
    end_time = time.time()
    time_taken = end_time - start_time
    print(f'Done for {csv_file}!')
    print(f'Time taken to run: {time_taken}')
    print()


def main():
    for csv_file in FILES:
        print(f'Running on {csv_file}')
        data = pd.read_csv(csv_file)
        model = QLearning(num_states=3375000, num_actions=3, lr=0.001, discount=0.95, max_iters=100)
        process(model, data, csv_file)


if __name__ == '__main__':
    main()
