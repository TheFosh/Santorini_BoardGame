## Object representing an AI that predicts the best move to make ##
###################################################################
## Author: Jake Swanson
import math
from os.path import curdir
from xxsubtype import bench

from GameObjects.Board import Board
from GameObjects.Turn import Turn


class GameEvaluator:

    def __init__(self, _d, _board: Board):
        self.Depth = _d              ## The depth to look into the future for
        self.insight_count = 0  ## The count of how many possible moves the AI has looked at
        self.current_board = _board  ## The board to analyse
        self.future_board = _board

    def get_player_pieces(self, player_num):
        pieces = []
        for i in range(self.future_board.WIDTH):
            for j in range(self.future_board.HEIGHT):
                if self.future_board.grid[i][j].get_player() == player_num:
                    pieces.append(self.future_board.grid[i][j])

        return pieces

    def search_moves(self, relevant_player_num):
        """
        :return: All possible turns for the pieces of the relevant player
        """
        pieces = self.get_player_pieces(relevant_player_num)
        all_turns = []

        for p in pieces:
            all_moves = self.future_board.get_spaces_around(p)
            possible_moves = self.future_board.move_filter(all_moves, p)
            for m in possible_moves:
                possible_builds = self.future_board.get_spaces_around(m)
                for b in possible_builds:
                    all_turns.append(Turn(p, m, b))

        return all_turns

    def total_board_score(self):
        return 0

    def simulate_turn(self, turn):
        """
        Given points on a board, a new board is created.
        These points are assumed to be valid and used to simulate a
        valid turn for a player.
        """
        temp_board = self.future_board

        temp_board.set_grid_player(turn.get_piece(), 0)
        temp_board.set_grid_player(turn.get_move(), turn.get_piece().get_player())
        temp_board.build_on_space(turn.get_build())

        return temp_board

    def undo_turn(self, turn):
        temp_board = self.future_board

        temp_board.set_grid_player(turn.get_piece(), turn.get_piece().get_player())
        temp_board.set_grid_player(turn.get_move(), 0)
        turn.get_build().remove_level()
        temp_board.build_on_space(turn.get_build())

        return temp_board

    def check_new_board(self, given_board):
        if given_board != self.current_board:
            self.current_board = given_board
            self.future_board = given_board
            self.insight_count = 0

        return given_board != self.current_board

    def find_best_turn(self, all_turns):
        turn = []
        best_turn = all_turns[0]

        for i in range(int(len(turn)/3)):
            current_turn = all_turns[i]
            if self.total_score(best_turn) < self.total_score(current_turn):
                best_turn = current_turn

        return best_turn

    def evaluate_board_step(self, given_board):
        """
        Every call looks 1 step further into possible moves
        from where it left off.
        """
        self.check_new_board(given_board)
        player_one_score = self.evaluate_board(self.Depth, 1)

        return player_one_score

    def evaluate_board(self, d, p):
        if d == 0:
            return self.total_board_score()

        all_turns = self.search_moves(p)

        best_score = -math.inf

        for t in all_turns:

            self.future_board = self.simulate_turn(t)
            score = -self.evaluate_board(d-1, 3-p)
            best_score = max(best_score, score)
            self.future_board = self.undo_turn(t)

        return best_score