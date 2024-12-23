## Object representing the board of spaces in a game ##
#######################################################
## Author: Jake Swanson
from math import floor
from GameObjects.Space import Space

class Board:
    def __init__(self, screen_w, screen_h, cell_count):
        self.WIDTH = cell_count
        self.HEIGHT = cell_count
        self.grid = [
                        [Space(i, j) for i in range(self.WIDTH)]
                        for j in range(self.HEIGHT)
                    ]

    ########################################
    ########### GETTERS & SETTERS ##########
    def get_width_height(self):
        return self.WIDTH

    def get_chosen_grid_space(self, chosen_space):
        """Given a point, the corresponding grid space is returned"""
        return self.grid[chosen_space.getX()][chosen_space.getY()]

    def set_grid_player(self, chosen_space, player_num):
        self.grid[chosen_space.getX()][chosen_space.getY()].set_player(player_num)
    ########################################

    def valid_for_player_start(self, _x, _y):
        print(_x)
        print(_y)
        return (self.space_on_board(_x, _y) and
                self.grid[_x][_y].playerNum == 0)

    def space_on_board(self, _x, _y):
        return (self.WIDTH > _x >= 0 and
                self.HEIGHT > _y >= 0)

    def valid_player_select(self, given_space, correct_num):
        """
        Returns whether a player figure is
        in the selected spot and is the correct
        number.
        """
        valid_space = self.space_on_board(given_space.getX(), given_space.getY())
        correct_player = self.grid[given_space.getX()][given_space.getY()].get_player() == correct_num
        return valid_space and correct_player