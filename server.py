# Flask server allowing users to play Othello online.
from flask import Flask, request
import flask
from flask_socketio import SocketIO
import json
import math
import random

from ai.random_play import Random
from ai.minimax import Minimax
from ai.selfplay import SelfPlay

# Initialize Flask server.
from utils.game_lib import GameState

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app)


# / route
@app.route('/')
def index():
    # Send the HTML file to the client.
    return flask.send_from_directory('templates', 'index.html')

@app.route('/socket.io/<path:path>')
def handle_socketio_file(path):
    return send_from_directory('templates', path)

game_states = {}
game_data = {}

game_ai_player_1 = {}
game_ai_player_2 = {}

# On socket connection, initialize a new game.
@sio.on('connect')
def connect():
    print('Client connected')

    game_states[request.sid] = None
    game_data[request.sid] = {
        "player_1": "human",
        "player_2": "human",
    }
    game_ai_player_1[request.sid] = None
    game_ai_player_2[request.sid] = None

@sio.on('new-game')
def game_start():
    # Initialize a new game.
    game_state = GameState('FULL', 8, 8, 'B', 'W', '>')

    # Add the game to the dictionary, with the key being the socket ID.
    game_states[request.sid] = game_state

    # Send the game state to the client.
    sio.emit('game_state', game_state.to_dict(), to=request.sid)
    if (game_data[request.sid]['player_1'] == 'random'):
        game_ai_player_1[request.sid] = Random(game_state)
    elif (game_data[request.sid]['player_1'] == 'minimax'):
        game_ai_player_1[request.sid] = Minimax(game_state)
    elif (game_data[request.sid]['player_1'] == 'selfplay'):
        game_ai_player_1[request.sid] = SelfPlay(game_state)
        game_ai_player_1[request.sid].load_q()
    if (game_data[request.sid]['player_2'] == 'random'):
        game_ai_player_2[request.sid] = Random(game_state)
    elif (game_data[request.sid]['player_2'] == 'minimax'):
        game_ai_player_2[request.sid] = Minimax(game_state)
    elif (game_data[request.sid]['player_2'] == 'selfplay'):
        game_ai_player_2[request.sid] = SelfPlay(game_state)
        game_ai_player_2[request.sid].load_q()

@sio.on('acknowledge')
def acknowledge(data):
    game_state = game_states[request.sid]
    if game_state.turn == 1 and game_data[request.sid]['player_1'] != 'human':
        move = game_ai_player_1[request.sid].move()
        game_state.move(move)
        sio.emit('game_state', game_state.to_dict(), to=request.sid)
    if game_state.turn == 2 and game_data[request.sid]['player_2'] != 'human':
        move = game_ai_player_2[request.sid].move()
        game_state.move(move)
        sio.emit('game_state', game_state.to_dict(), to=request.sid)

@sio.on('player-change')
def player_change(data):
    # Get the game state.
    game_state = game_states[request.sid]

    # Change the player. Player number can be found in data.player and the option can be found in data.option.
    if (data['player'] == 1):
        if (data['option'] == 'human'):
            # Remove the AI player from the dictionary.
            del game_ai_player_1[request.sid]
            game_data[request.sid]['player_1'] = 'human'
        elif (data['option'] == 'random'):
            # Add the AI player to the dictionary.
            game_ai_player_1[request.sid] = Random(game_state)
            game_data[request.sid]['player_1'] = 'random'
        elif (data['option'] == 'minimax'):
            # Add the AI player to the dictionary.
            game_ai_player_1[request.sid] = Minimax(game_state)
            game_data[request.sid]['player_1'] = 'minimax'
        elif (data['option'] == 'selfplay'):
            # Add the AI player to the dictionary.
            game_ai_player_1[request.sid] = SelfPlay(game_state)
            game_data[request.sid]['player_1'] = 'selfplay'
            game_ai_player_1[request.sid].load_q()
    elif (data['player'] == 2):
        if (data['option'] == 'human'):
            # Remove the AI player from the dictionary.
            del game_ai_player_2[request.sid]
            game_data[request.sid]['player_2'] = 'human'
        elif (data['option'] == 'random'):
            # Add the AI player to the dictionary.
            game_ai_player_2[request.sid] = Random(game_state)
            game_data[request.sid]['player_2'] = 'random'
        elif (data['option'] == 'minimax'):
            # Add the AI player to the dictionary.
            game_ai_player_2[request.sid] = Minimax(game_state)
            game_data[request.sid]['player_2'] = 'minimax'
        elif (data['option'] == 'selfplay'):
            # Add the AI player to the dictionary.
            game_ai_player_2[request.sid] = SelfPlay(game_state)
            game_data[request.sid]['player_2'] = 'selfplay'
            game_ai_player_2[request.sid].load_q()

    sio.emit('player-change-success', {'player': data['player'], 'option': data['option']}, to=request.sid)
    # Send the game state to the client.
    sio.emit('game_state', game_state.to_dict(), to=request.sid)


@sio.on('move-attempt')
def move_attempt(data):
    # Get the X and Y coordinates of the move.
    x = data['x']
    y = data['y']

    # Attempt to make the move.
    game_state = game_states[request.sid]

    # We need to make sure the user isn't trying to make a move during the AI's turn.
    if (game_state.turn == 1 and game_data[request.sid]['player_1'] != 'human'):
        sio.emit('error', "Please wait for the AI to make its move.", to=request.sid)
        return
    elif (game_state.turn == 2 and game_data[request.sid]['player_2'] != 'human'):
        sio.emit('error', "Please wait for the AI to make its move.", to=request.sid)
        return
    try:
        game_state.move((x, y))
        sio.emit('game_state', game_state.to_dict(), to=request.sid)
    except Exception as e:
        # there was an issue, so send the error message to the client.
        sio.emit('error', "Invalid move.", to=request.sid)

# Launch the Flask server.
if __name__ == '__main__':
    app.run(debug=True)
