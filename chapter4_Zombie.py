"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._human_list[:] = []
        self._zombie_list[:] = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        obstacle_list = []
        for row in range(len(self._cells)):
            for col in range(len(self._cells[row])):
                if not self.is_empty(row, col):
                    visited.set_full(row, col)
                    obstacle_list.append((row, col))
        
        distance_field = [[self._grid_height * self._grid_width for dummy_col in range(self._grid_width)]
                          for dummy_row in range(self._grid_height)]
        
        # get boundry queue
        boundry = poc_queue.Queue()
        if entity_type == ZOMBIE:
            for entity in self._zombie_list:
                boundry.enqueue(entity)
        else:
            for entity in self._human_list:
                boundry.enqueue(entity)
        
        # set visited and distance_field by boundry
        for item in boundry:
            visited.set_full(item[0], item[1])
            distance_field[item[0]][item[1]] = 0
        
        # using BFS to compute distance
        while len(boundry) > 0:
            current_cell = boundry.dequeue()
            current_neighbor = self.four_neighbors(current_cell[0], current_cell[1])     
            for neighbors in current_neighbor:
                if visited.is_empty(neighbors[0], neighbors[1]):
                    visited.set_full(neighbors[0], neighbors[1])
                    boundry.enqueue(neighbors)
                if neighbors not in obstacle_list:
                    distance_field[neighbors[0]][neighbors[1]] = min(distance_field[neighbors[0]][neighbors[1]],
                                                    distance_field[current_cell[0]][current_cell[1]] + 1)
        return distance_field   
                            
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        poss_moves = []
        new_pos_list = []
        max_dist = 0
        for human in self._human_list:
            max_dist = zombie_distance[human[0]][human[1]]
            for neighbors in self.eight_neighbors(human[0], human[1]):
                nrow, ncol = neighbors[0], neighbors[1]
                if (zombie_distance[nrow][ncol] > max_dist) and (zombie_distance[nrow][ncol] != self._grid_height * self._grid_width):
                    max_dist = zombie_distance[nrow][ncol]
                    poss_moves[:] = [neighbors]
                elif zombie_distance[nrow][ncol] == max_dist:
                    poss_moves.append(neighbors)
                else:
                    continue
            if len(poss_moves) == 0:
                new_pos = human
            else:
                new_pos = poss_moves[random.randint(0, len(poss_moves) - 1)]
            new_pos_list.append(new_pos)
        self._human_list = new_pos_list
    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        poss_moves = []
        new_pos_list = []
        min_dist = float("inf")
        for zombie in self._zombie_list:
            min_dist = human_distance[zombie[0]][zombie[1]]
            for neighbors in self.four_neighbors(zombie[0], zombie[1]):
                nrow, ncol = neighbors[0], neighbors[1]
                if (human_distance[nrow][ncol] < min_dist) and (human_distance[nrow][ncol] != self._grid_height * self._grid_width):
                    min_dist = human_distance[nrow][ncol]
                    poss_moves[:] = [neighbors]
                elif human_distance[nrow][ncol] == min_dist:
                    poss_moves.append(neighbors)
                else:
                    continue
            if len(poss_moves) == 0:
                new_pos = zombie
            else:
                new_pos = poss_moves[random.randint(0, len(poss_moves) - 1)]
            new_pos_list.append(new_pos)
        self._zombie_list = new_pos_list

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Zombie(30, 40))
