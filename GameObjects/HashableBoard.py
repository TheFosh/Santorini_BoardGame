## Object representing the board of spaces in a game as a binary number ##
##########################################################################
## Author: Jake Swanson
import math
from array import ArrayType

import numpy as np

from GameObjects.Space import Space

class Hashboard:
    def __init__(self, side_cell_count):
        """ TODO: IMPLEMENT THE HASH BOARD!!! IT'S SO SLOW ON IT'S OWN.
                    Hash board is not meant to be a separate way to play.
                    It is a storage for board combinations.
                    Make the board work for the notes below."""
        self.dimensions = side_cell_count

        #### BOARD MEANING ####
        ## 1D array
        ## Every 2 numbers is one space on the board.
        ## The first is the player number.
        ## The second is the player level.

        PL_COUNT = 1 # Player digit count
        BL_COUNT = 1 # Block digit count
        self.info_digits = PL_COUNT + BL_COUNT
        C_COUNT = side_cell_count ** 2 # Cell count on board
        self.num_board = np.zeros(self.info_digits * C_COUNT)

    ###########################################
    ########### GETTERS & SETTERS #############
    ###########################################
    def get_chosen_grid_space(self, chosen_x: int, chosen_y: int) -> list[int]:
        """Given a list of cords, the corresponding Space data in the 'grid' is returned"""
        return self.get_all_data(chosen_x, chosen_y)

    def get_dimensions(self) -> int:
        return self.dimensions

    def get_array_location(self, _x: int, _y: int) -> int:
        """
        Given two integers representing cartesian coordinates, they are converted to
        coordinates in the one dimensional array.

        Args:
            _x: Horizontal coordinate
            _y: Vertical coordinate

        Returns: An integer representing a place in a one dimensional array.

        """

        return self.info_digits * (_x + _y * self.dimensions)

    def get_space_from_index(self, _ind: int) -> [int]:
        """
        Behaves as if the index is only from 1 - 25.
        An index represents a spot for ALL player info.
        """
        x: int = (_ind -1) % self.dimensions
        y: int = math.floor((_ind - 1) / self.dimensions)

        return [x,y]

    def get_data(self, _x: int, _y: int, _b: int) -> int:
        """
        Since player and build height getters are quite similar, they are combined. The "_b" parameter
        takes care of the difference between the two.

        Args:
            _x: Horizontal coordinate
            _y: Vertical coordinate
            _b: Is building or not. ONLY SHOULD BE 1 or 0. This would indicate a true or false statement.

        Returns: The integer data in the num board representing the requested info at the requested spot.

        """
        index: int = int(self.get_array_location(_x, _y)) + _b # +_b for the build/player location
        return int(self.num_board[index])

    def get_all_data(self, _x: int, _y: int) -> list[int]:
        p_index: int = self.get_array_location(_x, _y)
        return [_x, _y, self.num_board[p_index], self.num_board[p_index +1]]

    def set_data(self, _x: int, _y: int, _b: int, _d: int) -> None:
        """
        Since player and build height setters are quite similar, they are combined. The "_b" parameter
        takes care of the difference between the two. The "_d" parameter is what data you are setting.

        Args:
            _x: Horizontal coordinate.
            _y: Vertical coordinate.
            _b: Is building or not. ONLY SHOULD BE 1 or 0. This would indicate a true or false statement.
            _d: Data to be set at given location.

        Returns: None

        """
        build_index: int = self.get_array_location(_x, _y) + _b # +_b for the build/player location
        self.num_board[build_index] = _d

    def set_grid_player(self, x, y, player_num):
        self.set_data(x, y, 0, player_num)

    #=========================================#
    def is_space_on_board(self, _x: int, _y: int) -> bool:
        """
        Checks if the given integers are outside the dimensions of the 'grid'.
        """
        return (self.dimensions > _x >= 0 and
                self.dimensions > _y >= 0)

    def valid_player_select(self, given_space: Space | list[int], correct_num: int):
        """
        Given a Space, the spot is checked whether a Player figure is in that spot.
        This is done by checking the Player num of the Space.
        """
        x = given_space[0]
        y = given_space[1]
        valid_space = self.is_space_on_board(x, y)
        correct_player = False
        if valid_space:
            correct_player = self.get_data(x, y, 0) == correct_num
        return valid_space and correct_player

    def valid_for_open_space(self, _x, _y):
        """
        Given two integers representing coordinates in grid space,
        the located spot in 'num_board' is determined to be a valid spot for selecting a player's location or not.
        These conditions are determined by Santorini's rules.
        """
        return (self.is_space_on_board(_x, _y) and
                self.get_data(_x, _y, 0) == 0 and
                self.get_data(_x, _y, 1) < 4)

    def get_spaces_around(self, center_x, center_y) -> list[list[int]]:
        """
    `   Given a Space representing the starting location of a Player,
        all Integers representing spaces around that spot in the 'num_board' are returned in an Array object.
        """
        possible_locations = []

        center = int(self.get_array_location(center_x, center_y) / 2) + 1

        operations = [6,5,4,1,-1,-4,-5,-6]

        for o in operations:
            if center % 5 == 0 and (o == -4 or o == 1 or o == 6):
                continue
            elif center % 5 == 1 and (o == 4 or o == -1 or o == -6):
                continue

            if center > 20 and (o == 4 or o == 5 or o == 6):
                continue
            elif center < 6 and (o == -4 or o == -5 or o == -6):
                continue
            index_spot = center + o
            array_spot = self.get_space_from_index(index_spot)
            if self.valid_for_open_space(array_spot[0], array_spot[1]):
                possible_locations.append(array_spot)

        return possible_locations

    def move_filter(self, possible_spots: list[list[int]], starting_level: int):
        """

        """
        filtered_list = []
        for spot in possible_spots:
            height = self.get_data(spot[0],spot[1], 1)
            if self.is_too_tall(height , starting_level):
                filtered_list.append(spot)
        return filtered_list

    def is_too_tall(self, _h, center_level):
        """

        """
        selected_level = _h
        return selected_level <= center_level or center_level + 1 == selected_level

    def update_player_space(self, player: list[int], new_spot: list[int]) -> None:
        """

        """
        ox = player[0]
        oy = player[1]
        self.set_data(ox, oy,0, 0)

        nx = new_spot[0]
        ny = new_spot[1]
        pn = player[2]
        self.set_data(nx, ny, 0, pn)

    def build_on_space(self, picked_space:list[int]) -> bool:
        """
        Calls 'build_level' function at the given Space in the 'grid'.
        """
        if picked_space[3] < 4:
            x = picked_space[0]
            y = picked_space[1]
            current_level = self.get_data(x, y, 1)
            self.set_data(x, y, 1, current_level + 1)

        return picked_space[3] < 4

