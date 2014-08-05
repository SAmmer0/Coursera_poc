"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    result_list = []
    for element in list1:
        if element in result_list:
            continue
        else:
            result_list.append(element)
    return result_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    result_list = []
    for element in list1:
        if element in list2:
            result_list.append(element)
    return result_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """
    merge_result = []
    i_list1 = 0
    j_list2 = 0
    while True:
        if (i_list1 < len(list1)) and (j_list2 < len(list2)):
            if list1[i_list1] <= list2[j_list2]:
                merge_result.append(list1[i_list1])
                i_list1 += 1
            else:
                merge_result.append(list2[j_list2])
                j_list2 += 1
            
        if i_list1 == len(list1):
            merge_result += list2[j_list2:]
            break
        elif j_list2 == len(list2):
            merge_result += list1[i_list1:]
            break
    
    return merge_result
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) < 2:
        return list1
    mid_idx = len(list1) / 2
    left = list1[:mid_idx]
    right = list1[mid_idx:]
    left_sorted = merge_sort(left)
    right_sorted = merge_sort(right)
    result = merge(left_sorted, right_sorted)
    return result

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    def insert_string(ini_str, insert_str):
        '''
        this function is used to insert one word to another word
        '''
        result_str = []
        if len(ini_str) < 1:
            result_str.append(insert_str)
            return result_str
        for idx in range(len(ini_str) + 1):
            temp_word = ini_str[:idx] + insert_str + ini_str[idx:]
            result_str.append(temp_word)
        return result_str
    
    result_list = []
    if len(word) == 1:
        result_list.append(word)
        return result_list + ['']
    elif len(word) == 0:
        result_list.append(word)
        return result_list
    first = word[0]
    rest = word[1:]
    rest_strings = gen_all_strings(rest)
    result_list += rest_strings
    for rest_string in rest_strings:
        result_list += insert_string(rest_string, first)
    
    return result_list

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    return []

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()

