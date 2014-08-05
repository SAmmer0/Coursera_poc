"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 

   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # replace with your code
    if len(line) < 2:
        return line
    tmp_list = [0] * len(line)
    # copy elements to the temp list,
    # until empty elements only appear
    # in the end of the list
    ind = 0
    for num in line:
        if num != 0:
            tmp_list[ind] = num
            ind += 1

    # set result list
    result = []
    
    # check if the neighbor numbers
    # are the same, if it is, merge
    # them
    tmp_ind = 0
    while tmp_ind < len(line):
        if tmp_ind == (len(line) - 1):
            result.append(tmp_list[tmp_ind])
            tmp_ind += 1
        elif tmp_list[tmp_ind] != tmp_list[tmp_ind + 1]:
                result.append(tmp_list[tmp_ind])
                tmp_ind += 1
        else:
            result.append(tmp_list[tmp_ind] * 2)
            tmp_ind += 2
    while len(result) < len(line):
        result.append(0)
    
    return result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.reset()
        
        # Set indices for initial tiles
        self.grid_indices = {UP: [(0, i) for i in range(self.grid_width)],
                             DOWN: [(self.grid_height - 1, i) for i in range(self.grid_width)],
                             LEFT: [(i, 0) for i in range(self.grid_height)],
                             RIGHT: [(i, self.grid_width - 1) for i in range(self.grid_height)]}
        
        # Set length of every direction to make it convenient to
        # compute indices
        self.direction_len = {UP: self.grid_height,
                              DOWN: self.grid_height,
                              LEFT: self.grid_width,
                              RIGHT: self.grid_width}
                              
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        # replace with your code
        self.grid = []
        for dummy_i in range(self.grid_height):
            self.grid.append([])
        for fst_list in self.grid:
            for dummy_j in range(self.grid_width):
                fst_list.append(0)
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        str_grid = str(self.grid)
        return str_grid
    
    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self.grid_height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self.grid_width
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        for elem in self.grid_indices[direction]:
            # Compute indices for every row or column
            tmp_ind = [(elem[0] + i * OFFSETS[direction][0],
                        elem[1] + i * OFFSETS[direction][1])
                        for i in range(self.direction_len[direction])]
            
            # Get the value of the row or column
            tmp_line = [self.get_tile(ind[0], ind[1]) for ind in tmp_ind]
            
            # Get the merge result
            merge_result = merge(tmp_line)
            
            # Using the merge result to reset the grid
            ind_i = 0
            for ind in tmp_ind:
                self.set_tile(ind[0], ind[1], merge_result[ind_i])
                ind_i += 1
        # Add a new random tile
        self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        # randomly select an empty position
        select_list = []
        for i_height in range(self.grid_height):
            for j_width in range(self.grid_width):
                if self.grid[i_height][j_width] == 0:
                    select_list.append((i_height, j_width))
        # if there is no empty square, the game ends
        if len(select_list) == 0:
            return
        rnd_pos = random.randint(0, len(select_list) - 1)
        row = select_list[rnd_pos][0]
        col = select_list[rnd_pos][1]
        
        # randomly set a value for the tile
        rnd_seed = random.random()
        if rnd_seed >= 0.9:
            self.set_tile(row, col, 4)
        else:
            self.set_tile(row, col, 2)
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        # replace with your code
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        # replace with your code
        return self.grid[row][col]
 

if __name__ == '__main__':
    poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
