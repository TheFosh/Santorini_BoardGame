## Object representing the board of spaces in a game ##
#######################################################
## Author: Jake Swanson
from logging.config import valid_ident
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
        return self.grid[chosen_space.getY()][chosen_space.getX()] ## Y VALUE FIRST THEN X FOR

    def set_grid_player(self, chosen_space, player_num):
        self.grid[chosen_space.getX()][chosen_space.getY()].set_player(player_num)
    ########################################

    def valid_for_open_space(self, _x, _y):
        return (self.space_on_board(_x, _y) and
                self.grid[_x][_y].playerNum == 0 and
                self.grid[_x][_y].level < 4)

    def space_on_board(self, _x, _y):
        return (self.WIDTH > _x >= 0 and
                self.HEIGHT > _y >= 0)

    def valid_player_select(self, given_space, correct_num):
        """
        Returns whether a player figure is
        in the selected spot and is the correct
        number.
        """
        print(str(given_space.getX()) + ", " + str(given_space.getY()))
        valid_space = False
        correct_player = False
        if self.space_on_board(given_space.getX(), given_space.getY()):
            valid_space = self.space_on_board(given_space.getX(), given_space.getY())
            correct_player = self.grid[given_space.getX()][given_space.getY()].get_player() == correct_num
        return valid_space and correct_player

    def is_too_tall(self, spot, center_level):
        return center_level >= spot.get_level() or spot.get_level() + 1 == center_level

    def get_spaces_around(self, starting_location):
        possible_locations = []
        starting_x = starting_location.getX() + 1
        starting_y = starting_location.getY() + 1
        starting_level = starting_location.get_level()

        RANGE_AROUND_POINT = 8
        for i in range(RANGE_AROUND_POINT):
            ## Coordinates for spot changes over time to loop around the spot.
            print(str(starting_x) +", " + str(starting_y))
            if i / 2 < 1:
                starting_x -= 1
            elif i / 2 < 2:
                starting_y -= 1
            elif i / 2 < 3:
                starting_x += 1
            elif i / 2 < 4:
                starting_y += 1
            valid_spot = self.valid_for_open_space(starting_x, starting_y)

            if valid_spot:
                current_spot = self.grid[starting_y][starting_x]
                good_height = self.is_too_tall(current_spot, starting_level)
                #print(valid_spot)
                #print(too_tall)
                if good_height:
                    possible_locations.append(current_spot)

        return possible_locations
