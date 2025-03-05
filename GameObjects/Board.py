## Object representing the board of spaces in a game ##
#######################################################
## Author: Jake Swanson

from GameObjects.Space import Space

class Board:

    def __init__(self, cell_count):
        self.WIDTH = cell_count
        self.HEIGHT = cell_count

        self.grid = [
                        [Space(j, i) for i in range(self.WIDTH)]
                        for j in range(self.HEIGHT)
                    ]

        #### BOARD MEANING ####
        ## Every 5 bits are a single cell
        ## The first 2 of the 5 bits are representing the player number.
        ## The last 3 are for the level of the space.
        ## There should be 5 * 25 bits for every space on the board.
        #self.hash_board = [self.decimal_to_binary(0)] * cell_count ** 2

    ########################################
    ########### GETTERS & SETTERS ##########
    def get_width_height(self):
        return self.WIDTH

    def get_chosen_grid_space(self, chosen_space):
        """Given a point, the corresponding grid space is returned"""
        return self.grid[chosen_space.getX()][chosen_space.getY()]

    def set_grid_player(self, chosen_space, player_num):
        """Sets given space to be the given player num."""
        self.grid[chosen_space.getX()][chosen_space.getY()].set_player(player_num)
    ########################################

    def same_board(self, check_board):
        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                if not self.grid[i][j].same_spot(check_board.grid[i][j]):
                    return False
        return True

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
        valid_space = False
        correct_player = False
        if self.space_on_board(given_space.getX(), given_space.getY()):
            valid_space = self.space_on_board(given_space.getX(), given_space.getY())
            correct_player = self.grid[given_space.getX()][given_space.getY()].get_player() == correct_num
        return valid_space and correct_player

    def is_too_tall(self, spot, center_level):
        selected_level = spot.get_level()
        return selected_level <= center_level or center_level + 1 == selected_level

    def get_spaces_around(self, starting_location):
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
        filtered_list = []
        starting_level = starting_location.get_level()
        for spot in possible_spots:
            if self.is_too_tall(spot, starting_level):
                filtered_list.append(spot)
        return filtered_list

    def update_player_space(self, player, new_spot):
        self.grid[player.getX()][player.getY()].set_player(0)
        self.grid[new_spot.getX()][new_spot.getY()].set_player(player.get_player())

    def build_on_space(self, picked_space):
        self.grid[picked_space.getX()][picked_space.getY()].build_level()

    def undo_build_on_space(self, picked_space):
        self.grid[picked_space.getX()][picked_space.getY()].remove_level()