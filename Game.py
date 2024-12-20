## Object that runs and stores info for a single game ##
## of Santorini                                       ##
########################################################
## Author: Jake Swanson


class Game:
    def __init__(self, p1, p2):
        self.player_start_order = [1,2,2,1]
        self.all_players = []
        for i in range(len(self.player_start_order)):
            if self.player_start_order[i] == 1:
                self.all_players.append(p1)
            elif self.player_start_order[i] == 2:
                self.all_players.append(p2)


    def start_game(self):
        return True

    def get_order(self):
        return self.player_start_order

    ## Sets the player with its given point and returns it's display
    def pick_character_spot(self, picked_space, player_iter):
        self.all_players[player_iter].set_space(picked_space)
        return self.all_players[player_iter].get_display()