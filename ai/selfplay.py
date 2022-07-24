import json
import json_lines
import base64
import math
import threading

import random


def num_to_player(num):
    if num == 0:
        return 'BLACK'
    elif num == 1:
        return 'WHITE'
    else:
        return None


def tuple_to_str(tuple_):
    return str(tuple_[0]) + ',' + str(tuple_[1])


def str_to_tuple(str_):
    return tuple(map(int, str_.split(',')))


def board_string_to_number(board_string):
    # . = 0, B = 1, W = 2
    # 0 = empty, 1 = black, 2 = white
    num = 0
    for i in range(64):
        if board_string[i] == '.':
            num = num * 3
        elif board_string[i] == 'B':
            num = num * 3 + 1
        elif board_string[i] == 'W':
            num = num * 3 + 2
    return num

def number_to_b64(num):
    return base64.b64encode(str(num).encode()).decode()

def handle(el1, el2, el3):
    return str(el1) + "|" + number_to_b64(board_string_to_number(str(el2))) + "|" + ("N" if el3 is None else str(el3[0]) + str(el3[1]))


def traverse_and_replace_tuples_in_keys_with_strings(dictionary):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            traverse_and_replace_tuples_in_keys_with_strings(value)
        elif isinstance(value, tuple):
            dictionary[key] = tuple_to_str(value)
    return dictionary


def traverse_and_replace_strings_in_keys_with_tuples(dictionary):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            traverse_and_replace_strings_in_keys_with_tuples(value)
        elif isinstance(value, str):
            dictionary[key] = str_to_tuple(value)
    return dictionary


class SelfPlay:
    def __init__(self, game_state):
        self.info = {
            "rounds_trained": 0,
            "num_params": 0
        }
        self.game_state = game_state
        self.q = {}
        self.alpha = 0.5
        self.epsilon = 0.1

    def get_q_value(self, game_state, action):
        # This function returns the Q-value of a move.
        # It returns the value of the move.
        # The value is positive if the move is good for the player.
        # The value is negative if the move is bad for the player.
        # The value is 0 if the move is neutral.
        if handle(game_state.turn, game_state.board, action) in self.q:
            return self.q[handle(game_state.turn, game_state.board, action)]
        else:
            return 0

    def update_q(self, game_state, action, reward):
        # This function updates the Q-value of a move.
        # It returns the updated Q-value.
        # The updated Q-value is positive if the move is good for the player.
        # The updated Q-value is negative if the move is bad for the player.
        # The updated Q-value is 0 if the move is neutral.
        if handle(game_state.turn, game_state.board, action) not in self.q:
            self.q[handle(game_state.turn, game_state.board, action)] = 0
        self.q[handle(game_state.turn, game_state.board, action)] += self.alpha * (
                reward - self.get_q_value(game_state, action))
        if self.q[handle(game_state.turn, game_state.board, action)] != 0:
            return self.q[handle(game_state.turn, game_state.board, action)]

    def get_reward(self, old_count=None):
        score = 0
        if self.game_state.ending_condition_met():
            if self.game_state.winner == self.game_state.turn:
                score = 100
            elif self.game_state.winner == self.game_state.opposite_turn_color():
                score = -100
            else:
                score = 0
        else:
            # The score is the number of pieces that will be flipped
            # if the move is made.
            # Count the number of pieces that will be flipped.
            new_piece_count_me = self.game_state.piece_count(self.game_state.turn)
            # The score is the difference between the number of pieces that will be flipped.
            score = new_piece_count_me - old_count
        return score

    def load_q(self, file_path='q.json'):
        # This function loads the Q-values from a file.
        # It returns the dictionary.
        with open(file_path, 'r') as f:
            self.q = json.load(f)
        with open("info.json", 'r') as f:
            self.info = json.load(f)
        return self.q

    def save_q(self, file_path='q.json'):
        # This function saves the Q-values to a file. But before we do that, we must first convert all tuples to strings.
        # It returns the dictionary.
        with open(file_path, 'w') as f:
            json.dump(self.q, f)
        with open("info.json", 'w') as f:
            json.dump(self.info, f)
        return self.q

    def move(self, epsilon=True):
        # We need to make sure that when we make a move, it gets saved to the Q-values.
        available_actions = self.game_state.full_possible_moves()
        if epsilon and random.random() <= self.epsilon:
            return random.sample(available_actions, 1)[0]
        best_reward = -math.inf
        for available_action in available_actions:
            if self.get_q_value(self.game_state, available_action) > best_reward:
                best_reward = self.get_q_value(self.game_state, available_action)
                best_action = available_action
        if best_reward == -math.inf:
            return random.sample(available_actions, 1)[0]
        return best_action

    def train(self, num_games=1000):
        # This function trains the AI.
        # It returns the dictionary.
        for i in range(num_games):

            last = {
                1: {"state": None, "action": None},
                2: {"state": None, "action": None}
            }

            while not self.game_state.ending_condition_met():
                old_count = self.game_state.piece_count(self.game_state.turn)
                action = self.move(True)
                self.game_state.move(action)

                # Keep track of last state and action
                last[self.game_state.turn]["state"] = self.game_state
                last[self.game_state.turn]["action"] = action

                # When game is over, update Q values with rewards
                if self.game_state.ending_condition_met():
                    reward = self.get_reward()
                    self.update_q(self.game_state, action, reward)
                    break

                # If game is continuing, no rewards yet
                else:
                    reward = self.get_reward(old_count)
                    self.update_q(self.game_state, action, reward)

            self.update_q(self.game_state, None, self.get_reward(self.game_state))
            print("Game " + str(i) + " over.")
            self.info["rounds_trained"] += 1
            self.info["num_params"] = len(self.q)
            if i % 5 == 0:
                self.save_q()
            self.game_state.reset()

    def num_params(self):
        # Reload the Q-values from the file.
        self.load_q()
        # Count the number of Q-values
        return self.info["num_params"]

    def num_games_trained(self):
        # Reload the Q-values from the file.
        self.load_q()
        # Count the number of games trained
        return self.info["rounds_trained"]
