"""
Tic Tac Toe Player
"""

import math
import copy
from itertools import chain


X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

# TODO
def player(board):
    """
    Returns player who has the next turn on a board.
    """
    flat_board = list(chain.from_iterable(board))

    x = flat_board.count(X)
    o = flat_board.count(O)

    if x == o:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    actions = []
    for rows in range(3):
        for cols in range(3):
            if board[rows][cols] is EMPTY:
                actions.append( (rows, cols) )

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if action is None:
        raise Exception("error")
    else:
        copied_board = copy.deepcopy(board)
        playerTurn = player(copied_board)
        copied_board[action[0]][action[1]] = playerTurn
        return copied_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check if X or O using utility(board)
    win_var = utility(board)
    if win_var == 1:
        return X
    elif win_var == -1:
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if not actions(board):
        return True

    for i in range(3):
        # check conditions on board
        condition1 = (board[i][0] == board[i][1] == board[i][2] != EMPTY)
        condition2 = (board[0][i] == board[1][i] == board[2][i] != EMPTY)
        if condition1 or condition2:
            return True
    diagonals1 = (board[0][0] == board[1][1] == board[2][2] != EMPTY)
    diagonals2 = (board[0][2] == board[1][1] == board[2][0] != EMPTY)
    if diagonals1 or diagonals2:
        return True

    # if none of them are returning True then game is not over!
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if not terminal(board):
        raise Exception("Has to be a terminal board")

    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            if board[i][0] == X:
                return 1
            else:
                return -1

        elif board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            if board[0][i] == X:
                return 1
            else:
                return -1

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        if board[0][0] == X:
            return 1
        else:
            return -1

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        if board[0][2] == X:
            return 1
        else:
            return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # NOTE: I fixed the code for minimax on the ed forum https://us.edstem.org/courses/241/discussion/37176 and hence modified used it in my code but built off of the logic

    # if the game has ended return none
    if terminal(board):
        return None

    # otherwise apply minimax algorithm as shown in class
    if player(board) == X:
        best_o_move = -1
        best_move = None
        for action in actions(board):
            value = min_value(result(board, action))
            if value > best_o_move:
                best_o_move = value
                best_move = action

        return best_move
    else:
        best_x_move = 1
        best_move = None
        for action in actions(board):
            value = max_value(result(board, action))
            if value < best_x_move:
                best_x_move = value
                best_move = action
        return best_move


def max_value(board):
    if terminal(board):
        return utility(board)

    v = -math.inf

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v


def min_value(board):
    if terminal(board):
        return utility(board)

    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
