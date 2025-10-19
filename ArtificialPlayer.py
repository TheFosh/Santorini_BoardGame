## Object representing an AI that predicts the best move to make ##
###################################################################
## Author: Jake Swanson
import copy
import math
from copy import deepcopy

import numpy as np

from BoardDisplay import BoardDisplay
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

        self.hash_value = pow(2,28)
        self.game_states = np.zeros(self.hash_value) -1

        self.p1_pieces = []
        self.p2_pieces = []
        self.display = BoardDisplay(500,500, 50, 5)

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

    def get_board_index(self) -> int:
        index = ""
        for r in self.current_board.grid:
            for s in r:
                sub = str(s.get_level()) + str(s.get_player())
                index += sub

        return int(index)

    def get_board_state(self, ind) -> int:
        return self.game_states[ind % self.hash_value]

    # Setter for setting the board the AI sees.
    def set_board(self, given_board: (Board | Hashboard)):
        self.current_board = copy.deepcopy(given_board)

    def search_moves(self, relevant_player_num):
        """
        :return: All possible turns for the pieces of the relevant player
        """
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
                    self.current_board.set_grid_player(p,0)
                    possible_builds = self.current_board.get_spaces_around(m)
                    for b in possible_builds:
                        all_turns.append(Turn(deepcopy(p), deepcopy(m), deepcopy(b)))
                    self.current_board.set_grid_player(p,p.get_player())
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
        player_one_score = (self.winning_score(p1_pieces) + self.near_blocks_score(p1_pieces) +
                            self.climbing_score(p1_pieces) + self.depleting_moves_score(p2_pieces) +
                            self.pieces_proximaty(p1_pieces))
        player_two_score = (self.winning_score(p2_pieces) + self.near_blocks_score(p2_pieces) +
                            self.climbing_score(p2_pieces) + self.depleting_moves_score(p1_pieces) +
                            self.pieces_proximaty(p2_pieces))
        # print("P2 "+ str(player_two_score))
        # print("P1 "+ str(player_one_score))
        return player_two_score - player_one_score

    def depleting_moves_score(self, op_pi):
        score = 0

        for o in op_pi:
            all_moves = self.search_moves(o.get_player())
            score = (64 - len(all_moves)) * 5

        return score

    def near_blocks_score(self, pieces):
        score = 0

        for p in pieces:
            all_moves = self.current_board.get_spaces_around(p)

            climbable_moves = 0
            for m in all_moves:
                if m.get_level() == p.get_level() +1:
                    climbable_moves += 1

            score += (10 ** p.get_level()) * climbable_moves

        return score

    def pieces_proximaty(self, pieces):

        piece_one = pieces[0]
        piece_two = pieces[1]

        distance = int(math.sqrt((piece_one.getX() - piece_two.getX())**2 + (piece_one.getY() - piece_two.getY())**2))

        return (2 - distance) * 50

    def climbing_score(self, pieces):
        total_score = 0
        for p in pieces:
            total_score += pow(2000, p.get_level())

        return total_score

    def winning_score(self, pieces):
        for p in pieces:
            if p.get_level() == 3:
                return math.inf

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
        self.update_piece(p, p_num, m)
        # print(self.p1_pieces)
        # print(self.p2_pieces)

    def undo_turn(self, turn):
        p = copy.deepcopy(turn.get_piece())
        m = copy.deepcopy(turn.get_move())
        b = copy.deepcopy(turn.get_build())
        p_num = p.get_player()
        self.current_board.set_grid_player(m, 0)
        self.current_board.set_grid_player(p, p_num)
        self.current_board.undo_build_on_space(b)
        self.update_piece(m, p_num, p)

    def update_piece(self, _p: Space, _pnum: int, _m: Space):
        # print(_p)
        if _pnum == 1:
            for i in range(len(self.p1_pieces)):
                if _p.getX() == self.p1_pieces[i].getX() and _p.getY() == self.p1_pieces[i].getY():
                    self.p1_pieces[i].set_cords(_m.getX(), _m.getY())
                    self.p1_pieces[i].set_height(_m.get_level())
                    break
        else:
            for i in range(len(self.p2_pieces)):
                if _p.getX() == self.p2_pieces[i].getX() and _p.getY() == self.p2_pieces[i].getY():
                    self.p2_pieces[i].set_cords(_m.getX(), _m.getY())
                    self.p2_pieces[i].set_height(_m.get_level())
                    break

    def update_all_pieces(self, p: list[Space], p_num):
        if p_num == 1:
            self.p1_pieces = copy.deepcopy(p)
        else:
            self.p2_pieces = copy.deepcopy(p)

    def check_new_board(self, given_board):
        if not self.current_board.same_board(given_board):
            self.current_board = copy.deepcopy(given_board)
            self.current_board = copy.deepcopy(given_board)
            self.insight_count = 0

        return given_board != self.current_board

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

        current_state = self.board_defined()
        if current_state != None:
            return current_state

        if d == 0:
            #if  self.total_board_score() != 0:
            #print(self.total_board_score())
            board_score = self.total_board_score()
            self.add_game_state(board_score)
            return board_score

        all_turns = self.search_moves(p)

        if len(all_turns) == 0 or self.did_oppenet_win(3-p):
            new_score =  pow(-1, 3-p) * math.inf
            return new_score

        if p == 2:
            score = -math.inf
            for i in range(len(all_turns)):
                current_turn = deepcopy(all_turns[i])
                self.simulate_turn(current_turn)
                # board = copy.deepcopy(self.get_board())
                # self.display.display_artificial_game(board)
                negate_flip = 1 #pow(-1,3-p)

                score = negate_flip * self.evaluate_board(d - 1, 3 - p, alpha, beta)

                self.undo_turn(current_turn)

                if score >= beta:
                    return beta

                alpha = max(score, alpha)

            return score

        else:
            score = math.inf
            for i in range(len(all_turns)):
                current_turn = deepcopy(all_turns[i])
                self.simulate_turn(current_turn)
                # board = copy.deepcopy(self.get_board())
                # self.display.display_artificial_game(board)
                negate_flip = 1  # pow(-1,3-p)
                score = negate_flip * self.evaluate_board(d - 1, 3 - p, alpha, beta)
                self.undo_turn(current_turn)

                if score <= alpha:
                    return alpha

                beta = min(score, beta)

            return score

    def get_best_turn(self, p=2):
        """
        Method made to find the best turn a player can make on a turn.
        Args:
            p: A number representing which player is currently playing. By default, it player 1.

        Returns: A Turn object representing the best course of action the AI should make.
        """

        self.p1_pieces = self.get_player_pieces(1)
        self.p2_pieces = self.get_player_pieces(2)
        poss_turns = self.search_moves(p)
        turn_count =len(poss_turns)

        for i in range(len(poss_turns)):
            current_turn = copy.deepcopy(poss_turns[i])
            self.simulate_turn(current_turn)
            # board = self.get_board()
            # self.display.display_artificial_game(board)
            score = self.evaluate_board(self.get_depth(), (3-p), -math.inf, math.inf)
            if self.did_oppenet_win(3-p):
                score = -math.inf
            poss_turns[i].set_evaluation(score)
            self.undo_turn(current_turn)
            poss_turns[i].set_id(i+1)
            print(str((i+1)/turn_count * 100) + "%")

        decided_turn = Turn()
        decided_turn.set_evaluation(-math.inf)

        for t in poss_turns:
            if t.get_evaluation() > decided_turn.get_evaluation():
                decided_turn = t

        #print(poss_turns)
        print(decided_turn)
        return decided_turn

    def did_oppenet_win(self, p: int) -> bool:
        if p == 1:
            return self.p1_pieces[0].get_level() == 3 or self.p1_pieces[1].get_level() == 3
        else:
            return self.p2_pieces[0].get_level() == 3 or self.p2_pieces[1].get_level() == 3

    def board_defined(self) -> int | None:
        board_ind = self.get_board_index()
        score = self.game_states[board_ind % self.hash_value]
        if score != -1 :
            return self.get_board_state(board_ind)

        return None

    def add_game_state(self, score):
        ind = self.get_board_index()
        self.game_states[ind % self.hash_value] = score