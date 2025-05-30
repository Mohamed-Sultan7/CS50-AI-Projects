from random import choice, random


class NimAI:
    def __init__(self, alpha=0.5, epsilon=0.1):
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def get_q_value(self, state, action):
        key = (tuple(state), action)
        return self.q.get(key, 0)

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        new_value_estimate = reward + future_rewards
        new_q = old_q + self.alpha * (new_value_estimate - old_q)
        self.q[(tuple(state), action)] = new_q

    def best_future_reward(self, state):
        best = 0
        for action in self.available_actions(state):
            q = self.get_q_value(state, action)
            if q > best:
                best = q
        return best

    def choose_action(self, state, epsilon=True):
        actions = list(self.available_actions(state))
        if not actions:
            return None

        if epsilon and random() < self.epsilon:
            return choice(actions)

        best_value = float("-inf")
        best_actions = []

        for action in actions:
            q = self.get_q_value(state, action)
            if q > best_value:
                best_value = q
                best_actions = [action]
            elif q == best_value:
                best_actions.append(action)

        return choice(best_actions)

    def available_actions(self, state):
        actions = set()
        for i, pile in enumerate(state):
            for j in range(1, pile + 1):
                actions.add((i, j))
        return actions
