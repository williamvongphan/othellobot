# Play a game of Othello in the terminal.
# Using the game_lib.py file, this code will play a game of Othello.
# The user can choose to play against a computer or another player.
import sys

import utils.game_lib as game_lib
from utils.game_lib import GameState
from utils.game_lib import InvalidMoveError
from utils.game_lib import OddColRowNumber

from ai.random_play import Random
from ai.minimax import Minimax
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
    # Start the game.
    game_state = GameState('FULL', 8, 8, 'B', 'W', '>')

    # Get arguments from the command line.
    if not len(sys.argv) == 3:
        print('Usage: python3 main.py <player1> <player2>')
        print('Players can be either "human", "random", "minimax", or "selfplay".')
        sys.exit(1)
    else:
        player1 = sys.argv[1]
        player2 = sys.argv[2]
        if (player1 not in ['human', 'random', 'minimax', 'selfplay']) or (player2 not in ['human', 'random', 'minimax', 'selfplay']):
            print('Players can be either "human", "random", "minimax", or "selfplay".')
            sys.exit(1)
        else:
            if player1 == 'human' and player2 == 'human':
                while not game_state.ending_condition_met():
                    # Clear the screen
                    print('\x1b[2J\x1b[1;1H', end='')
                    # Display the board.
                    display(game_state)
                    # Display some game information.
                    print()
                    # Print number of red disks in red
                    print('Red has \x1b[1;31m' + str(game_state.board.white_disc) + '\x1b[0m disks.')
                    print('Blue has \x1b[1;34m' + str(game_state.board.black_disc) + '\x1b[0m disks.')
                    print()
                    player_now = "Blue" if game_state.turn == game_lib.BLACK else "Red"
                    print('It is ' + player_now + '\'s turn.')
                    print()
                    # Get the user's move.
                    move = input('Enter your move: ')
                    if move == 'q':
                        break
                    elif len(move) != 2:
                        print('Invalid move.')
                        continue
                    # Try to make the move.
                    try:
                        move_char1 = move[0]
                        move_char2 = move[1]
                        # Convert the first character from a letter to a number.
                        row = int(move_char2) - 1
                        col = ord(move_char1) - ord('a')
                        print(row, col)
                        game_state.move((row, col))
                    except:
                        # Print the error message.
                        print('Invalid move. The system errored with the following message:')
                        print(sys.exc_info()[0])
                        print()
                        continue
                    # Check if the game is over.
                    if game_state.ending_condition_met():
                        break

                        # Clear the screen
                        print('\x1b[2J\x1b[1;1H', end='')
                        # Display the board.
                        display(game_state)
                        # Display some game information.
                        print()
                        # Print number of red disks in red
                        print('Red has \x1b[1;31m' + str(game_state.board.white_disc) + '\x1b[0m disks.')
                        print('Blue has \x1b[1;34m' + str(game_state.board.black_disc) + '\x1b[0m disks.')
                        print()
                        game_winner = "\x1b[1;31mRed\x1b[0m" if "WHITE" == game_state.winner else "\x1b[1;34mBlue\x1b[0m"
                        print(game_winner + ' wins!')

            elif player1 == 'human' and player2 != 'human':
                ai = None
                if player2 == 'random':
                    ai = Random(game_state)
                elif player2 == 'minimax':
                    ai = Minimax(game_state)
                elif player2 == 'selfplay':
                    ai = SelfPlay(game_state)
                    ai.load_q()

                while not game_state.ending_condition_met():
                    # Human is black (or red in our terminal view)
                    # AI is white (or blue in our terminal view)
                    # Clear the screen
                    print('\x1b[2J\x1b[1;1H', end='')
                    # Display the board.
                    display(game_state)
                    # Display some game information.
                    print()
                    # Print number of red disks in red
                    print('Red has \x1b[1;31m' + str(game_state.board.white_disc) + '\x1b[0m disks.')
                    print('Blue has \x1b[1;34m' + str(game_state.board.black_disc) + '\x1b[0m disks.')
                    # If the AI is a SelfPlay, print the number of games it has played.
                    if player2 == 'selfplay':
                        print('SelfPlay has \x1b[1;34m' + str(ai.num_games_played()) + '\x1b[0m parameters so far.')
                    print()
                    player_now = "Blue" if game_state.turn == game_lib.BLACK else "Red"
                    print('It is ' + player_now + '\'s turn.')
                    print()
                    # If it's the AI's turn, ask the AI to make a move. Since the AI is white, we'll prompt the AI for a move on white.
                    if game_state.turn == game_lib.WHITE:
                        # Move the AI.
                        move = ai.move()
                        # Try to make the move.
                        try:
                            game_state.move((move[0], move[1]))
                        except:
                            # Print the error message.
                            print('Invalid move. The system errored with the following message:')
                            print(sys.exc_info()[0])
                            print()
                            continue
                    else:
                        # Get the user's move.
                        move = input('Enter your move: ')
                        if move == 'q':
                            break
                        elif len(move) != 2:
                            print('Invalid move.')
                            continue
                        # Try to make the move.
                        try:
                            move_char1 = move[0]
                            move_char2 = move[1]
                            # Convert the first character from a letter to a number.
                            row = int(move_char2) - 1
                            col = ord(move_char1) - ord('a')
                            print(row, col)
                            game_state.move((row, col))
                        except:
                            # Print the error message.
                            print('Invalid move. The system errored with the following message:')
                            print(sys.exc_info()[0])
                            print()
                            continue
                    # Check if the game is over.
                    if game_state.ending_condition_met():
                        break

                # Clear the screen
                print('\x1b[2J\x1b[1;1H', end='')
                # Display the board.
                display(game_state)
                # Display some game information.
                print()
                # Print number of red disks in red
                print('Red has \x1b[1;31m' + str(game_state.board.white_disc) + '\x1b[0m disks.')
                print('Blue has \x1b[1;34m' + str(game_state.board.black_disc) + '\x1b[0m disks.')
                print()
                game_winner = "\x1b[1;31mRed\x1b[0m" if "WHITE" == game_state.winner else "\x1b[1;34mBlue\x1b[0m"
                print(game_winner + ' wins!')

            elif player1 != 'human' and player2 == 'human':
                ai = None
                if player1 == 'random':
                    ai = Random(game_state)
                elif player1 == 'minimax':
                    ai = Minimax(game_state)
                elif player1 == 'selfplay':
                    ai = SelfPlay(game_state)
                    ai.load_q()

                while not game_state.ending_condition_met():
                    # Human is black (or red in our terminal view)
                    # AI is white (or blue in our terminal view)
                    # Clear the screen
                    print('\x1b[2J\x1b[1;1H', end='')
                    # Display the board.
                    display(game_state)
                    # Display some game information.
                    print()
                    # Print number of red disks in red
                    print('Red has \x1b[1;31m' + str(game_state.board.white_disc) + '\x1b[0m disks.')
                    print('Blue has \x1b[1;34m' + str(game_state.board.black_disc) + '\x1b[0m disks.')
                    if player1 == 'selfplay':
                        print('SelfPlay has \x1b[1;31m' + str(ai.num_games_played()) + '\x1b[0m parameters so far.')
                    print()
                    player_now = "Blue" if game_state.turn == game_lib.BLACK else "Red"
                    print('It is ' + player_now + '\'s turn.')
                    print()
                    # If it's the AI's turn, ask the AI to make a move. Since the AI is white, we'll prompt the AI for a move on white.
                    if game_state.turn == game_lib.BLACK:
                        # Move the AI.
                        move = ai.move()
                        # Try to make the move.
                        try:
                            game_state.move((move[0], move[1]))
                        except:
                            # Print the error message.
                            print('Invalid move. The system errored with the following message:')
                            print(sys.exc_info()[0])
                            print()
                            continue
                    else:
                        # Get the user's move.
                        move = input('Enter your move: ')
                        if move == 'q':
                            break
                        elif len(move) != 2:
                            print('Invalid move.')
                            continue
                        # Try to make the move.
                        try:
                            move_char1 = move[0]
                            move_char2 = move[1]
                            # Convert the first character from a letter to a number.
                            row = int(move_char2) - 1
                            col = ord(move_char1) - ord('a')
                            print(row, col)
                            game_state.move((row, col))
                        except:
                            # Print the error message.
                            print('Invalid move. The system errored with the following message:')
                            print(sys.exc_info()[0])
                            print()
                            continue
                    # Check if the game is over.
                    if game_state.ending_condition_met():
                        break

                # Clear the screen
                print('\x1b[2J\x1b[1;1H', end='')
                # Display the board.
                display(game_state)
                # Display some game information.
                print()
                # Print number of red disks in red
                print('Red has \x1b[1;31m' + str(game_state.board.white_disc) + '\x1b[0m disks.')
                print('Blue has \x1b[1;34m' + str(game_state.board.black_disc) + '\x1b[0m disks.')
                print()
                game_winner = "\x1b[1;31mRed\x1b[0m" if "WHITE" == game_state.winner else "\x1b[1;34mBlue\x1b[0m"
                print(game_winner + ' wins!')

            elif player1 != 'human' and player2 != 'human':
                ai_1 = None
                ai_2 = None
                if player1 == 'random':
                    ai_1 = Random(game_state)
                elif player1 == 'minimax':
                    ai_1 = Minimax(game_state)
                elif player1 == 'selfplay':
                    ai_1 = SelfPlay(game_state)
                if player2 == 'random':
                    ai_2 = Random(game_state)
                elif player2 == 'minimax':
                    ai_2 = Minimax(game_state)
                elif player2 == 'selfplay':
                    ai_2 = SelfPlay(game_state)
                    ai_2.load_q()


                while not game_state.ending_condition_met():
                    # AI 1 is black, AI 2 is white
                    # Clear the screen
                    print('\x1b[2J\x1b[1;1H', end='')
                    # Display the board.
                    display(game_state)
                    # Display some game information.
                    print()
                    # Print number of red disks in red
                    print('Red has \x1b[1;31m' + str(game_state.board.white_disc) + '\x1b[0m disks.')
                    print('Blue has \x1b[1;34m' + str(game_state.board.black_disc) + '\x1b[0m disks.')
                    if player1 == 'selfplay':
                        print('SelfPlay has \x1b[1;31m' + str(ai_1.num_games_played()) + '\x1b[0m parameters so far.')
                    if player2 == 'selfplay':
                        print('SelfPlay has parameters \x1b[1;34m' + str(ai_2.num_games_played()) + '\x1b[0m so far.')
                    print()
                    player_now = "Blue" if game_state.turn == game_lib.BLACK else "Red"
                    print('It is ' + player_now + '\'s turn.')
                    print()
                    # If it's the AI's turn, ask the AI to make a move. Since the AI is white, we'll prompt the AI for a move on white.
                    if game_state.turn == game_lib.BLACK:
                        # Move the AI.
                        move = ai_1.move()
                        # Try to make the move.
                        try:
                            game_state.move((move[0], move[1]))
                        except:
                            # Print the error message.
                            print('Invalid move. The system errored with the following message:')
                            print(sys.exc_info()[0])
                            print()
                            continue
                    else:
                        # Move the AI.
                        move = ai_2.move()
                        # Try to make the move.
                        try:
                            game_state.move((move[0], move[1]))
                        except:
                            # Print the error message.
                            print('Invalid move. The system errored with the following message:')
                            print(sys.exc_info()[0])
                            print()
                            continue
                    # Check if the game is over.
                    if game_state.ending_condition_met():
                        break

                # Clear the screen
                print('\x1b[2J\x1b[1;1H', end='')
                # Display the board.
                display(game_state)
                # Display some game information.
                print()
                # Print number of red disks in red
                print('Red has \x1b[1;31m' + str(game_state.board.white_disc) + '\x1b[0m disks.')
                print('Blue has \x1b[1;34m' + str(game_state.board.black_disc) + '\x1b[0m disks.')
                print()
                game_winner = "\x1b[1;31mRed\x1b[0m" if "WHITE" == game_state.winner else "\x1b[1;34mBlue\x1b[0m"
                print(game_winner + ' wins!')