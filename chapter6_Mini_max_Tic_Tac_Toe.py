"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}
# Next player
NEXT_PLAYER = {provided.PLAYERX: provided.PLAYERO,
               provided.PLAYERO: provided.PLAYERX}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    if not(board.check_win() is None):
        return SCORES[board.check_win()], (-1, -1)
    empty_squares = board.get_empty_squares()
    max_score_step = None
    for square in empty_squares:
        new_board = board.clone()
        new_board.move(square[0], square[1], player)
        result = mm_move(new_board, NEXT_PLAYER[player])
        if max_score_step is None:
            max_score_step = result
        if result[0] * SCORES[player] == 1:
            return result[0], square
        elif (result[0] - max_score_step[0]) * SCORES[player] > 0:
            max_score_step = (result[0], square)
    return max_score_step

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
#sample_board = provided.TTTBoard(3, board=[[provided.PLAYERX, provided.PLAYERO, provided.PLAYERX],
#                                           [provided.PLAYERO, provided.PLAYERX, provided.EMPTY],
#                                           [provided.PLAYERO, provided.EMPTY, provided.EMPTY]])
#print mm_move(sample_board, provided.PLAYERO)
#print sample_board