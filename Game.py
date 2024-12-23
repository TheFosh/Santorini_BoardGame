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
    ########################################

    def pick_player_spot(self, chosen_cell, player_num):
        """
        Given a space in grid cords and a player label,
        it is checked if the spot chosen can be a valid starting spot for
        the player.
        If it is valid, it will return true while also setting the player
        to the chosen spot
        If not, it will ONLY return false.
        """
        if self.Board.valid_for_player_start(chosen_cell.getX(), chosen_cell.getY()):
            self.Board.set_grid_player(chosen_cell, player_num)
            return True
        else:
            return False

    def pick_character_spot(self, picked_space, player_iter):
        """Sets the player with its given point and returns it's display"""
        self.all_players[player_iter].set_space(picked_space)
        return self.all_players[player_iter].get_display()