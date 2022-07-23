import random


class Random:
    def __init__(self, game_state):
        self.game_state = game_state

    def move(self):
        # Return a random move.
        return random.choice(list(self.game_state.full_possible_moves()))