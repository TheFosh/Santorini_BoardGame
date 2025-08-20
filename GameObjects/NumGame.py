## Objects that runs and stores info for a single game ##
## of Santorini. Made to be more efficient.            ##
#########################################################
## Author: Jake Swanson
from ArtificialPlayer import CPU
from GameObjects.HashableBoard import Hashboard
from GameObjects.Player import Player

from GameObjects.Space import Space
from GameObjects.Turn import Turn


class NumGame:
    def __init__(self, _cell_num: int, ai_on = False):

        self.Board = Hashboard(_cell_num)

        self.AI_ON = ai_on

        self.player_start_order = [1,2,2,1]
        self.all_players = []

        self.game_state = True

    ########################################
    ########### GETTERS & SETTERS ##########
    def get_order(self) -> list:
        """
        Returns: A predefined list of integers dictating which player plays a piece next at the start of a game.
        """
        return self.player_start_order

    def get_board(self) -> Hashboard:
        """
        Returns: A numpy array of integers representing the board.
        """
        return self.Board

    def get_player_at_spot(self, spot: list[int]) -> int:
        """
            Looks through the player list to find if there is a player at the given spot. If so, the index of that player is returned.

        spot: A Space object that is being checked against the player list.

        Returns: An integer index representing the found player's location.

        """
        for i in range(len(self.all_players)):
            player = self.all_players[i]
            if spot[0] == player.getX() and spot[1] == player.getY():
                return i

        return -1

    def get_player_at_index(self, player_index: int) -> Player:
        """
        Returns: player object from 'all_players' from the given index.
        """
        return self.all_players[player_index]

    def get_grid_data(self, spot: Space) -> list[int]:
        return self.Board.get_chosen_grid_space([spot.getX(), spot.getY()])
    ########################################

    def pick_player_spot(self, chosen_cell: list[int], player_num: int) -> bool:
        """
        Given a Space in grid cords and a player label,
        it is checked if the spot chosen can be a valid starting spot for
        the current player.
        If it is valid, it will return true while also setting the Player
        to the chosen spot.
        Will also add the Space to the list of 'all_players' as a Player object.
        If not, it will ONLY return false.

        """
        x = chosen_cell[0]
        y = chosen_cell[1]
        if self.Board.valid_for_open_space(x, y):
            self.Board.set_data(x, y, 0, player_num)
            self.add_player(x, y, player_num)
            return True
        else:
            return False

    def add_player(self, x:int , y:int, l:int ) -> None:
        """
        Given the parameters of a Player object, one is created
        and added to the 'all_players' array.
        Assumes all inputs are valid integers.
        Args:
            x: X(Horizontal) coordinate in grid space.
            y: Y(Vertical) coordinate in grid space.
            l: Label of the Player object to be.
        """

        current_player = Player(x,y,l)
        self.all_players.append(current_player)

    def get_move_spots(self, player_index: int) -> list[Space]:
        """
        Given an integer for a Player object in 'all_players',
        Space's around that Player are returned following legal move rules.
        """

        current_player = self.all_players[player_index]
        possible_move_locations = []
        possible_move_locations = self.Board.get_spaces_around(current_player)
        possible_move_locations = self.Board.move_filter(possible_move_locations, current_player)

        return possible_move_locations

    def move_player(self, player_index: int, picked_location: Space) -> None:
        """
        Moves the Player indexed with the given parameter
        to a given Space in the 'Board' object data.
        """
        current_player = self.all_players[player_index]
        # 'Board' object updates it's location data on the given player.

        self.Board.update_player_space(current_player, picked_location)

        # Player in 'all_players' gets updated as well.
        self.all_players[player_index].set_cords(picked_location.getX(), picked_location.getY())
        self.all_players[player_index].set_level(picked_location.get_level())
        # Checks if the game is over or not.
        if current_player.get_level() == 3:
            self.game_state = False

    def get_build_spots(self, player_index: int) -> list[list[int]]:
        """
        Finds all spots around the indexed Player given for possible builds.
        """
        current_player = self.all_players[player_index]
        possible_move_locations = []
        possible_move_locations = self.Board.get_spaces_around(current_player)
        return possible_move_locations

    def spot_in_list(self, picked:Space, options:list[Space]) -> bool:
        """
        Checks if the 'picked' Space is among the given list of possible Space's in 'options'.
        """
        for i in range(len(options)):
            if picked.getX() == options[i].getX() and picked.getY() == options[i].getY():
                return True
        return False

    def build_at_spot(self, picked_location: Space) -> None:
        """
        Records and updates the 'Board' object with building a block level on given Space.
        """
        self.Board.build_on_space(picked_location)

    def AI_Turn(self, cpu: CPU) -> Turn:
        """
        Given a CPU(AI), the game is simulated to have a turn taken as if someone decided
        a turn for the game.
        """
        cur_board = self.get_board()
        CPU.set_board(cur_board)
        decided_turn = CPU.get_best_turn()
        p = decided_turn.get_piece()    # Player object chosen.
        m = decided_turn.get_move()     # Space to move to.
        b = decided_turn.get_build()    # Space to build on.

        return decided_turn


    # NOT SURE IF THIS IS NEEDED.
    # def simulate_turn(self, given_turn):
    #     """
    #     Given a Turn object, a new board is generated as if the
    #     given turn was followed through on.
    #
    #     Args:
    #         given_turn: A Turn object. Assumed to be a valid turn.
    #
    #     Returns: Board object.
    #     """
    #
    #     # sim_board = self.get_board()
    #     # p = given_turn.get_piece()
    #     # sim_board.se