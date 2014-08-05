"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

# Some useful constant
# ITER_NUM = 100	# iteration number of mc simulation

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def gen_all_permutation(outcomes, length):
    """
    Iterative function that enumerates the set of all permutation of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                if item in partial_sequence:
                    continue
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    # get all possible score
    score_board = {}
    for dice in hand:
        if dice in score_board.keys():
            score_board[dice] += 1
        else:
            score_board[dice] = 1
    
    # find the maximum score
    max_score = 0
    for item in score_board.items():
        item_score = item[0]*item[1]
        if item_score > max_score:
            max_score = item_score
    
    return max_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    # compute all results if I set free dice number to num_free_dice
    outcomes = [dice for dice in range(1, num_die_sides + 1, 1)]
    free_dice_result = list(gen_all_sequences(outcomes, num_free_dice))
    
    # compute expect value
    expect_val = 0.
    result_num = len(free_dice_result)
    for free_dice in free_dice_result:
        combine_hand = tuple(list(held_dice) + list(free_dice))
        expect_val += score(combine_hand)
    expect_val /= result_num
    return expect_val


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    idx_len = len(hand)
    idx_outcomes = [idx for idx in range(1, idx_len + 1, 1)]
    ans_idx = []
    # find all possible index of subset
    for len_i in range(idx_len):
        idx_res = list(gen_all_permutation(idx_outcomes, len_i + 1))
        ans_idx += idx_res
    
    # using index find the right element
    result_set = set([()])
    for idx_item in ans_idx:
        new_subset = []
        for idx in idx_item:
            new_subset.append(hand[idx - 1])
        new_subset.sort()
        result_set.add(tuple(new_subset))
    
    return result_set


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    hand_len = len(hand)
    max_val = .0
    max_val_tuple = []
    posb_hold = list(gen_all_holds(hand))
    print posb_hold
    for hold in posb_hold:
        num_free_dice = hand_len - len(hold)
        exp_val = expected_value(hold, num_die_sides, num_free_dice)
        #print "hold:" + str(hold)
        #print "maximum hold:" + str(max_val_tuple)
        #print "expected value:" + str(exp_val)
        #print "maximum value:" + str(max_val)
        if exp_val > max_val:
            max_val = exp_val
            max_val_tuple = list(hold)
    max_hold = (max_val, tuple(max_val_tuple))
    return max_hold


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)



