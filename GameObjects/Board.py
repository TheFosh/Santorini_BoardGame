## Object representing the board of spaces in a game ##
#######################################################
## Author: Jake Swanson

from GameObjects.Space import Space

class Board:

    def __init__(self, cell_count):
        self.WIDTH = cell_count             # Int. Width (horizontal) of the board grid.
        self.HEIGHT = cell_count            # Int. Height (Vertical) of the board grid.

        self.grid = [                       # Space 2D Array. Represents an actual board of Santorini.
                                            # Holds all information for Space objects.
                        [Space(j, i) for i in range(self.WIDTH)]
                        for j in range(self.HEIGHT)
                    ]

    ########################################
    ########### GETTERS & SETTERS ##########
    def get_width_height(self):
        return self.WIDTH

    def get_chosen_grid_space(self, chosen_space: Space):
        """Given a Space, the corresponding Space data in the 'grid' is returned"""
        return self.grid[chosen_space.getX()][chosen_space.getY()]

    def set_grid_player(self, chosen_space, player_num):
        """Sets the given Space in the 'grid' to be the given 'player_num'."""
        self.grid[chosen_space.getX()][chosen_space.getY()].set_player(player_num)
    ########################################

    def same_board(self, check_board):
        """
        Checks if the given Board has the same 'grid' as the self's.
        Return: False if a difference is found. True if no difference was found.
        """
        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                if not self.grid[i][j].same_spot(check_board.grid[i][j]):
                    return False
        return True

    def valid_for_open_space(self, _x, _y):
        """
        Given two integers representing coordinates in grid space,
        the located Space in 'grid' is a valid spot to place a Player object.
        These conditions are determined by Santorini's rules.
        """
        return (self.space_on_board(_x, _y) and
                self.grid[_x][_y].playerNum == 0 and
                self.grid[_x][_y].level < 4)

    def space_on_board(self, _x, _y):
        """
        Checks if the given integers are outside the dimensions of the 'grid'.
        """
        return (self.WIDTH > _x >= 0 and
                self.HEIGHT > _y >= 0)

    def valid_player_select(self, given_space, correct_num):
        """
        Given a Space, the spot is checked whether a Player figure is in that spot.
        This is done by checking the Player num of the Space.
        """
        valid_space = self.space_on_board(given_space.getX(), given_space.getY())
        correct_player = False
        if valid_space:
            correct_player = self.grid[given_space.getX()][given_space.getY()].get_player() == correct_num
        return valid_space and correct_player

    def is_too_tall(self, spot, center_level):
        """
        Checks if the Space given is valid height for possible future movement rules.
        I.E. Given Space's height, should be less than or equal to center level +1 for valid movement.
        """
        selected_level = spot.get_level()
        return selected_level <= center_level or center_level + 1 == selected_level

    def get_spaces_around(self, starting_location):
        """
    `   Given a Space representing the starting location of a Player,
        all Space's around that spot in the 'grid' are returned in an Array object.
        """
        possible_locations = []
        starting_x = starting_location.getX() + 1
        starting_y = starting_location.getY() + 1

        RANGE_AROUND_POINT = 8
        for i in range(RANGE_AROUND_POINT):
            ## Coordinates for spot changes over time to loop around the spot.
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
                current_spot = self.grid[starting_x][starting_y]
                possible_locations.append(current_spot)

        return possible_locations

    def move_filter(self, possible_spots, starting_location):
        """
        Given an Array of Spaces and a starting Space, a new Array of Spaces
        is created that represent valid movement spots for a Player.
        """
        filtered_list = []
        starting_level = starting_location.get_level()
        for spot in possible_spots:
            if self.is_too_tall(spot, starting_level):
                filtered_list.append(spot)
        return filtered_list

    def update_player_space(self, player, new_spot):
        """
        Given a Player and a new Space, the locations of both on the 'grid' are swapped.
        """
        self.grid[player.getX()][player.getY()].set_player(0)
        self.grid[new_spot.getX()][new_spot.getY()].set_player(player.get_player())

    def build_on_space(self, picked_space):
        """
        Calls 'build_level' function at the given Space in the 'grid'.
        """
        self.grid[picked_space.getX()][picked_space.getY()].build_level()

    def undo_build_on_space(self, picked_space):
        """
        Calls 'remove_level' function at the given Space in the 'grid'.
        """
        self.grid[picked_space.getX()][picked_space.getY()].remove_level()
