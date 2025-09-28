import copy
from math import floor

from GameObjects.Board import Board
from graphics import *

from GameObjects.Player import Player
from GameObjects.Space import Space
from GameObjects.Turn import Turn


class BoardDisplay:
        def __init__(self, _height, _width, _off, _cell_num, ai_on=False, _is_hash=False):

            self.IS_HASH: bool = _is_hash
            self.AI: bool = ai_on

            self.screen_height: int = _height
            self.screen_width: int = _width
            self.screen_offset: int = _off
            self.window: GraphWin | None = None

            self.COLUMN_WIDTH: int = 10
            self.BOARD_PADDING: int = 30
            self.board_dimensions: int = _width - 2 * self.BOARD_PADDING
            self.column_spacing: int = (self.board_dimensions - ((_cell_num + 1) * self.COLUMN_WIDTH)) / _cell_num

            text_point: Point = Point(self.screen_width / 2, self.screen_height + self.BOARD_PADDING / 2)
            self.instruction_display: Text = Text(text_point, "")
            self.player_displays: list[Circle] = []
            self.block_displays: list[Rectangle] = []

        ########################################
        ########### GETTERS & SETTERS ##########
        def get_window(self):
            return self.window

        def get_screen_width(self):
            return self.screen_width

        def get_screen_height(self):
            return self.screen_height

        def get_selected_display(self, cord_spot: Space | list[int]):
            """
            Converts given grid coordinates into display coordinates.
            Display coordinates should be centered in the chosen cell.
            """
            display_x_cord = self.BOARD_PADDING + self.COLUMN_WIDTH + self.column_spacing / 2 + cord_spot.getX() * (
                    self.COLUMN_WIDTH + self.column_spacing)
            display_y_cord = self.BOARD_PADDING + self.COLUMN_WIDTH + self.column_spacing / 2 + cord_spot.getY() * (
                    self.COLUMN_WIDTH + self.column_spacing)

            return Space(display_x_cord, display_y_cord)

        ########################################

        def setup(self, current_board: Board):
            self.window = GraphWin("Santorini", self.screen_width + self.screen_offset, self.screen_height)
            win = self.get_window()
            # Background set to a nice blue
            win.setBackground(color_rgb(108, 158, 240))

            # Displaying the board relative to the right side of the screen
            ul_board = Point(0 + self.BOARD_PADDING, self.BOARD_PADDING)
            br_board = Point(self.screen_width - self.BOARD_PADDING, self.screen_height - self.BOARD_PADDING)

            display_board = Rectangle(ul_board, br_board)

            display_board.setFill(color_rgb(81, 237, 94))

            display_board.draw(win)

            # Displaying the grid of cells on the board
            cell_per_row = current_board.get_dimensions()

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

            ## Makes blocks that are located on the board
            pow(current_board.get_dimensions(), 2)
            for i in range(25):
                x_point_calculation = self.BOARD_PADDING + self.COLUMN_WIDTH + (
                            self.COLUMN_WIDTH * int(i % 5) + self.column_spacing * int(i % 5))
                y_point_calculation = self.BOARD_PADDING + self.COLUMN_WIDTH + (
                            self.COLUMN_WIDTH * int(i / 5) + self.column_spacing * int(i / 5))
                top_left_point = Point(x_point_calculation, y_point_calculation)
                bottom_left_point = Point(x_point_calculation + self.column_spacing,
                                          y_point_calculation + self.column_spacing)
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
                vertical_pos = self.BOARD_PADDING + self.COLUMN_WIDTH + self.column_spacing / 2 + (
                            self.COLUMN_WIDTH + self.column_spacing) * i
                text_point = Point(self.BOARD_PADDING / 2, vertical_pos)
                label_iteration = Text(text_point, str(4 - i + 1))
                label_iteration.draw(win)

            ### Horizontally positioned letters
            for i in range(cell_per_row):
                horizontal_pos = self.BOARD_PADDING + self.COLUMN_WIDTH + self.column_spacing / 2 + (
                            self.COLUMN_WIDTH + self.column_spacing) * i
                text_point = Point(horizontal_pos, self.screen_height - self.BOARD_PADDING / 2)
                label_iteration = Text(text_point, chr(ord('a') + i))
                label_iteration.draw(win)

            ## Setting and returning the new window to the current one
            self.window = win
            return self.get_window()

        def setup_game(self, game_info, is_hash=False):
            """
            Will ask the player to select where on the screen, they would
            like their player piece to be. It will do this for all pieces,
            according to the order of determined by the game object.
            """
            win = self.get_window()
            self.instruction_display.draw(win)

            pieces = game_info.get_order()
            for i in range(len(pieces)):
                message = "Player " + str(pieces[i]) + ", select position for piece: "
                self.instruction_display.setText(message)
                ## Loops until all characters are validly placed
                while True:
                    chosen_cell = self.ask_for_grid_point(win)
                    ## Checks if picked spot is valid
                    if game_info.pick_player_spot(chosen_cell, pieces[i]):
                        self.setup_player(chosen_cell, game_info)
                        print(self.player_displays)
                        self.player_displays.__getitem__(i).draw(win)
                        break
                    else:
                        continue

        def start_game(self, game_info):
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
                num_players = floor(len(game_info.get_order()) / 2)
                for i in range(num_players):
                    if not self.AI or (self.AI and i + 1 == 1):
                        current_board = game_info.get_board()
                        while True:
                            self.set_message("Player " + str(i + 1) + ", pick a piece.")
                            chosen_point = self.ask_for_grid_point(self.get_window())
                            if current_board.valid_player_select(chosen_point, i + 1):
                                ## Successfully chosen a player
                                chosen_player_piece = current_board.get_chosen_grid_space(chosen_point)
                                picked_player = game_info.get_player_at_spot(chosen_player_piece)
                                break

                        move_options = game_info.get_move_spots(picked_player)
                        while True:
                            self.set_message("Move selected piece.")
                            picked_location = self.ask_for_grid_point(self.get_window())
                            if game_info.spot_in_list(picked_location, move_options):
                                game_info.move_player(picked_player, picked_location)
                                self.update_player_display(picked_player, picked_location)
                                break

                        build_options = game_info.get_build_spots(picked_player)
                        while True:
                            self.set_message("Build around selected piece.")
                            picked_location = self.ask_for_grid_point(self.get_window())
                            if game_info.spot_in_list(picked_location, build_options):
                                game_info.build_at_spot(picked_location)
                                self.update_block_display(picked_location, game_info.get_board())
                                break

                        if self.AI:
                            num_count += 1
                            turn = game_info.AI_Turn()
                            p_ind = game_info.get_player_at_spot(turn.get_piece())
                            m_sp = turn.get_move()
                            game_info.move_player(p_ind, m_sp)
                            self.update_player_display(p_ind, m_sp)
                            b_sp = turn.get_build()
                            game_info.build_at_spot(b_sp)
                            self.update_block_display(b_sp, game_info.get_board())
                            continue

                current_player = game_info.get_player_at_index(picked_player)

                if current_player.get_level() == 3:
                    break

                num_count += 1

            print("game over")

        ############

        # def display_artificial_game(self, new_turn, given_game) -> None:
        #     given_game.simulate_turn(new_turn)
        #     self.window = GraphWin("Santorini", self.screen_width + self.screen_offset, self.screen_height + self.screen_offset)
        #     self.setup(copy.deepcopy(given_game.get_board()))
        #     self.update_board_display(given_game)
        #     win = self.get_window()
        #     win.getMouse()
        #     self.window.close()

        def update_board_display(self, given_game):
            board = copy.deepcopy(given_game.get_board())
            players = board.get_all_players()
            self.display_new_players(players, given_game)
            blocks = board.get_all_blocks()
            self.display_new_blocks(blocks, board)

        def display_new_players(self, players: list[Space], given_game) -> None:
            for p in players:
                self.setup_player(p, given_game)

        def display_new_blocks(self, blocks: list[Space], given_board) -> None:
            for b in blocks:
                self.update_block_display(b, given_board)
