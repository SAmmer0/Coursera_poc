"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 200    # Number of trials to run
MCMATCH = 3.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
INF = 10000000000000	# Define a number as infinite
    
# Add your functions here.
def mc_trial(board, player):
    '''
    This function will use mc simulation to randomly play a
    game.
    '''
    def change_player(last_player):
        '''
        this function is used to change alternative player in
        turn
        '''
        this_player = None
        if last_player == None:
            this_player = player
        elif last_player == provided.PLAYERX:
            this_player = provided.PLAYERO
        else:
            this_player = provided.PLAYERX
        return this_player
    
    player_last = None	# recording the player of last turn
    player_this = None	# recording the player of this turn
    
    # main loop to simulate a game
    while board.check_win() == None:
        empty_squares = board.get_empty_squares()
        rand_square = random.randint(0, len(empty_squares) - 1)
        this_move = empty_squares[rand_square]
        player_this = change_player(player_last)
        player_last = player_this
        board.move(this_move[0], this_move[1], player_this)

def mc_update_scores(scores, board, player):
    '''
    This function is used to update the scores of the grid.
    '''
    def score(board, winner, player, row, col):
        '''
        score a specific square.
        '''
        score_square = .0
        if winner == provided.DRAW:
            pass
        elif board.square(row, col) == provided.EMPTY:
            pass
        elif winner == player:
            if winner == board.square(row, col):
                score_square = MCMATCH
            else:
                score_square = -MCOTHER
        else:
            if winner == board.square(row, col):
                score_square = MCOTHER
            else:
                score_square = -MCMATCH
        return score_square
    
    # main loop to update score
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            scores[row][col] += score(board, board.check_win(),
                                      player, row, col)

def get_best_move(board, scores):
    '''
    This function will get the scores of the grid, and return
    the positon of the maximum scores.
    '''
    empty_squares = board.get_empty_squares()
    if len(empty_squares) == 0:
        return None
    max_score = -INF
    idx = []
    for num in range(len(empty_squares)):
        row = empty_squares[num][0]
        col = empty_squares[num][1]
        if scores[row][col] > max_score:
            max_score = scores[row][col]
            idx[:] = []
            idx.append((row, col))
        elif scores[row][col] == max_score:
            idx.append((row, col))
        else:
            pass
    print idx
    rand_idx = random.randint(0, len(idx) - 1)
    return idx[rand_idx]

def mc_move(board, player, trials):
    '''
    This function will return the best move after mc
    simulation.
    '''
    board_copy = board.clone()
    socres = [[0 for dummy_i in range(board.get_dim())]
              for dummy_j in range(board.get_dim())]
    
    for dummy_i in range(trials):
        mc_trial(board_copy, player)
        mc_update_scores(socres, board_copy, player)
    
    return get_best_move(board, socres)


# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
