# Tic Tac Toe Player

import math

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
    # Count the number of X and O on the board
    x_count = 0
    o_count = 0
    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1
    # If the counts are equal, it is X's turn
    if x_count == o_count:
        return X
    # Otherwise, it is O's turn
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Initialize an empty set of actions
    actions = set()
    # Loop through each cell of the board
    for i in range(3):
        for j in range(3):
            # If the cell is empty, add it to the set of actions
            if board[i][j] == EMPTY:
                actions.add((i, j))
    # Return the set of actions
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Check if the action is valid
    if action not in actions(board):
        raise ValueError("Invalid action")
    # Get the current player
    p = player(board)
    # Copy the board
    new_board = [row[:] for row in board]
    # Make the move on the copied board
    i, j = action
    new_board[i][j] = p
    # Return the copied board
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check each row, column and diagonal for a winner
    for i in range(3):
        # Check row i
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        # Check column i
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    # Check the main diagonal
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    # Check the anti-diagonal
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    # No winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If there is a winner, the game is over
    if winner(board) is not None:
        return True
    # If there are no empty cells, the game is over
    if EMPTY not in board[0] + board[1] + board[2]:
        return True
    # Otherwise, the game is not over
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Get the winner
    w = winner(board)
    # If X has won, return 1
    if w == X:
        return 1
    # If O has won, return -1
    elif w == O:
        return -1
    # If no one has won, return 0
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If the board is terminal, return None
    if terminal(board):
        return None
    # Get the current player
    p = player(board)
    # Initialize the best action and value
    best_action = None
    if p == X:
        # X wants to maximize the value
        best_value = -math.inf
    else:
        # O wants to minimize the value
        best_value = math.inf
    # Loop through each possible action
    for action in actions(board):
        # Get the value of the action by calling minimax recursively
        value = minimax_value(result(board, action), p)
        # Update the best action and value
        if p == X:
            # X chooses the action with the highest value
            if value > best_value:
                best_value = value
                best_action = action
        else:
            # O chooses the action with the lowest value
            if value < best_value:
                best_value = value
                best_action = action
    # Return the best action
    return best_action


def minimax_value(board, p):
    """
    Returns the value of the board for the player p.
    """
    # If the board is terminal, return the utility
    if terminal(board):
        return utility(board)
    # Initialize the value
    if p == X:
        # X wants to maximize the value
        value = -math.inf
    else:
        # O wants to minimize the value
        value = math.inf
    # Loop through each possible action
    for action in actions(board):
        # Get the value of the action by calling minimax_value recursively
        new_value = minimax_value(result(board, action), not p)
        # Update the value
        if p == X:
            # X chooses the maximum value
            value = max(value, new_value)
        else:
            # O chooses the minimum value
            value = min(value, new_value)
    # Return the value
    return value
