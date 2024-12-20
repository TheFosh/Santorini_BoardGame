## Object that runs and stores info for a single game ##
## of Santorini                                       ##
########################################################
## Author: Jake Swanson


class Game:
    def __init__(self):
        self.all_player_pieces = [1,2,2,1]

    def start_game(self):
        return True

    def get_players(self):
        return self.all_player_pieces