## Object representing an AI that predicts the best move to make ##
###################################################################
## Author: Jake Swanson
import math
from os.path import curdir

from GameObjects.Board import Board


class GameEvaluator:
    def __init__(self, _d, _board: Board):
        self.Depth = _d              ## The depth to look into the future for
        self.insight_count = 0  ## The count of how many possible moves the AI has looked at
        self.current_board = _board  ## The board to analyse

    def get_player_pieces(self, player_num):
        pieces = []
        for i in range(self.current_board.WIDTH):
            for j in range(self.current_board.HEIGHT):
                if self.current_board.grid[i][j].get_player() == player_num:
                    pieces.append(self.current_board.grid[i][j])

        return pieces

    def search_moves(self, relevant_player_num):
        """
        :return: All possible turns for the pieces of the relevant player
        """
        piece_turns = []
        pieces = self.get_player_pieces(relevant_player_num)

        for p in pieces:
            piece_turns.append(self.turn_generator(p))

        return piece_turns

    def turn_generator(self, player_piece):
        """
        Makes an array of moves and builds around the given player piece.
        """
        all_turns = []

        all_moves = self.current_board.get_spaces_around(player_piece)
        possible_moves = self.current_board.move_filter(all_moves, player_piece)
        for m in possible_moves:
            possible_builds = self.current_board.get_spaces_around(m)
            all_turns.append(m)
            for b in possible_builds:
                all_turns.append(b)

    def total_score(self, player_piece, potential_spot):
        return (self.winning_score(player_piece, potential_spot)
                + self.height_weights(player_piece, potential_spot)
                + self.player_distance_weights(player_piece, potential_spot))

    def winning_score(self, player_piece, potential_spot):
        if player_piece.get_level() == 2 and potential_spot.get_level() == 3:
            return 10000

        return 0

    def height_weights(self, player_piece, potential_spot):
        """
        Influences turns to favor being at a higher level vs. falling down.
        """
        level_difference = potential_spot.get_level() - player_piece.get_level()
        if  level_difference == 1:
            return level_difference * 10

        return 20 * level_difference

    def player_distance_weights(self, player_piece, potential_spot):
        """
        Influences player pieces to be keep a certain distance to their opponent's pieces.
        """
        opponent_label = 3 - player_piece.get_player()
        opponent_pieces = self.get_player_pieces(opponent_label)

        spaces_away = []
        for o_piece in opponent_pieces:
            x_difference = player_piece.getX() - o_piece.getX()
            y_difference = player_piece.getY() - o_piece.getY()
            e_distance = math.sqrt(math.pow(x_difference, 2) + math.pow(y_difference, 2))

            spaces_away.append(math.floor(math.fabs(e_distance - 1)))

        weights = []
        for space_num in spaces_away:
            ## Want to prefer a distance of 1
            score = 2 - math.pow(space_num - 1, 2)

            ## Arbitrary weight
            distance_weight = 30
            weights.append(score * distance_weight)

        return weights[0] + weights[1]

    def evaluate_next_step(self, relevant_player):
        """
        Every call looks 1 step further into possible moves
        from where it left off.
        """

        for i in self.Depth:
            all_turns = self.search_moves(relevant_player)


