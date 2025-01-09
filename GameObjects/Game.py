## Object that runs and stores info for a single game ##
## of Santorini                                       ##
########################################################
## Author: Jake Swanson
from GameObjects.Board import Board
from GameObjects.Player import Player


class Game:
    def __init__(self, _cell_num):
        self.Board = Board(_cell_num)
        self.player_start_order = [1,2,2,1]
        self.all_players = []

        self.PLAYER_TURN = 1
        self.PICKED_PLAYER = -1
        self.MOVE = False
        self.BUILD = False

        self.game_state = True

    ########################################
    ########### GETTERS & SETTERS ##########
    def get_order(self):
        return self.player_start_order

    def get_board(self):
        return self.Board

    def get_player_at_spot(self, spot):
        """
        Looks through all players for the correct one.
        Returns the index in which it was found. Returns -1 if none is found.
        """
        for i in range(len(self.all_players)):
            player = self.all_players[i]
            if spot.getX() == player.getX() and spot.getY() == player.getY():
                return i

        return -1

    def get_player_at_index(self, player_index):
        return self.all_players[player_index]

    def get_move(self):
        return self.MOVE

    def get_build(self):
        return self.BUILD

    def get_player_turn(self):
        return self.PLAYER_TURN

    def get_picked_player(self):
        return self.PICKED_PLAYER
    ########################################

    def pick_player_spot(self, chosen_cell, player_num):
        """
        Given a space in grid cords and a player label,
        it is checked if the spot chosen can be a valid starting spot for
        the player.
        If it is valid, it will return true while also setting the player
        to the chosen spot. Also, will add it to the list of players.
        If not, it will ONLY return false.
        """
        if self.Board.valid_for_open_space(chosen_cell.getX(), chosen_cell.getY()):
            self.Board.set_grid_player(chosen_cell, player_num)
            self.add_player(chosen_cell.getX(),chosen_cell.getY(), player_num)
            return True
        else:
            return False

    def set_character_spot(self, picked_space, player_iter):
        """Sets the player with its given point."""
        self.all_players[player_iter].set_space(picked_space)

    def add_player(self, x, y, l):
        current_player = Player(x,y,l)
        self.all_players.append(current_player)

    def get_move_spots(self, player_index):
        """
        Given an integer for a player in all_players,
        the move action of the game is preformed.
        """
        current_player = self.all_players[player_index]
        possible_move_locations = self.Board.get_spaces_around(current_player)
        possible_move_locations = self.Board.move_filter(possible_move_locations, current_player)
        return possible_move_locations

    def move_player(self, picked_player, picked_location):
        """
        Moves the selected player to a chosen space and changes the player and board objects.
        :param picked_player: integer representing a player in all_players
        :param picked_location: Space where the picked player is chosen to move to. Assumed to be possible.
        :return: Nothing
        """
        current_player = self.all_players[picked_player]
        self.Board.update_player_space(current_player, picked_location)
        self.all_players[picked_player].set_cords(picked_location.getX(), picked_location.getY())
        self.all_players[picked_player].set_level(picked_location.get_level())
        if current_player.get_level() == 3:
            self.game_state = False

    def get_build_spots(self, player_index):
        current_player = self.all_players[player_index]
        possible_move_locations = self.Board.get_spaces_around(current_player)
        return possible_move_locations

    def spot_in_list(self, picked, options):
        for i in range(len(options)):
            if picked.getX() == options[i].getX() and picked.getY() == options[i].getY():
                return True
        return False

    def build_at_spot(self, picked_location):
        """
        Records and updates the board object with building a block level on given spot.
        :param picked_location: Space object that is assumed to be a vaild build location
        :return: Nothing
        """
        self.Board.build_on_space(picked_location)

    def pick_piece_turn(self, spot):
        current_board = self.get_board()
        if current_board.valid_player_select(spot, self.PLAYER_TURN):
            ## Successfully chosen a player
            chosen_player_piece = current_board.get_chosen_grid_space(spot)
            self.PICKED_PLAYER = self.get_player_at_spot(chosen_player_piece)
            self.MOVE = True
            return True

        return False

    def move_piece_turn(self, spot):
        move_options = self.get_move_spots(self.PICKED_PLAYER)
        valid_spot = self.spot_in_list(spot, move_options)
        if valid_spot:
            self.MOVE = False
            self.BUILD = True
        return valid_spot

    def build_piece_turn(self, spot):
        build_options = self.get_build_spots(self.PICKED_PLAYER)
        valid_spot = self.spot_in_list(spot, build_options)
        if valid_spot:
            self.BUILD = False
            self.PLAYER_TURN = self.PLAYER_TURN % 2 + 1  ## Flip turn order
        return valid_spot