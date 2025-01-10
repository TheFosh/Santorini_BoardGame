from random import Random, randint

from GameObjects.Game import Game


class RandomPlayer:
    def __init__(self,  _g: Game, _p_num):
        self.current_Game = _g
        self.player_label = _p_num

        self.piece_choices = []
        for i in range(len(self.current_Game.player_start_order)):
            if self.current_Game.player_start_order[i] == self.player_label:
                self.piece_choices.append(i)

    def do_turn(self):
        r_int_piece = randint(0,len(self.piece_choices))
        r_piece = self.current_Game.all_players[r_int_piece]

        MOVE = self.current_Game.get_move()
        BUILD = self.current_Game.get_build()

        if not MOVE and not BUILD:
            return r_piece

        elif MOVE:
            return self.generate_move_space(r_piece)

        elif BUILD:
            return self.generate_build_space(r_piece)

    def generate_move_space(self, r_piece):
        current_board = self.current_Game.get_board()
        possible_locations = current_board.get_spaces_around(r_piece)
        move_options = current_board.move_filter(possible_locations, r_piece)

        r_move = randint(0, len(possible_locations)-1)

        return move_options[r_move]

    def generate_build_space(self, r_piece):
        current_board = self.current_Game.get_board()
        build_options = current_board.get_spaces_around(r_piece)

        r_build = randint(0, len(build_options) -1)

        return build_options[r_build]