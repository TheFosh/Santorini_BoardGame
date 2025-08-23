## Object representing an AI that predicts the best move to make ##
###################################################################
## Author: Jake Swanson
import copy
import math

import numpy as np

from GameObjects.Board import Board
from GameObjects.HashableBoard import Hashboard
from GameObjects.Space import Space
from GameObjects.Turn import Turn

class CPU:
    def __init__(self, _d, board):
        self.Depth = _d              ## The depth to look into the current for
        self.insight_count = 0  ## The count of how many possible moves the AI has looked at
        self.current_board = board  ## The board to analyse

        self.PLAYER_NUM_COUNT = 1
        self.BUILD_NUM_COUNT = 1
        self.SPACES_COUNT = 25
        self.BITS = (self.PLAYER_NUM_COUNT + self.BUILD_NUM_COUNT) * self.SPACES_COUNT
        self.hashArray = []
        self.p1_pieces = []
        self.p2_pieces = []

    def get_player_pieces(self, player_num):
        pieces = []
        for i in range(self.current_board.WIDTH):
            for j in range(self.current_board.HEIGHT):
                if self.current_board.grid[i][j].get_player() == player_num:
                    pieces.append(copy.deepcopy(self.current_board.grid[i][j]))
        return pieces

    def get_depth(self):
        return self.Depth

    def get_board(self):
        return self.current_board

    def get_dec_equivalence(self):
        board = self.get_board()
        binary_state = ""
        for row in board.grid:
            for spot in row:
                pn = spot.get_player()
                player_dec = str(pn)
                bn = spot.get_level()
                build_dec = str(bn)
                binary_state += player_dec + build_dec

        return binary_state

    def get_hash_eval(self, hash_ind):
        all_data = self.get_hash_at_loc(hash_ind)
        current_eval = int(all_data[self.BITS:])
        return current_eval

    def get_hash_at_loc(self, hash_ind):
        for i in range(len(self.hashArray)):
            hash_data = self.hashArray[i]
            cur_hash_ind = hash_data[:self.BITS]
            if cur_hash_ind.__eq__(hash_ind):
                return hash_data
        return "0" * self.BITS + "-1"

    # Setter for setting the board the AI sees.
    def set_board(self, given_board: (Board | Hashboard)):
        self.current_board = copy.deepcopy(given_board)

    def search_moves(self, relevant_player_num):
        """
        :return: All possible turns for the pieces of the relevant player
        """
        pieces = []
        if relevant_player_num == 1:
            pieces = self.p1_pieces
        else:
            pieces = self.p2_pieces
        all_turns = []

        for p in pieces:
            if p.get_level() < 3:
                all_moves = self.current_board.get_spaces_around(p)
                possible_moves = self.current_board.move_filter(all_moves, p)
                for m in possible_moves:
                    possible_builds = self.current_board.get_spaces_around(m)
                    for b in possible_builds:
                        all_turns.append(Turn(p, m, b))
            else:
                return []

        return all_turns

    def total_board_score(self):
        """
        Calculates the advantage of a player in the current board.
        :return: Positive values means an advantage for player 1. Negative means player 2.
        """

        p1_pieces = self.p1_pieces
        p2_pieces = self.p2_pieces
        player_one_score = (self.winning_score(p1_pieces) + self.climbing_score(p1_pieces))
                            #self.near_blocks_score(p1_pieces) +
                            #self.climbing_score(p1_pieces))
        player_two_score = (self.winning_score(p2_pieces) + self.climbing_score(p2_pieces))
                            #self.near_blocks_score(p2_pieces) +
                            #self.climbing_score(p2_pieces))
        # print("P2 "+ str(player_two_score))
        # print("P1 "+ str(player_one_score))
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
        # print(self.p1_pieces)
        # print(self.p2_pieces)
        p_num = turn.get_piece().get_player()
        p = copy.deepcopy(turn.get_piece())
        m = copy.deepcopy(turn.get_move())
        b = copy.deepcopy(turn.get_build())
        self.current_board.set_grid_player(p, 0)
        self.current_board.set_grid_player(m, p_num)
        self.current_board.build_on_space(b)
        self.update_piece(p, m)
        # print(self.p1_pieces)
        # print(self.p2_pieces)

    def undo_turn(self, turn):
        p_num = turn.get_move().get_player()
        p = copy.deepcopy(turn.get_piece())
        m = copy.deepcopy(turn.get_move())
        b = copy.deepcopy(turn.get_build())
        self.current_board.set_grid_player(p, p_num)
        self.current_board.set_grid_player(m, 0)
        self.current_board.undo_build_on_space(b)
        self.update_piece(m, p)

    def update_piece(self, _p: Space, _m: Space):
        # print(_p)
        p_num = _p.get_player()
        if p_num == 1:
            for i in range(len(self.p1_pieces)):
                if _p.getX() == self.p1_pieces[i].getX() and _p.getY() == self.p1_pieces[i].getY():
                    self.p1_pieces[i].set_cords(_m.getX(), _m.getY())
                    self.p1_pieces[i].set_height(_m.get_level())
        else:
            for i in range(len(self.p2_pieces)):
                if _p.getX() == self.p2_pieces[i].getX() and _p.getY() == self.p2_pieces[i].getY():
                    self.p2_pieces[i].set_cords(_m.getX(), _m.getY())
                    self.p2_pieces[i].set_height(_m.get_level())

    def update_all_pieces(self, p: list[Space], p_num):
        if p_num == 1:
            self.p1_pieces = copy.deepcopy(p)
        else:
            self.p2_pieces = copy.deepcopy(p)

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
        all_turns = self.search_moves(p)

        if d == 0 or len(all_turns) == 0:
            #if  self.total_board_score() != 0:
            #print(self.total_board_score())
            return self.total_board_score()

        if self.did_opponent_win(p * 2 - 3):
            return -1000000000

        for t in all_turns:
            current_turn = copy.deepcopy(t)
            self.simulate_turn(current_turn)
            negate_flip = 1 #(p % 2 + 1)
            score = negate_flip * self.evaluate_board(d - 1, 3 - p, -beta, -alpha)
            self.undo_turn(current_turn)

            if score >= beta:
                return beta

            alpha = max(score, alpha)
        return alpha

    def get_best_turn(self, p=2):
        """
        Method made to find the best turn a player can make on a turn.
        Args:
            p: A number representing which player is currently playing. By default, it player 1.

        Returns: A Turn object representing the best course of action the AI should make.
        """

        """
            TODO: BOARD GRID IS NOT ACCURATE ON SIMULATIONS
        """
        self.p1_pieces = self.get_player_pieces(1)
        self.p2_pieces = self.get_player_pieces(2)
        poss_turns = copy.deepcopy(self.search_moves(p))
        for i in range(len(poss_turns)):
            current_turn = copy.deepcopy(poss_turns[i])
            self.simulate_turn(current_turn)
            score = self.evaluate_board(self.get_depth(), (p % 2 + 1), -math.inf, math.inf)
            poss_turns[i].set_evaluation(score)
            self.undo_turn(current_turn)
            poss_turns[i].set_id(i+1)
            #print(str((i+1)/turn_count) + "%")

        decided_turn = Turn()

        for t in poss_turns:
            if t.get_evaluation() > decided_turn.get_evaluation():
                decided_turn = t

        #print(poss_turns)
        print(decided_turn)
        return decided_turn

    def did_opponent_win(self, p: int) -> bool:
        if p == 1:
            return self.p1_pieces[0].get_level() == 3 or self.p1_pieces[1].get_level() == 3
        else:
            return self.p2_pieces[0].get_level() == 3 or self.p2_pieces[1].get_level() == 3