"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY for _ in range(3)] for _ in range(3)]


def player(board):
    total_moves = sum(cell is not EMPTY for row in board for cell in row)
    return X if total_moves % 2 == 0 else O


def actions(board):
    return set((r, c) for r in range(3) for c in range(3) if board[r][c] is EMPTY)


def result(board, action):
    r, c = action
    if r < 0 or r > 2 or c < 0 or c > 2:
        raise ValueError("Invalid move: out of bounds.")
    if board[r][c] is not EMPTY:
        raise ValueError("Invalid move: cell already taken.")

    new_board = copy.deepcopy(board)
    new_board[r][c] = player(board)
    return new_board


def winner(board):
    lines = []

    # Rows and columns
    for idx in range(3):
        lines.append(board[idx])  # row
        lines.append([board[0][idx], board[1][idx], board[2][idx]])  # column

    # Diagonals
    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])

    for line in lines:
        if line[0] and all(cell == line[0] for cell in line):
            return line[0]

    return None


def terminal(board):
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)


def utility(board):
    w = winner(board)
    return 1 if w == X else -1 if w == O else 0


def minimax(board):
    if terminal(board):
        return None

    current = player(board)
    best_action = None

    if current == X:
        highest = -math.inf
        for move in actions(board):
            score = min_score(result(board, move))
            if score > highest:
                highest = score
                best_action = move
    else:
        lowest = math.inf
        for move in actions(board):
            score = max_score(result(board, move))
            if score < lowest:
                lowest = score
                best_action = move

    return best_action


def max_score(board):
    if terminal(board):
        return utility(board)

    score = -math.inf
    for move in actions(board):
        score = max(score, min_score(result(board, move)))
    return score


def min_score(board):
    if terminal(board):
        return utility(board)

    score = math.inf
    for move in actions(board):
        score = min(score, max_score(result(board, move)))
    return score
