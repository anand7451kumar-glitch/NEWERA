import json
import random


class QLearningAgent:
    def __init__(self):
        # Stores what the AI has learned.
        # Each state has four Q-values: up, down, left, right.
        self.q_table = {}

        self.actions = [0, 1, 2, 3]

        # Learning parameters
        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.epsilon = 1.0

    def get_q_values(self, state):
        """Return the Q-values for a state."""
        if state not in self.q_table:
            self.q_table[state] = [0.0, 0.0, 0.0, 0.0]

        return self.q_table[state]

    def choose_action(self, state):
        """Choose an action using epsilon-greedy exploration."""

        # Exploration: try a random action.
        if random.random() < self.epsilon:
            return random.choice(self.actions)

        # Exploitation: choose an action with the best Q-value.
        q_values = self.get_q_values(state)
        best_value = max(q_values)

        # Randomly break ties between equally good actions.
        best_actions = [
            action
            for action, value in enumerate(q_values)
            if value == best_value
        ]

        return random.choice(best_actions)

    def learn(self, state, action, reward, next_state, done):
        """Update the Q-table using the Q-learning algorithm."""

        current_q = self.get_q_values(state)[action]

        if done:
            future_q = 0.0
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
        """Gradually reduce random actions as the AI learns."""
        self.epsilon = max(0.02, self.epsilon * 0.995)

    def save(self, filename="neuro_model.json"):
        """Save the learned Q-table to a JSON file."""

        data = {
            f"{x},{y}": values
            for (x, y), values in self.q_table.items()
        }

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

        print(f"AI model saved to {filename}")

    def load(self, filename="neuro_model.json"):
        """Load a previously saved Q-table."""

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.q_table = {
            tuple(map(int, state.split(","))): values
            for state, values in data.items()
        }

        print(f"AI model loaded from {filename}")