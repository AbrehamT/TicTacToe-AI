"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None

no_winner = False
v_max = -100000000
v_min = 100000000
v_min_here = 100000000
v_max_here = -100000000
min_max_value = -69
coord = None

winning_combo = {
    (0, 0): {
        "combo_1": [(0, 1), (0, 2)],
        "combo_2": [(1, 0), (2, 0)],
        "combo_3": [(1, 1), (2, 2)],
        "combo_4": [EMPTY, EMPTY]
    },
    (0, 1): {
        "combo_1": [(0, 0), (0, 2)],
        "combo_2": [(1, 1), (2, 1)],
        "combo_3": [EMPTY, EMPTY],  # No diagonal wins possible from this cell
        "combo_4": [EMPTY, EMPTY]
    },
    (0, 2): {
        "combo_1": [(0, 0), (0, 1)],
        "combo_2": [(1, 2), (2, 2)],
        "combo_3": [(1, 1), (2, 0)],
        "combo_4": [EMPTY, EMPTY]
    },
    (1, 0): {
        "combo_1": [(1, 1), (1, 2)],
        "combo_2": [(0, 0), (2, 0)],
        "combo_3": [EMPTY, EMPTY],
        "combo_4": [EMPTY, EMPTY]  # No diagonal wins possible from this cell
    },
    (1, 1): {
        "combo_1": [(1, 0), (1, 2)],
        "combo_2": [(0, 1), (2, 1)],
        "combo_3": [(0, 0), (2, 2)],  # Diagonal down to the right
        "combo_4": [(0, 2), (2, 0)]   # Diagonal up to the right
    },
    (1, 2): {
        "combo_1": [(1, 0), (1, 1)],
        "combo_2": [(0, 2), (2, 2)],
        "combo_3": [EMPTY, EMPTY],
        "combo_4": [EMPTY, EMPTY]  # No diagonal wins possible from this cell
    },
    (2, 0): {
        "combo_1": [(2, 1), (2, 2)],
        "combo_2": [(0, 0), (1, 0)],
        "combo_3": [(1, 1), (0, 2)],
        "combo_4": [EMPTY, EMPTY]
    },
    (2, 1): {
        "combo_1": [(2, 0), (2, 2)],
        "combo_2": [(0, 1), (1, 1)],
        "combo_3": [EMPTY, EMPTY],
        "combo_4": [EMPTY, EMPTY]  # No diagonal wins possible from this cell
    },
    (2, 2): {
        "combo_1": [(2, 0), (2, 1)],
        "combo_2": [(0, 2), (1, 2)],
        "combo_3": [(0, 0), (1, 1)],
        "combo_4": [EMPTY, EMPTY]
    }
}

def initial_state():
    """
    Returns starting state of the board.
    """
    #return [[X, O, X],
    #        [EMPTY, EMPTY, EMPTY],
    #        [EMPTY, EMPTY, EMPTY]]
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_counter = 0
    o_counter = 0
    empty_count = 0
    
    for i in range(3):
        for j in range (3):
            if board[i][j] == EMPTY:
                empty_count += 1
            if board[i][j] == X:
                x_counter += 1
            if board[i][j] == O:
                o_counter += 1
    
    if o_counter < x_counter:
        return O
    
    return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range (3):
            if board[i][j] == EMPTY: 
                possible_actions.add((i, j))
    
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = [row[:] for row in board]
    new_board[action[0]][action[1]] = player(board)

    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        for j in range(3):
            for l in range(4):
                row = winning_combo [ (i,j) ]["combo_{x}".format(x=l+1)]
                col = winning_combo[(i,j)][ "combo_{x}".format(x=l+1)]
                if row[0] == None:
                    continue
                row = row[0][0]
                col = col[0][1]
                if board[i][j] == board[row][col] and board[i][j] != EMPTY:
                    row = winning_combo [ (i,j) ]["combo_{x}".format(x=l+1)]
                    row = row[1][0]
                    col = winning_combo[(i,j)][ "combo_{x}".format(x=l+1)]
                    col = col[1][1]
                    if board[i][j] == board[row][col]:
                        #RETURN WINNER
                        if board[i][j] == 'X':
                            return X
                        return O
    
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #if winner(board) == None:
    #    no_winner = True
        
        
    return True if len(actions(board)) == 0 or winner(board) != None else False
    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    """
    find all the Xs and keep record of their position
    Look for a winning combination in this record
    """
    #flag = false means that no winner was found
    winner_is = winner(board)
    if winner_is == None:
        return 0
    
    return 1 if winner_is == X else -1
        

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    v_min_here = 100000000
    v_max_here = -100000000
    global v_max
    global v_min
    v_max = -100000000
    v_min = 100000000
    
    optimal_action = (0,0)
    
    if(terminal(board)):
        print("WE IMN EHERE")
        min_max_val = utility(board)
        return coord
    
    player_is = player(board)
    # print("PLAYER IS: {x}".format(x=player_is) )
    actions_list = actions(board)
    if len(actions_list) == 9:
        return optimal_action
    if X == player_is:
        for action in actions_list:
            resulting1 = min_value(result(board, action))
            if v_max_here < resulting1:
                optimal_action = action
                v_max_here = resulting1          


    else:
        for action in actions_list:
            resulting = max_value(result(board, action))
            if v_min_here > resulting:                
                optimal_action = action
                v_min_here = resulting 

    return optimal_action

def max_value(board):
    v_max = -100000000
    
    if(terminal(board)):
        return utility(board)
    
    for action in actions(board):
        v_max = max(v_max, min_value(result(board, action)))
    
    return v_max
        
def min_value(board):
    v_min = 100000000
    
    if(terminal(board)):
        return utility(board)
    
    for action in actions(board):
        v_min = min(v_min, max_value(result(board, action)))
    
    return v_min