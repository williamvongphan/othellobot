import sys
import math
from collections.abc import Iterable
import copy
import numpy as np

class Minimax:
    def __init__(self, game_state):
        self.game_state = game_state

    def minimax(self, depth, maximizing_player):
        if depth == 0:
            return self.evaluation_function()
        elif maximizing_player:
            return self.max_value(self.game_state, depth)
        else:
            return self.min_value(self.game_state, depth)

    def max_value(self, game_state, depth):
        if game_state.ending_condition_met():
            return self.evaluation_function()
        v = -math.inf
        if depth == 1:
            for move in game_state.full_possible_moves():
                v = max(v, self.evaluation_function(move))
            return v
        for move in game_state.full_possible_moves():
            v = max(v, self.min_value(game_state.result(move), depth - 1))
        return v

    def min_value(self, game_state, depth):
        if game_state.ending_condition_met():
            return self.evaluation_function()
        v = math.inf
        if depth == 1:
            for move in game_state.full_possible_moves():
                v = min(v, self.evaluation_function(move))
            return v
        for move in game_state.full_possible_moves():
            v = min(v, self.max_value(game_state.result(move), depth - 1))
        return v

    def evaluation_function(self, move):
        # This function evaluates the fitness of a move.
        # It returns a value between -1 and 1.
        # The value is positive if the move is good for the player.
        # The value is negative if the move is bad for the player.
        # The value is 0 if the move is neutral.
        score = 0
        if self.game_state.ending_condition_met():
            if self.game_state.winner == self.game_state.turn:
                score = 100
            elif self.game_state.winner == self.game_state.opposite_turn_color():
                score = -100
        else:
            # The score is the number of pieces that will be flipped
            # if the move is made.
            old_piece_count_me = self.game_state.piece_count(self.game_state.turn)
            new_board = self.game_state.result(move)
            # Count the number of pieces that will be flipped.
            new_piece_count_me = new_board.piece_count(self.game_state.turn)
            # The score is the difference between the number of pieces that will be flipped.
            score = new_piece_count_me - old_piece_count_me
        return score

    def move(self):
        # This function returns the best move for the current player.
        # It is a recursive function.
        # It returns the best move for the current player.
        # It also returns the value of the best move.
        # The best move is the move that results in the highest value.
        v = -math.inf
        best_move = None
        for move in self.game_state.full_possible_moves():
            score = self.minimax(1, True)
            if score > v:
                v = score
                best_move = move
        return best_move