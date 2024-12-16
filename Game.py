## Object that runs and stores info for a single game ##
## of Santorini                                       ##
########################################################
## Author: Jake Swanson
from GameObjects.Board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.all_player_pieces = []

