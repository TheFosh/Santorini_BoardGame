## Object representing an AI that predicts the best move to make ##
###################################################################
## Author: Jake Swanson
import copy
import math

import numpy as np

from GameObjects.Board import Board
from GameObjects.Turn import Turn


class CPU:

    def __init__(self, _d, _board: Board):
        self.Depth = _d              ## The depth to look into the current for
        self.insight_count = 0  ## The count of how many possible moves the AI has looked at
        self.current_board = copy.deepcopy(_board)  ## The board to analyse

    def get_depth(self):
        return self.Depth

    def get_board(self):
        return self.current_board

    def get_player_pieces(self, player_num):
        pieces = []
        for i in range(self.current_board.WIDTH):
            for j in range(self.current_board.HEIGHT):
                if self.current_board.grid[i][j].get_player() == player_num:
                    pieces.append(self.current_board.grid[i][j])
        return pieces

    # Setter for setting the board the AI sees.
    def set_board(self, given_board):
        self.current_board = copy.deepcopy(given_board)

    def search_moves(self, relevant_player_num):
        """
        :return: All possible turns for the pieces of the relevant player
        """
        pieces = self.get_player_pieces(relevant_player_num)
        all_turns = []

        for p in pieces:
            all_moves = self.current_board.get_spaces_around(p)
            possible_moves = self.current_board.move_filter(all_moves, p)
            for m in possible_moves:
                possible_builds = self.current_board.get_spaces_around(m)
                for b in possible_builds:
                    all_turns.append(Turn(p, m, b))

        return all_turns

    def total_board_score(self):
        """
        Calculates the advantage of a player in the current board.
        :return: Positive values means an advantage for player 1. Negative means player 2.
        """

        p1_pieces = self.get_player_pieces(1)
        p2_pieces = self.get_player_pieces(2)
        player_one_score = (self.winning_score(p1_pieces) + self.climbing_score(p1_pieces))
                            #self.near_blocks_score(p1_pieces) +
                            #self.climbing_score(p1_pieces))
        player_two_score = (self.winning_score(p2_pieces) + self.climbing_score(p2_pieces))
                            #self.near_blocks_score(p2_pieces) +
                            #self.climbing_score(p2_pieces))
        #print("p1: " + str(player_one_score))

        #print("p2: " + str(player_two_score))

        return player_two_score - player_one_score

    def near_blocks_score(self, pieces):
        score = 0

        for p in pieces:
            all_moves = self.current_board.get_spaces_around(p)
            climbable_moves = 0
            for m in all_moves:
                if m.get_level() + 1 == p.get_level():
                    climbable_moves += 1

            score += 10 * climbable_moves ** 2

        return score

    def climbing_score(self, pieces):
        total_score = 0
        for p in pieces:
            if p.get_level() < 4:
                total_score += p.get_level() * 50

        return total_score

    def winning_score(self, pieces):
        for p in pieces:
            if p.get_level() == 3:
                return 10000000

        return 0

    def simulate_turn(self, turn):
        """
        Given points on a board, a new board is created.
        These points are assumed to be valid and used to simulate a
        valid turn for a player.
        """
        p_num = turn.get_piece().get_player()
        self.current_board.set_grid_player(turn.get_piece(), 0)
        self.current_board.set_grid_player(turn.get_move(), p_num)
        self.current_board.build_on_space(turn.get_build())

    def undo_turn(self, turn):
        p_num = turn.get_move().get_player()
        self.current_board.set_grid_player(turn.get_piece(), p_num)
        self.current_board.set_grid_player(turn.get_move(), 0)
        self.current_board.undo_build_on_space(turn.get_build())

    def check_new_board(self, given_board):
        if not self.current_board.same_board(given_board):
            self.current_board = copy.deepcopy(given_board)
            self.current_board = copy.deepcopy(given_board)
            self.predicting_board = copy.deepcopy(given_board)
            self.insight_count = 0

        return given_board != self.current_board

    def evaluate_board_step(self, given_board):
        """
        Every call looks 1 step further into possible moves
        from where it left off.
        """
        self.check_new_board(given_board)
        player_one_score = self.evaluate_board(self.Depth, 1, self.alpha, self.beta)
        self.current_board = copy.deepcopy(self.predicting_board)
        return player_one_score

    def evaluate_board(self, d, p, alpha, beta):
        # print("Alpha: " + str(alpha))
        # print("Beta: " + str(beta))
        """
        Recursive method of evaluating board states of a game of Santorini.
        Looks into the current of the depth given.
        Args:
            d: Depth of search
            p: number representing a player. Supposed to be a 1 or a 2.
            alpha: Alpha value in pruning technique.
            beta: Beta value in pruning technique.

        Returns: Integer representing a score of the current board.



        """

        if d == 0:
            #if  self.total_board_score() != 0:
            #print(self.total_board_score())
            return self.total_board_score()

        all_turns = self.search_moves(p)
        if len(all_turns) == 0:
            return 0

        for t in all_turns:

            self.simulate_turn(t)
            score = -self.evaluate_board(d - 1, 3 - p, -beta, -alpha)
            self.undo_turn(t)

            if score >= beta:
                return beta

            alpha = max(score, alpha)
        return alpha

    def get_best_turn(self, p=2):
        """
        Method made to find the best turn a player can make on a turn.
        Args:
            p: A number representing which player is currently playing. By default, it player 2.

        Returns: A Turn object representing the best course of action the AI should make.
        """
        poss_turns = self.search_moves(p)
        turn_count = len(poss_turns)
        for i in range(len(poss_turns)):
            self.simulate_turn(poss_turns[i])
            score = self.evaluate_board(self.get_depth(), p, -math.inf, math.inf)
            poss_turns[i].set_evaluation(score)
            self.undo_turn(poss_turns[i])
            poss_turns[i].set_id(i+1)
            print(str((i+1)/turn_count) + "%")

        decided_turn = Turn()

        for t in poss_turns:
            if t.get_evaluation() > decided_turn.get_evaluation():
                decided_turn = t

        #print(poss_turns)
        print(decided_turn)
        return decided_turn