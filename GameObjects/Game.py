## Object that runs and stores info for a single game ##
## of Santorini                                       ##
########################################################
## Author: Jake Swanson
from GameObjects.Board import Board
from GameObjects.Player import Player


class Game:
    def __init__(self, _width, _height, _cell_num):
        self.Board = Board(_width, _height, _cell_num)
        self.player_start_order = [1,2,2,1]
        self.all_players = []
        self.width = _width
        self.height = _height

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
        return possible_move_locations