from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
import numpy as np
import math
from scipy.signal import convolve2d

app = Flask(__name__)


def get_json_error(msg):
    return jsonify({'ok': 0, 'error': msg})


def get_json_response(board, win):
    return jsonify({'ok': 1, 'win': win, 'board': [[np.int(v) if ~np.isnan(v) else None for v in r] for r in board]})


@app.route('/docs',methods=['GET'])
def get_docs():
    return app.send_static_file('botwars.html')


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if not request.is_json:
        return get_json_error('request is not a json')

    content = request.get_json()

    # check board
    try:
        board_list = content['board']
    except KeyError:
        return get_json_error('no board in request')

    try:
        board = np.array(board_list, dtype=np.float)
    except ValueError:
        return get_json_error('invalid value in board')

    if board.shape != (8, 8):
        return get_json_error('invalid board dimensions')

    # mask blocked cells
    allowed = np.where(~np.isnan(board), True, False)

    if np.all(~allowed):
        return get_json_error('invalid board: all cells are blocked')

    # mask cells not owned by player
    owned = np.where(~np.isnan(board), board, 0) > 0

    if np.all(~owned):
        return get_json_error('invalid board: no player owned cells exist')

    # mask unreachable cells
    valid = (convolve2d(owned, np.ones((3, 3)), mode='same') > 0) & allowed

    if np.all(~valid):
        return get_json_error('invalid board: no valid cells to move to')

    # check moves
    try:
        moves_list = content['moves']
    except KeyError:
        return get_json_error('no moves in request')
    try:
        moves = np.array(moves_list, dtype=np.int)
    except ValueError:
        return get_json_error('invalid value in moves')

    if len(moves.shape) != 2 or moves.shape[1] != 5:
        return get_json_error('invalid moves dimensions')

    if np.any((moves.T[1:] < 0) | (moves.T[1:] > 7)):
        return get_json_error('invalid x or y value: outside board bounds')

    if np.any(~owned[moves.T[1], moves.T[2]]):
        return get_json_error('invalid move: x,y origin not owned by player')

    if np.any(~valid[moves.T[3], moves.T[4]]):
        return get_json_error('invalid move: x,y destination unreachable')

    if np.any(moves.T[0] < 1):
        return get_json_error('invalid move: less than 1 soldier moved')

    if np.any(moves.T[0] > board[moves.T[1], moves.T[2]]):
        return get_json_error('invalid move: more soldiers than available')

    if np.any((np.abs(moves.T[1] - moves.T[3]) > 1) | (np.abs(moves.T[2] - moves.T[4]) > 1)):
        return get_json_error('invalid move: destination farther than 1 from origin')

    # update board
    for m in moves:
        board[m[1], m[2]] -= m[0]
        board[m[3], m[4]] += m[0]

    if np.any(board[owned] < 0):
        return get_json_error('invalid moves: more soldiers moved than at origin')

    # enemy cells remaining
    if np.any(np.where(~np.isnan(board), board, 0) < 0):
        return get_json_response(board, win=0)

    # player won the game
    return get_json_response(board, win=1)


if __name__ == '__main__':
    app.run()
