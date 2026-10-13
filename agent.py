import random


class QLearningAgent:
    def __init__(self):
        # Each state is a position: (x, y).
        # Each state has four possible actions.
        self.q_table = {}

        self.actions = [0, 1, 2, 3]

        # Learning settings
        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.epsilon = 1.0

    def get_q_values(self, state):
        if state not in self.q_table:
            self.q_table[state] = [0.0, 0.0, 0.0, 0.0]

        return self.q_table[state]

    def choose_action(self, state):
        # Exploration: try a random action.
        if random.random() < self.epsilon:
            return random.choice(self.actions)

        # Exploitation: choose the action with the
        # highest estimated future reward.
        q_values = self.get_q_values(state)
        best_value = max(q_values)

        best_actions = [
            action
            for action, value in enumerate(q_values)
            if value == best_value
        ]

        return random.choice(best_actions)

    def learn(self, state, action, reward, next_state, done):
        current_q = self.get_q_values(state)[action]

        if done:
            future_q = 0
        else:
            future_q = max(self.get_q_values(next_state))

        # Q-learning update rule
        new_q = current_q + self.learning_rate * (
            reward
            + self.discount_factor * future_q
            - current_q
        )

        self.q_table[state][action] = new_q

    def reduce_exploration(self):
        # Gradually stop random exploration.
        self.epsilon = max(0.02, self.epsilon * 0.995)