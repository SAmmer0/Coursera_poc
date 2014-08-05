"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # replace with your code
        position0 = self.current_position(0, 0)
        if position0 != (target_row, target_col):
            return False
        for row in range(target_row + 1, self._height):
            for col in range(self._width):
                cur_row, cur_col = self.current_position(row, col)
                if not((cur_row, cur_col) == (row, col)):
                    return False
        for col in range(target_col + 1, self._width):
            cur_row, cur_col = self.current_position(target_row, col)
            if not((cur_row, cur_col) == (target_row, col)):
                return False
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # replace with your code
        # row move section
        ans = ''
        cur_row, cur_col = self.current_position(target_row, target_col)
        cur0_row, cur0_col = self.current_position(0, 0)
        # reach the row where the target lies in
        for dummy_col in range(cur0_row, cur_row, -1):
            ans += 'u'
        
        # inline row move   
        row_option_move = ()
        modify_move = ''
        if cur_row == 0:
            row_option_move = ('drrul', 'dllur')
            modify_move = 'dllu'
        else:
            row_option_move = ('urrdl', 'ulldr')
            modify_move = 'ulld'
        
        if cur_col < cur0_col:
            for dummy_row in range(cur0_col, cur_col, -1):
                ans += 'l'
            cur_col += 1
            while cur_col < cur0_col:
                ans += row_option_move[0]
                cur_col += 1
            
        elif cur_col == cur0_col:
            ans += 'ld'
            cur_row += 1
        else:
            for dummy__row in range(cur0_col, cur_col , 1):
                ans += 'r'
            cur_col -= 1
            while cur_col > cur0_col:
                ans += row_option_move[1]
                cur_col -= 1
            ans += modify_move

        # column move section
        while cur_row < cur0_row:
            ans += 'druld'
            cur_row += 1
        
        # update puzzle
        for move in ans:
            self.update_puzzle(move)
        
        return ans

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        ans = 'ur'
        for move in ans:
            self.update_puzzle(move)
        if (target_row, 0) == self.current_position(target_row, 0):
            row_move = 'r'*(self._width - 2)
            ans += row_move
            for move in row_move:
                self.update_puzzle(move)
            return ans
        
        interior_move = self.solve_interior_tile(target_row, 0)
        ans += interior_move
        
        final_move = 'ruldrdlurdluurddlur'
        for move in final_move:
            self.update_puzzle(move)
        ans += final_move
        
        col_move = ''
        dummy_zero_row, zero_col = self.current_position(0, 0)
        while zero_col < self._width - 1:
            col_move += 'r'
            zero_col += 1
        for move in col_move:
            self.update_puzzle(move)
        ans += col_move
        return ans

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        position0 = self.current_position(0, 0)
        if position0 != (0, target_col):
            return False
        for col in range(target_col + 1, self._width):
            if (((0, col) != self.current_position(0, col))
                or ((1, col) != self.current_position(1, col))):
                return False
        if (1, target_col) != self.current_position(1, target_col):
            return False
        for row in range(2, self._height):
            for col in range(0, self._width):
                if (row, col) != self.current_position(row, col):
                    return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        position0 = self.current_position(0, 0)
        if position0 != (1, target_col):
            return False
        for col in range(target_col + 1, self._width):
            if (((0, col) != self.current_position(0, col))
                or ((1, col) != self.current_position(1, col))):
                return False
        for row in range(2, self._height):
            for col in range(0, self._width):
                if (row, col) != self.current_position(row, col):
                    return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        ans = ''
        ans += 'ld'
        for move in ans:
            self.update_puzzle(move)
        if (0, target_col) == self.current_position(0, target_col):
            return ans
        row_move = ''
        cur_row, cur_col = self.current_position(0, target_col)
        cur0_row, cur0_col = self.current_position(0, 0)
        
        for dummy_col in range(cur0_col, cur_col, -1):
            row_move += 'l'
        
        if cur0_row != cur_row:
            row_move += 'u'
        else:
            row_move += 'ur'
            cur_col += 1
        
        while cur_col < cur0_col:
            row_move += 'rdlur'
            cur_col += 1
        row_move += 'ld'
        
        row_move += 'urdlurrdluldrruld'
        ans += row_move
        for move in row_move:
            self.update_puzzle(move)
        return ans

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        cur_row, cur_col = self.current_position(1, target_col)
        cur0_row, cur0_col = self.current_position(0, 0)
        ans = ''
        for dummy_col in range(cur0_col, cur_col, -1):
            ans += 'l'
        if cur_row  == cur0_row:
            cur_col += 1
            ans += 'ur'
        
        if cur_row != cur0_row:
            ans += 'u'
        
        while cur_col < cur0_col:
            ans += 'rdlur'
            cur_col += 1
        # update puzzle
        for move in ans:
            self.update_puzzle(move)
        
        return ans

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        ans = 'lu'
        for move in ans:
            self.update_puzzle(move)
        iter_move = ''
        while not self.row0_invariant(0):
            move_this = 'drul'
            iter_move += move_this
            for move in move_this:
                self.update_puzzle(move)
        ans += iter_move
        return ans

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        ans = ''
        row0, col0 = self.current_position(0, 0)
        # move zero to the bottom-right
        for row in range(row0, self._height - 1):
            ans += 'd'
        for col in range(col0, self._width - 1):
            ans += 'r'
        for move in ans:
            self.update_puzzle(move)
        print self
        # solve_lower_row_tile
        for row in range(self._height - 1, 1, -1):
            for col in range(self._width - 1, -1, -1):
                assert self.lower_row_invariant(row, col)
                if col != 0:
                    ans += self.solve_interior_tile(row, col)
                    assert self.lower_row_invariant(row, col - 1), 'solve_interior_tile error!'
                else:
                    ans += self.solve_col0_tile(row)
                    assert self.lower_row_invariant(row - 1, self._width - 1), 'solve_col0_tile error!'
        
        # solve top 2 rows tile
        for col in range(self._width - 1, 1, -1):
            for row in range(1, -1, -1):
                if row == 1:
                    assert self.row1_invariant(col), 'solve_row0_tile error!'
                    ans += self.solve_row1_tile(col)
                    
                else:
                    assert self.row0_invariant(col), 'solve_row1_tile error!'
                    ans += self.solve_row0_tile(col)
                    print self
        ans += self.solve_2x2()
        
        return ans

# Start interactive simulation
# poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
# main function, simple test
