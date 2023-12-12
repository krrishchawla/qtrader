import numpy as np
import pandas as pd
import time

class QLearning:
    def __init__(self, num_states, num_actions, lr, discount, max_iters):
        self.num_states = num_states
        self.num_actions = num_actions
        self.lr = lr
        self.discount = discount
        Q_size = (num_states, num_actions)
        self.Q = np.zeros(Q_size)
        self.max_iters = max_iters

    def update(self, state, action, reward, next_state):
        self.Q[state, action] += (self.lr * (reward + self.discount * np.max(self.Q[next_state, :] - self.Q[state, action])))                                   


if __name__ == '__main__':
    pass
