## Object for setting up the Graphical User Interface ##
########################################################
## Author: Jake Swanson
import copy
import time
from math import floor

from BoardDisplay import BoardDisplay
from GameObjects.Board import Board
from GameObjects.Game import Game

from GameObjects.NumGame import NumGame
from GameObjects.Player import Player
from GameObjects.Space import Space
from GameObjects.Turn import Turn


class GUI:
    def __init__(self, _height, _width, _off, _cell_num, ai_on = False, _is_num = False):
        if _is_num:
            self.Game = NumGame(_cell_num, ai_on = ai_on)
        else:
            self.Game = Game(_cell_num, is_hash=_is_num)

        self.IS_NUM = _is_num
        self.AI = ai_on

        self.display = BoardDisplay(_height, _width, _off, _cell_num, ai_on=ai_on, _is_num=_is_num)
########################################
########### GETTERS & SETTERS ##########
    def get_window(self):
        return self.display.get_window()

    def get_board(self):
        return self.Game.get_board()

    def set_board(self, given_board: Board):
        self.Game.set_board(given_board)

    def set_game(self, given_game_state: Game) -> None:
        self.Game = copy.deepcopy(given_game_state)

########################################

    def ask_for_grid_point(self) -> Space | list[int]:
        win = self.display.get_window()
        mouse = win.getMouse()
        return self.convert_display_on_grid(mouse.getX(), mouse.getY())

    def convert_display_on_grid(self, _disX, _disY) -> Space | list[int]:

        pad, col_wit, col_spa, _ = self.display.get_board_display_dimensions()

        chosen_x = floor((_disX - pad) / (col_wit + col_spa))
        chosen_y = floor((_disY - pad) / (col_wit + col_spa))

        board = self.get_board()
        chosen_space = board.get_chosen_grid_space(chosen_x, chosen_y)

        return chosen_space

    def setup_player(self, chosen_cell: Space | list[int]):
        if not self.IS_NUM:
            x = chosen_cell.getX()
            y = chosen_cell.getY()
        else:
            x = chosen_cell[0]
            y = chosen_cell[1]
        middle_spot = self.display.get_selected_display(x, y)
        added_player_index = self.Game.get_player_at_spot(x, y)
        added_player = self.Game.get_player_at_index(added_player_index)
        if not self.IS_NUM:
            current_display = added_player.get_display(middle_spot.getX(), middle_spot.getY())
        else:
            player_object = Player(added_player[0], added_player[1], added_player[2])
            current_display = player_object.get_display(middle_spot.getX(), middle_spot.getY())
        self.display.add_player_display(current_display)

    def setup_game(self, is_hash=False):
        """
        Will ask the player to select where on the screen, they would
        like their player piece to be. It will do this for all pieces,
        according to the order of determined by the game object.
        """
        win = self.get_window()

        pieces = self.Game.get_order()
        for i in range(len(pieces)):
            message = "Player " + str(pieces[i]) + ", select position for piece: "
            self.display.set_display_message(message)
            ## Loops until all characters are validly placed
            while True:
                chosen_cell = self.ask_for_grid_point()
                ## Checks if picked spot is valid
                if self.Game.pick_player_spot(chosen_cell, pieces[i]):
                    self.setup_player(chosen_cell)
                    player_displays = self.display.get_player_displays()
                    player_displays.__getitem__(i).draw(win)
                    break
                else:
                    continue

    def start_game(self):
        """
        Runs the game.
        Assumes that functions, setup and setup_game have already been called.

        Every 'While' loop that always is true is meant as a 'do while'
        loop that checks loops until the player gives a vaild input.

        First for loops through players to simulate taking turns.

        """
        current_board = self.Game.get_board()

        self.display.setup(current_board)
        self.setup_game()

        num_count = 1
        while True:
            # Current picked player number
            picked_player = -1
            num_players = floor(len(self.Game.get_order()) / 2)
            for i in range(num_players):
                if not self.AI or (self.AI and i + 1 == 1):
                    while True:
                        self.display.set_display_message("Player " + str(i + 1) + ", pick a piece.")
                        chosen_point = self.ask_for_grid_point()
                        if current_board.valid_player_select(chosen_point, i + 1):
                            ## Successfully chosen a player
                            if not self.IS_NUM:
                                selected_x = chosen_point.getX()
                                selected_y = chosen_point.getY()
                            else:
                                selected_x = chosen_point[0]
                                selected_y = chosen_point[1]
                            # chosen_player_piece: Space | list[int] = current_board.get_chosen_grid_space(selected_x, selected_y)

                            picked_player = self.Game.get_player_at_spot(selected_x, selected_y)
                            break

                    move_options = self.Game.get_move_spots(picked_player)
                    while True:
                        self.display.set_display_message("Move selected piece.")
                        picked_location = self.ask_for_grid_point()
                        print(picked_location)
                        if self.Game.spot_in_list(picked_location, move_options):
                            self.Game.move_player(picked_player, picked_location)
                            if not self.IS_NUM:
                                x = picked_location.getX()
                                y = picked_location.getY()
                            else:
                                x = picked_location[0]
                                y = picked_location[1]
                            self.display.update_player_display(picked_player, x, y)
                            break

                    build_options = self.Game.get_build_spots(picked_player)
                    while True:
                        self.display.set_display_message("Build around selected piece.")
                        picked_location = self.ask_for_grid_point()
                        if self.Game.spot_in_list(picked_location, build_options):
                            self.Game.build_at_spot(picked_location)
                            if not self.IS_NUM:
                                x = picked_location.getX()
                                y = picked_location.getY()
                            else:
                                x = picked_location[0]
                                y = picked_location[1]
                            self.display.update_block_display(x, y, current_board)
                            break

                    if self.AI:
                        start_time = time.time()
                        num_count += 1
                        turn = self.Game.AI_Turn()
                        if turn.get_move() == None:
                            self.Game.update_game(False)
                            break
                        piece = turn.get_piece()
                        p_ind = self.Game.get_player_at_spot(piece.getX(), piece.getY())
                        m_sp = turn.get_move()
                        self.Game.move_player(p_ind, m_sp)
                        self.display.update_player_display(p_ind, m_sp.getX(), m_sp.getY())
                        b_sp = turn.get_build()
                        self.Game.build_at_spot(b_sp)
                        self.display.update_block_display(b_sp.getX(), b_sp.getY(), current_board)
                        print("--- %s seconds ---" % (time.time() - start_time), 2)
                        continue

            current_player = self.Game.get_player_at_index(picked_player)

            if (self.IS_NUM and current_player[3] == 3) or (not self.IS_NUM and current_player.get_level() == 3):
                break

            num_count += 1


        print("game over")

    def next_turn(self, _dis_x, _dis_y, ai_on = False):
        """
        The next step in the game will happen given the inputted spot.
        Depends on the boolean fields for determining the turn order.
        :param _dis_x, _dis_y: Display coordinates that is the user selection.
        :return: Boolean. False for game over. True for continue.
        """
        if ai_on:
            print("Test")
            return

        spot = self.convert_display_to_grid(_dis_x, _dis_y)

        PICKED_PLAYER = self.Game.get_picked_player()
        PLAYER_TURN = self.Game.get_player_turn()
        MOVE = self.Game.get_move()
        BUILD = self.Game.get_build()

        current_board = self.Game.get_board()
        valid_select = current_board.space_on_board(spot.getX(), spot.getY())

        if not valid_select:
            return True

        spot = self.convert_display_on_grid(_dis_x, _dis_y)

        if not MOVE and not BUILD:
            ### Player piece select
            if self.Game.pick_piece_turn(spot):
                self.set_message("Move selected piece.")

        elif MOVE:
            ### Movement select
            if self.Game.move_piece_turn(spot):
                self.Game.move_player(PICKED_PLAYER, spot)
                self.update_player_display(PICKED_PLAYER, spot)
                self.set_message("Build around selected piece.")
            #self.window.update()


        elif not self.Game.game_state:
            self.set_message("Game over")
            return False

        elif BUILD:
            ### Build select
            if self.Game.build_piece_turn(spot):
                self.Game.build_at_spot(spot)
                self.update_block_display(spot)
                self.set_message("Player " + str(3 -PLAYER_TURN) + ", pick a piece.")

        return True

#########
    def next_turn_hash(self, _dis_x, _dis_y):
        """
        The next step in the game will happen given the inputted spot.
        Depends on the boolean fields for determining the turn order.
        :param _dis_x, _dis_y: Display coordinates that is the user selection.
        :return: Boolean. False for game over. True for continue.
        """
        spot = self.convert_display_to_grid(_dis_x, _dis_y)

        PICKED_PLAYER = self.Game.get_picked_player()
        PLAYER_TURN = self.Game.get_player_turn()
        MOVE = self.Game.get_move()
        BUILD = self.Game.get_build()

        current_board = self.Game.get_hashboard()
        valid_select = current_board.space_on_board(spot.getX(), spot.getY())

        if not valid_select:
            return True

        spot = self.convert_display_on_grid(_dis_x, _dis_y)

        if not MOVE and not BUILD:
            ### Player piece select
            if self.Game.pick_piece_turn_hash(spot):
                self.set_message("Move selected piece.")

        elif MOVE:
            ### Movement select
            if self.Game.move_piece_turn(spot):
                self.Game.move_player(PICKED_PLAYER, spot)
                self.update_player_display(PICKED_PLAYER, spot)
                self.set_message("Build around selected piece.")
            #self.window.update()


        elif not self.Game.game_state:
            self.set_message("Game over")
            return False

        elif BUILD:
            ### Build select
            if self.Game.build_piece_turn(spot):
                self.Game.build_at_spot(spot)
                self.update_block_display(spot)
                self.set_message("Player " + str(3 -PLAYER_TURN) + ", pick a piece.")

        return True
############
