## Object that runs and stores info for a single game ##
## of Santorini                                       ##
########################################################
## Author: Jake Swanson
from GameObjects.Board import Board
from GameObjects.Player import Player


class Game:
    def __init__(self):
        self.player_start_order = [1,2,2,1]
        self.all_players = []
        for i in range(len(self.player_start_order)):
            if self.player_start_order[i] == 1:
                self.all_players.append(Player(-1,-1,1))
            elif self.player_start_order[i] == 2:
                self.all_players.append(Player(-1,-1,2))

    def get_order(self):
        return self.player_start_order

    ## Sets the player with its given point and returns it's display
    def pick_character_spot(self, picked_space, player_iter):
        self.all_players[player_iter].set_space(picked_space)
        return self.all_players[player_iter].get_display()