import utils.game_lib as game_lib
# Play a game of Othello in the terminal.
# Using the game_lib.py file, this code will play a game of Othello.
# The user can choose to play against a computer or another player.
import sys

import utils.game_lib as game_lib
from utils.game_lib import GameState
from utils.game_lib import InvalidMoveError
from utils.game_lib import OddColRowNumber

from ai.selfplay import SelfPlay
def display(game):
    game_board = game.board.board
    # First, print the letters of the grid.
    print('  a b c d e f g h')
    # Now print each row.
    for row in range(len(game_board)):
        # Print the row number.
        print(str(row + 1) + ' ', end='')
        # Print each piece in the row.
        for piece in game_board[row]:
            if piece.color == game_lib.BLACK:
                # Print an O in blue.
                print('\x1b[1;34mO\x1b[0m', end=' ')
            elif piece.color == game_lib.WHITE:
                # Print an O in red.
                print('\x1b[1;31mO\x1b[0m', end=' ')
            elif piece.location in game_state.full_possible_moves():
                # Print a blank space in green.
                print('\x1b[1;32m*\x1b[0m', end=' ')
            else:
                # Print a blank space in white.
                print('-', end=' ')
        print()


if __name__ == '__main__':
    # Play 10000 games of Othello against itself.
    game_state = GameState('FULL', 8, 8, 'B', 'W', '>')
    self_play = SelfPlay(game_state)
    self_play.train(100)
