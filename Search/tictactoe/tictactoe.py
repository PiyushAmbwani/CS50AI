"""
Tic Tac Toe Player
"""

import math
import copy

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


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x = sum(row.count(X) for row in board)
    count_o = sum(row.count(O) for row in board)
    if count_x > count_o:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    n = len(board)
    action_list = [(i, j) for i in range(n) for j in range(n) if board[i][j] == EMPTY]
    action_set = set(action_list)
    # print(action_set)
    return action_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    # print(f'Action passed in result fn is: {action}')
    i, j = action
    # print(str(i) + str(j))
    if (new_board[i][j] == EMPTY):
        new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for val in [X, O]:
        if any(row.count(val) == 3 for row in board):
            return val
        if all(board[i][i] == val for i in range(len(board))):
            return val
        if all(board[2-i][i] == val for i in range(len(board))):
            return val
        for i in range(len(board)):
            if all(board[j][i] == val for j in range(len(board))):
                return val
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    for val in ['X', 'O']:
        if any(row.count(val) == 3 for row in board):
            return True
        if all(board[i][i] == val for i in range(len(board))):
            return True
        if all(board[2-i][i] == val for i in range(len(board))):
            return True
        for i in range(len(board)):
            if all(board[j][i] == val for j in range(len(board))):
                return True
    if all(row.count(EMPTY) == 0 for row in board):
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    for val in [X, O]:
        if any(row.count(val) == 3 for row in board):
            if (val == X):
                return 1
            else:
                return -1
        if all(board[i][i] == val for i in range(len(board))):
            if (val == X):
                return 1
            else:
                return -1
        if all(board[2-i][i] == val for i in range(len(board))):
            if (val == X):
                return 1
            else:
                return -1
        for i in range(len(board)):
            if all(board[j][i] == val for j in range(len(board))):
                if (val == X):
                    return 1
                else:
                    return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def min_value(state, dep):
        # prev_dep = dep
        dep += 1
        # print(f'Min depth is {dep}')
        if terminal(state):
            # print("YES MIN terminal")
            return utility(state)
        v = math.inf
        for action in actions(state):
            # print(f'Possible action in min function: {action}')
            new_v = max_value(result(state, action), dep)
            # print(f'Board: {state}')
            # print(f'New Value : {new_v}')
            # print(f'New Value with depth for min func: {new_v-dep}')
            if new_v < v:
                v = new_v
                mov = action
        if dep == 0:
            return mov
        else:
            return v

    def max_value(state, dep):
        # prev_dep = dep
        dep += 1
        # print(f'Max depth is {dep}')
        if terminal(state):
            # print("YES MAX terminal")
            return utility(state)
        v = -math.inf
        for action in actions(state):
            # print(f'Possible action in max function: {action}')
            new_v = min_value(result(state, action), dep)
            # print(f'Board: {state}')
            # print(f'New Value : {new_v}')
            # print(f'New Value with depth for max func: {new_v+dep}')
            if new_v > v:
                v = new_v
                mov = action
        if dep == 0:
            return mov
        else:
            return v

    if player(board) == X:
        return max_value(board, -1)
    else:
        return min_value(board, -1)