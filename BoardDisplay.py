import copy
from ctypes import windll
from math import floor
from typing import Tuple

from GameObjects.Board import Board
from graphics import *

from GameObjects.HashableBoard import Hashboard
from GameObjects.Player import Player
from GameObjects.Space import Space
from GameObjects.Turn import Turn


class BoardDisplay:
        def __init__(self, _height, _width, _off, _cell_num, ai_on=False, _is_num=False):

            self._IS_NUM: bool = _is_num
            self.AI: bool = ai_on

            self.column_count = _cell_num

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

        def get_selected_display(self, chosen_x: int, chosen_y: int):
            """
            Converts given grid coordinates into display coordinates.
            Display coordinates should be centered in the chosen cell.
            """
            display_x_cord = self.BOARD_PADDING + self.COLUMN_WIDTH + self.column_spacing / 2 + chosen_x * (
                    self.COLUMN_WIDTH + self.column_spacing)
            display_y_cord = self.BOARD_PADDING + self.COLUMN_WIDTH + self.column_spacing / 2 + chosen_y * (
                    self.COLUMN_WIDTH + self.column_spacing)

            return Space(display_x_cord, display_y_cord)

        def get_board_display_dimensions(self) -> Tuple[int, int, int, int]:
            return (self.BOARD_PADDING,
                    self.COLUMN_WIDTH,
                    self.column_spacing,
                    self.column_count)

        def get_player_displays(self):
            return self.player_displays

        def set_display_message(self, message:str):
            self.instruction_display.setText(message)

        def set_player_displays(self, given_board: Board):
            players = given_board.get_all_players()
            for p in players:
                display_point = self.get_selected_display(p)
                display = p.get_display(display_point)
                self.player_displays.append(display)
                display.draw(self.window)

        ########################################

        def setup(self, current_board: Board):
            self.window = GraphWin("Santorini", self.screen_width + self.screen_offset, self.screen_height + self.screen_offset)
            win = self.get_window()
            # Background set to a nice blue
            win.setBackground(color_rgb(108, 158, 240))

            text_point: Point = Point(self.screen_width / 2, self.screen_height + self.BOARD_PADDING / 2)
            self.instruction_display: Text = Text(text_point, "")
            self.instruction_display.draw(win)

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

        ############

        def display_artificial_game(self, given_board) -> None:
            board_copy = copy.deepcopy(given_board)
            self.setup(board_copy)
            self.set_player_displays(board_copy)
            self.update_board_display(board_copy)
            win = self.get_window()
            win.getMouse()
            self.window.close()

        def update_player_display(self, player_index, x, y):
            player_display = self.player_displays[player_index].getCenter()

            old_display_x = player_display.getX()
            old_display_y = player_display.getY()

            new_display_x = self.get_selected_display(x,y).getX()
            new_display_y = self.get_selected_display(x,y).getY()

            self.player_displays[player_index].move(new_display_x - old_display_x, new_display_y - old_display_y)

        def update_block_display(self, x, y, current_board: Board | Hashboard):
            selected_space: Space | list[int] = current_board.get_all_data(x,y)
            block_index = y * 5 + x
            if isinstance(current_board, Board):
                spot_level = selected_space.get_level()
            else:
                spot_level = selected_space[3]
            if spot_level == 0:
                self.block_displays[block_index].undraw()

            elif 0 < spot_level < 4:
                block_color = int(255 / (4 - spot_level))
                self.block_displays[block_index].setFill(color_rgb(block_color, block_color, block_color))

            else:
                self.block_displays[block_index].setFill(color="blue")

        def add_player_display(self, pd: Circle):
            self.player_displays.append(pd)

        def update_board_display(self, given_board):
            new_board:Board = copy.deepcopy(given_board)
            blocks = new_board.get_all_blocks()
            self.display_new_blocks(blocks, new_board)

        def display_new_players(self, new_p, old_p, game_info):
            for i in range(len(new_p)):
                np_ind = game_info.get_player_at_spot(new_p[i])
                self.update_player_display(np_ind, old_p[i])

        def display_new_blocks(self, blocks: list[Space], given_board) -> None:
            for b in blocks:
                self.update_block_display(b, given_board)
