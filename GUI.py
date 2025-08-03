## Object for setting up the Graphical User Interface ##
########################################################
## Author: Jake Swanson
import copy
from math import floor

from ArtificialPlayer import CPU
from GameObjects.Game import Game
from graphics import *

from GameObjects.NumGame import NumGame
from GameObjects.Space import Space


class GUI:
    def __init__(self, _height, _width, _off, _cell_num, ai_on = False, _is_hash = False):
        if _is_hash:
            self.Game = NumGame(_cell_num, ai_on = ai_on)
        else:
            self.Game = Game(_cell_num, is_hash=_is_hash)

        self.IS_HASH = _is_hash
        self.AI = ai_on
        self.game_ai = CPU(4)

        self.screen_height = _height
        self.screen_width = _width
        self.screen_offset = _off
        self.window = GraphWin("Santorini", _width + _off, _height + _off)

        self.COLUMN_WIDTH = 10
        self.BOARD_PADDING = 30
        self.board_dimensions = _width - 2 * self.BOARD_PADDING
        self.column_spacing = (self.board_dimensions - ((_cell_num + 1) * self.COLUMN_WIDTH)) / _cell_num

        text_point = Point(self.screen_width / 2, self.screen_height + self.BOARD_PADDING / 2)
        self.instruction_display = Text(text_point, "")
        self.player_displays = []
        self.block_displays = []

        self.evaluation_displays = []
########################################
########### GETTERS & SETTERS ##########
    def get_window(self):
        return self.window

    def get_screen_width(self):
        return self.screen_width

    def get_screen_height(self):
        return self.screen_height

    def get_selected_display(self, cord_spot):
        """
        Converts given grid coordinates into display coordinates.
        Display coordinates should be centered in the chosen cell.
        """
        display_x_cord = self.BOARD_PADDING + self.COLUMN_WIDTH + self.column_spacing/ 2 + cord_spot.getX() * (self.COLUMN_WIDTH + self.column_spacing)
        display_y_cord = self.BOARD_PADDING + self.COLUMN_WIDTH + self.column_spacing/ 2 + cord_spot.getY() * (self.COLUMN_WIDTH + self.column_spacing)
        return Space(display_x_cord, display_y_cord)

    def get_board(self):
        return self.Game.get_board()

########################################

    def setup(self):
        win = self.window
        # Background set to a nice blue
        win.setBackground(color_rgb(108, 158, 240))

        # Displaying the board relative to the right side of the screen
        ul_board = Point(0 + self.BOARD_PADDING, self.BOARD_PADDING)
        br_board = Point(self.screen_width - self.BOARD_PADDING, self.screen_height - self.BOARD_PADDING)

        display_board = Rectangle(ul_board, br_board)

        display_board.setFill(color_rgb(81, 237, 94))

        display_board.draw(win)

        # Displaying the grid of cells on the board
        current_board = self.Game.get_board()
        cell_per_row = current_board.get_width_height()

        ## For the bars that are tall. Horizontal refers to how they are spaced.
        horizontal_grid = [Rectangle
                           (Point(0 + self.BOARD_PADDING,
                                  self.column_spacing * i + self.COLUMN_WIDTH * i + self.BOARD_PADDING),
                            Point(self.screen_width - self.BOARD_PADDING,
                                  self.column_spacing * i + self.COLUMN_WIDTH * i + self.COLUMN_WIDTH + self.BOARD_PADDING))
                           for i in range(cell_per_row + 1)]

        ## For the bars that are long. Vertical refers to how they are spaced.
        vertical_grid = [Rectangle
                         (Point(self.column_spacing * i + self.COLUMN_WIDTH * i + self.BOARD_PADDING,
                                0 + self.BOARD_PADDING),
                          Point(
                              self.column_spacing * i + self.COLUMN_WIDTH * i + self.COLUMN_WIDTH + self.BOARD_PADDING,
                              self.screen_height - self.BOARD_PADDING)
                          )

                         for i in range(cell_per_row + 1)]
        tempBoard = self.Game.get_board()


        ## Makes blocks that are located on the board
        pow(tempBoard.get_width_height(), 2)
        for i in range(25):
            x_point_calculation = self.BOARD_PADDING + self.COLUMN_WIDTH +(self.COLUMN_WIDTH * int(i % 5) + self.column_spacing * int(i % 5))
            y_point_calculation = self.BOARD_PADDING + self.COLUMN_WIDTH +(self.COLUMN_WIDTH * int(i / 5) + self.column_spacing * int(i / 5))
            top_left_point = Point(x_point_calculation, y_point_calculation)
            bottom_left_point = Point(x_point_calculation + self.column_spacing, y_point_calculation + self.column_spacing)
            self.block_displays.append(Rectangle(top_left_point, bottom_left_point))
            current_box = self.block_displays[i]
            current_box.setFill(color="Green")
            current_box.draw(win)


        ## Drawing all bars
        for i in range(cell_per_row + 1):
            v_current_rec = vertical_grid[i]
            h_current_rec = horizontal_grid[i]

            v_current_rec.setFill(color="white")
            h_current_rec.setFill(color="white")

            v_current_rec.draw(win)
            h_current_rec.draw(win)

        ## Drawing on the text labels for the cells
        ### Vertically positioned numbers
        for i in range(cell_per_row):
            vertical_pos =  self.BOARD_PADDING + self.COLUMN_WIDTH + self.column_spacing/2 + (self.COLUMN_WIDTH + self.column_spacing) * i
            text_point = Point(self.BOARD_PADDING / 2, vertical_pos)
            label_iteration = Text(text_point, str(4 - i +1))
            label_iteration.draw(win)

        ### Horizontally positioned letters
        for i in range(cell_per_row):
            horizontal_pos =  self.BOARD_PADDING + self.COLUMN_WIDTH + self.column_spacing/2 + (self.COLUMN_WIDTH + self.column_spacing) * i
            text_point = Point(horizontal_pos, self.screen_height - self.BOARD_PADDING/2)
            label_iteration = Text(text_point, chr(ord('a') +i))
            label_iteration.draw(win)

        ## Setting and returning the new window to the current one
        self.window = win
        return self.get_window()

    def setup_game(self, is_hash = False):
        """
        Will ask the player to select where on the screen, they would
        like their player piece to be. It will do this for all pieces,
        according to the order of determined by the game object.
        """
        win = self.get_window()
        self.instruction_display.draw(win)

        pieces = self.Game.get_order()
        for i in range(len(pieces)):
            message = "Player " + str(pieces[i]) + ", select position for piece: "
            self.instruction_display.setText(message)
            ## Loops until all characters are validly placed
            while True:
                chosen_cell = self.ask_for_grid_point(win)
                if not is_hash:
                    ## Checks if picked spot is valid
                    if self.Game.pick_player_spot(chosen_cell, pieces[i]):
                        middle_spot = self.get_selected_display(chosen_cell)
                        added_player_index = self.Game.get_player_at_spot(chosen_cell)
                        added_player = self.Game.get_player_at_index(added_player_index)
                        current_display = added_player.get_display(middle_spot)
                        self.player_displays.append(current_display)

                        self.player_displays.__getitem__(i).draw(win)
                        break
                    else:
                        continue
                else:
                    if self.Game.pick_player_spot(chosen_cell, pieces[i]):
                        middle_spot = self.get_selected_display(chosen_cell)
                        added_player_index = self.Game.get_player_at_spot(chosen_cell)
                        added_player = self.Game.get_player_at_index(added_player_index)
                        current_display = added_player.get_display(middle_spot)
                        self.player_displays.append(current_display)

                        self.player_displays.__getitem__(i).draw(win)
                        break
                    else:
                        continue

    def ask_for_grid_point(self, win) -> Space | float:
        mouse = win.getMouse()
        return self.convert_display_on_grid(mouse.getX(), mouse.getY())

    def convert_display_on_grid(self, _disX, _disY) -> Space:
        chosen_x = floor((_disX - self.BOARD_PADDING) / (self.COLUMN_WIDTH + self.column_spacing))
        chosen_y = floor((_disY - self.BOARD_PADDING) / (self.COLUMN_WIDTH + self.column_spacing))

        current_board = self.Game.get_board()
        tempSpace = Space(chosen_x,chosen_y)
        return current_board.get_chosen_grid_space(tempSpace)

    def convert_to_display(self, grid_spot):
        disX = grid_spot.getX() * (self.COLUMN_WIDTH + self.column_spacing) + self.BOARD_PADDING
        disY = grid_spot.getY() * (self.COLUMN_WIDTH + self.column_spacing) + self.BOARD_PADDING

        return Point(disX, disY)

    def convert_display_to_grid(self, _disX, _disY):
        chosen_x = floor((_disX - self.BOARD_PADDING) / (self.COLUMN_WIDTH + self.column_spacing))
        chosen_y = floor((_disY - self.BOARD_PADDING) / (self.COLUMN_WIDTH + self.column_spacing))

        return Space(chosen_x, chosen_y)

    def update_player_display(self, player_index, picked_location):
        player_display = self.player_displays[player_index].getCenter()
        old_display_x = player_display.getX()
        old_display_y = player_display.getY()
        new_display_x = self.get_selected_display(picked_location).getX()
        new_display_y = self.get_selected_display(picked_location).getY()
        self.player_displays[player_index].move(new_display_x - old_display_x, new_display_y - old_display_y)

    def update_block_display(self, picked_location):
        current_board = self.Game.get_board()
        selected_space = current_board.grid[picked_location.getX()][picked_location.getY()]
        block_index = picked_location.getY() * 5 + picked_location.getX()
        spot_level = selected_space.get_level()
        if spot_level == 0:
            self.block_displays[block_index].undraw()
        elif 0 < spot_level < 4:
            block_color = int(255/(4 - spot_level))
            self.block_displays[block_index].setFill(color_rgb(block_color, block_color, block_color))
        else:
            self.block_displays[block_index].setFill(color="blue")

    def set_message(self, message):
        self.instruction_display.setText(message)

    def start_game(self):
        """
        Runs the game.
        Assumes that functions, setup and setup_game have already been called.

        Every 'While' loop that always is true is meant as a 'do while'
        loop that checks loops until the player gives a vaild input.

        First for loops through players to simulate taking turns.

        """
        num_count = 1
        while True:
            # Current picked player number
            picked_player = -1
            num_players = floor(len(self.Game.get_order()) / 2)
            for i in range(num_players):
                if not self.AI or (self.AI and i + 1 == 1):
                    current_board = None
                    if not self.IS_HASH:
                        current_board = self.Game.get_board()
                    else:
                        current_board = self.Game.get_hashboard()
                    while True:
                        self.set_message("Player " + str(i + 1) + ", pick a piece.")
                        chosen_point = self.ask_for_grid_point(self.get_window())
                        if current_board.valid_player_select(chosen_point, i + 1):
                            ## Successfully chosen a player
                            chosen_player_piece = current_board.get_chosen_grid_space(chosen_point)
                            picked_player = self.Game.get_player_at_spot(chosen_player_piece)
                            break

                    move_options = self.Game.get_move_spots(picked_player)
                    while True:
                        self.set_message("Move selected piece.")
                        picked_location = self.ask_for_grid_point(self.get_window())
                        if self.Game.spot_in_list(picked_location, move_options):
                            self.Game.move_player(picked_player, picked_location)
                            self.update_player_display(picked_player, picked_location)
                            break

                    build_options = self.Game.get_build_spots(picked_player)
                    while True:
                        self.set_message("Build around selected piece.")
                        picked_location = self.ask_for_grid_point(self.get_window())
                        if self.Game.spot_in_list(picked_location, build_options):
                            self.Game.build_at_spot(picked_location)
                            self.update_block_display(picked_location)
                            break

                    if self.AI:
                        num_count += 1
                        turn = self.Game.AI_Turn(self.game_ai)
                        p_ind = self.Game.get_player_at_spot(turn.get_piece())
                        m_sp = turn.get_move()
                        self.Game.move_player(p_ind, m_sp)
                        self.update_player_display(p_ind, m_sp)
                        b_sp = turn.get_build()
                        self.Game.build_at_spot(b_sp)
                        self.update_block_display(b_sp)
                        continue

            current_player = self.Game.get_player_at_index(picked_player)

            if current_player.get_level() == 3:
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

    def update_ai(self):
        board_copy = copy.deepcopy(self.Game.get_board())

        print(self.game_ai.evaluate_board_step(board_copy))