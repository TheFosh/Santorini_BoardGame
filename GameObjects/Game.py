## Objects that runs and stores info for a single game ##
## of Santorini                                       ##
########################################################
## Author: Jake Swanson
import copy

from ArtificialPlayer import CPU
from GameObjects.Board import Board
from GameObjects.HashableBoard import Hashboard
from GameObjects.Player import Player
from GameObjects.Space import Space
from GameObjects.Turn import Turn


class Game:
    def __init__(self, _cell_num, is_hash = False, ai_on = False):
        self.Board = Board(_cell_num)           # Board object. Stores all location based data and update functions.
        self.HashBoard = Hashboard(_cell_num)   # HashBoard object. Used for optimized gameplay.
        self.IS_HASH = is_hash                  # Bool. Says if a hash is used or not.
        self.AI_ON = ai_on                      # Bool. Says if an AI is used or not.
        self.game_ai = CPU(1, self.get_board())
        self.player_start_order = [1,2,2,1]     # Int Array. Gives the order in which players put their pieces on the board.
                                                    # ex: 1,2,2,1 means that p1 goes first, p2 does both next then p1 puts their last piece down.
        self.all_players = []                   # Player Array. Initialized empty. Stores all player object data.
        self.PLAYER_TURN = 1                    # Int. Number made to signify the starting player.
        self.PICKED_PLAYER = -1                 # Int. Initialized as -1. Index number for 'all_players' array designating a specific player piece.
        self.MOVE = False                       # Bool. Says if the current player is in the MOVE phase of the game or not.
        self.BUILD = False                      # Bool. Says if the current player is in the BUILD phase of the game or not.
        self.game_state = True                  # Bool. Says if the game is over or not.

    ########################################
    ########### GETTERS & SETTERS ##########
    def get_order(self):
        return self.player_start_order

    def get_board(self):
        return self.Board

    def get_hashboard(self):
        return self.HashBoard

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
        """Returns player object from the given index."""
        return self.all_players[player_index]

    def get_move(self):
        return self.MOVE

    def get_build(self):
        return self.BUILD

    def get_player_turn(self):
        return self.PLAYER_TURN

    def get_picked_player(self):
        return self.PICKED_PLAYER

    def get_grid_data(self, spot: Space) -> Space:
        return self.Board.get_chosen_grid_space(spot)

    def set_board(self, _board: Board) -> None:
        self.Board = copy.deepcopy(_board)
        
    ########################################


    def pick_player_spot(self, chosen_cell, player_num):
        """
        Given a Space in grid cords and a player label,
        it is checked if the spot chosen can be a valid starting spot for
        the current player.
        If it is valid, it will return true while also setting the Player
        to the chosen spot.
        Will also add the Space to the list of 'all_players' as a Player object.
        If not, it will ONLY return false.

        If IS_HASH, then the hash board is used.
        """
        if not self.IS_HASH:
            if self.Board.valid_for_open_space(chosen_cell.getX(), chosen_cell.getY()):
                self.Board.set_grid_player(chosen_cell, player_num)
                self.add_player(chosen_cell.getX(), chosen_cell.getY(), player_num)
                return True
            else:
                return False
        else:
            if self.HashBoard.valid_for_open_space(chosen_cell.getX(), chosen_cell.getY()):
                self.HashBoard.set_grid_player(chosen_cell.getX(), chosen_cell.getY(), player_num)
                self.add_player(chosen_cell.getX(), chosen_cell.getY(), player_num)
                return True
            else:
                return False

    def add_player(self, x, y, l):
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

    def get_move_spots(self, player_index):
        """
        Given an integer for a Player object in 'all_players',
        Space's around that Player are returned following legal move rules.
        """

        current_player = self.all_players[player_index]
        possible_move_locations = []
        if not self.IS_HASH:
            possible_move_locations = self.Board.get_spaces_around(current_player)
            possible_move_locations = self.Board.move_filter(possible_move_locations, current_player)
        else:
            possible_move_locations = self.HashBoard.get_spaces_around(current_player.getX(), current_player.getY())
            possible_move_locations = self.HashBoard.move_filter(possible_move_locations, current_player)

        return possible_move_locations

    def move_player(self, player_index, picked_location):
        """
        Moves the Player indexed with the given parameter
        to a given Space in the 'Board' object data.
        """
        current_player = self.all_players[player_index]
        # 'Board' object updates it's location data on the given player.
        if not self.IS_HASH:
            self.Board.update_player_space(current_player, picked_location)
        else:
            c_x = current_player.getX()
            c_y = current_player.getY()
            c_n = current_player.get_player()
            n_x = picked_location.getX()
            n_y = picked_location.getY()
            self.HashBoard.update_player_space(c_x,c_y,c_n,n_x,n_y)
        # Player in 'all_players' gets updated as well.
        self.all_players[player_index].set_cords(picked_location.getX(), picked_location.getY())
        self.all_players[player_index].set_level(picked_location.get_level())
        # Checks if the game is over or not.
        if current_player.get_level() == 3:
            self.game_state = False

    def get_build_spots(self, player_index):
        """
        Finds all spots around the indexed Player given for possible builds.
        """
        current_player = self.all_players[player_index]
        possible_move_locations = []
        if not self.IS_HASH:
            possible_move_locations = self.Board.get_spaces_around(current_player)
        else:
            cx = current_player.getX()
            cy = current_player.getY()
            possible_move_locations = self.HashBoard.get_spaces_around(cx, cy)
        return possible_move_locations

    def spot_in_list(self, picked, options):
        """
        Checks if the 'picked' Space is among the given list of possible Space's in 'options'.
        """
        for i in range(len(options)):
            if picked.getX() == options[i].getX() and picked.getY() == options[i].getY():
                return True
        return False

    def build_at_spot(self, picked_location):
        """
        Records and updates the 'Board' object with building a block level on given Space.
        """
        if not self.IS_HASH:
            self.Board.build_on_space(picked_location)
        else:
            px = picked_location
            py = picked_location
            self.HashBoard.build_on_space(px, py)

    def pick_piece_turn(self, spot):
        """
        Simulates the phase of a turn where a player picks one of their pieces to move.
        Given a Space, it is checked whether that 'spot' contains a Player of the correct label.
        """
        current_board = self.get_board()
        if current_board.valid_player_select(spot, self.PLAYER_TURN):
            ## Successfully chosen a player
            chosen_player_piece = current_board.get_chosen_grid_space(spot)
            self.PICKED_PLAYER = self.get_player_at_spot(chosen_player_piece)
            self.MOVE = True
            return True

        return False

    def pick_piece_turn_hash(self, spot):
        """
        Same as function 'pick_piece_turn' but used for 'Hash_Bord'
        """
        current_board = self.get_hashboard()
        if not self.IS_HASH:
            if current_board.valid_player_select(spot.getX(), spot.getY(), self.PLAYER_TURN):
                ## Successfully chosen a player
                chosen_player_piece = current_board.get_chosen_grid_space(spot.getX(), spot.getY())
                self.PICKED_PLAYER = self.get_player_at_spot(chosen_player_piece)
                self.MOVE = True
                return True
        else:
            spot_x = self.HashBoard.getX(spot)
            spot_y = self.HashBoard.getY(spot)
            if current_board.valid_player_select(spot_x, spot_y, self.PLAYER_TURN):
                ## Successfully chosen a player
                chosen_player_piece = current_board.get_chosen_grid_space(spot_x, spot_y)
                self.PICKED_PLAYER = self.get_player_at_spot(chosen_player_piece)
                self.MOVE = True
                return True
        return False

    def move_piece_turn(self, spot):
        """
        Simulates the move phase of a turn.
        Checks if the given Space is a valid spot to move to.
        """
        move_options = self.get_move_spots(self.PICKED_PLAYER)
        valid_spot = self.spot_in_list(spot, move_options)
        if valid_spot:
            self.MOVE = False
            self.BUILD = True
        return valid_spot

    def build_piece_turn(self, spot):
        """
        Simulates the build phase of a turn.
        Checks whether the given Space is a valid build location or not.
        """
        build_options = self.get_build_spots(self.PICKED_PLAYER)
        valid_spot = self.spot_in_list(spot, build_options)
        if valid_spot:
            self.BUILD = False
            self.PLAYER_TURN = self.PLAYER_TURN % 2 + 1  ## Flip turn order
        return valid_spot

    def AI_Turn(self):
        """
        Given a CPU(AI), the game is simulated to have a turn taken as if someone decided
        a turn for the game.
        """
        if not self.IS_HASH:
            self.game_ai.set_board(self.get_board())
        else:
            self.game_ai.set_board(self.get_hashboard())

        pieces: list[Space] = [self.get_player_at_index(0), self.get_player_at_index(3)]

        self.game_ai.update_all_pieces(pieces, 1)
        decided_turn = self.game_ai.get_best_turn(self)
        p = decided_turn.get_piece()    # Player object chosen.
        m = decided_turn.get_move()     # Space to move to.
        b = decided_turn.get_build()    # Space to build on.
        p: list[Space] = [self.get_player_at_index(1), self.get_player_at_index(2)]

        self.game_ai.update_all_pieces(pieces, 2)

        return decided_turn

    def simulate_turn(self, given_turn: Turn):
        """
        Given a Turn object, a new board is generated as if the
        given turn was followed through on.

        Args:
            given_turn: A Turn object. Assumed to be a valid turn.

        Returns: None
        """
        p = given_turn.get_piece()
        m = given_turn.get_move()
        b = given_turn.get_build()
        self.Board.set_grid_player(m, p.get_player())
        self.Board.set_grid_player(p, 0)
        self.Board.build_on_space(b)

