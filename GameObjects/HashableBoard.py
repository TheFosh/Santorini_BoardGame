## Object representing the board of spaces in a game as a binary number ##
##########################################################################
## Author: Jake Swanson

class Hashboard:
    def __init__(self, side_cell_count):
        self.dimensions = side_cell_count

        #### BOARD MEANING ####
        ## 1D array
        ## Every 5 bits are a single cell
        ## The first 2 of the 5 bits are representing the player number.
        ## The last 3 are for the level of the space.
        ## There should be 5 * 25 bits for every space on the board.
        self.hash_board = [self.decimal_to_binary(0)] * side_cell_count**2

    def decimal_to_binary(self, n):
        return bin(n)[2:]
    def binary_to_decimal(self, n):
        return int(n, 2)

    ########################################
    ########### GETTERS & SETTERS ##########
    def get_position_num(self, x, y):
        return x + y * self.dimensions

    def getX(self, n):
        return n % self.dimensions

    def getY(self, n):
        return n / self.dimensions

    def get_width_height(self):
            return self.dimensions

    def get_space_level(self, x, y):
        b_spot = self.get_chosen_grid_space(x, y)
        d_spot = self.binary_to_decimal(b_spot)
        return int(d_spot % 8)

    def get_space_player_num(self, x, y):
        b_spot = self.get_chosen_grid_space(x, y)
        d_spot = self.binary_to_decimal(b_spot)
        return int(d_spot / 8)

    def get_chosen_grid_space(self, x, y):
        """Given a point, the corresponding data in the space is returned"""
        return self.hash_board[self.get_position_num(x, y)]

    def set_grid_player(self, x, y, player_num):
        """Sets given space to be the given player num."""
        pn = player_num * 8
        binary_s = self.hash_board[self.get_position_num(x, y)]
        decimal_s = self.binary_to_decimal(binary_s)
        building_b = decimal_s % 8
        self.hash_board[self.get_position_num(x, y)] = self.decimal_to_binary(pn + building_b)

    ########################################

    def same_board(self, check_board):
        for i in range(len(self.hash_board)):
            if check_board[i] != self.hash_board[i]:
                return False
        return True

    def valid_for_open_space(self, x, y):
        return (self.space_on_board(x, y) and
                int(self.get_space_player_num(x, y)) == 0 and
                self.get_space_level(x, y) < 4)

    def space_on_board(self, _x, _y):
        return (self.dimensions > _x >= 0 and
                self.dimensions > _y >= 0)

    def valid_player_select(self, x, y, correct_num):
        """
        Returns whether a player figure is
        in the selected spot and is the correct
        number.
        """
        valid_space = False
        correct_player = False
        if self.space_on_board(x, y):
            valid_space = self.space_on_board(x, y)
            correct_player = self.get_space_player_num(x, y) == correct_num
        return valid_space and correct_player

    def is_too_tall(self, x, y, center_level):
        selected_level = self.get_space_level(x, y)
        return selected_level <= center_level or center_level + 1 == selected_level

    def get_spaces_around(self, x, y):
        possible_locations = []
        OPERATORS = [-6,-5,-4,-1,1,4,5,6]

        for o in OPERATORS:
            grid_index = self.get_position_num(x, y)

            right = grid_index % 5 == 4
            left = grid_index % 5 == 0
            top = grid_index < 5
            bottom = grid_index >= 20

            spot_check = True
            if ((right and(o == -4 or o == 1 or o == 6)) or
                    (left and(o == -1 or o == -6 or o == 4)) or
                    (top and(o == -4 or o == -5 or o == -6)) or
                    (bottom and(o == 4 or o == 5 or o == 6))):
                    spot_check = False
            else:
                grid_index += o

            valid_spot = self.valid_for_open_space(int(grid_index% self.dimensions), int(grid_index/self.dimensions))
            valid_spot = valid_spot and spot_check
            if valid_spot:
                print(grid_index)
                current_spot = self.hash_board[grid_index]
                possible_locations.append(current_spot)

        return possible_locations

    def move_filter(self, possible_spots, starting_location):
        filtered_list = []
        start_x = int(starting_location% self.dimensions)
        start_y = int(starting_location/self.dimensions)
        starting_level = self.get_space_level(start_x, start_y)
        for spot in possible_spots:
            s_x = int(starting_location% self.dimensions)
            s_y = int(starting_location/self.dimensions)
            if self.is_too_tall(s_x, s_y, starting_level):
                filtered_list.append(spot)
        return filtered_list

    def update_player_space(self, p_x, p_y, p_n, new_x, new_y):
        """
        Given Player starting location and number data, and a new location
        data, the board is updated on where the player is being moved to.
        """
        self.hash_board[p_x + 5 * p_y] = self.decimal_to_binary(0) # Old player location updated to 0 for no player.
        self.hash_board[new_x + 5 * new_y] = self.decimal_to_binary(p_n) # New player location updated to have the player number added.

    def build_on_space(self, x, y):
        if self.binary_to_decimal(self.get_space_level(x,y)) < 4:
            self.hash_board[self.get_position_num(x,y)] += 1

    def undo_build_on_space(self, x, y):
        if self.binary_to_decimal(self.get_space_level(x, y)) > 0:
            self.hash_board[self.get_position_num(x,y)] -= 1
