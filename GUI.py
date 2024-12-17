## Object for setting up the Graphical User Interface ##
########################################################
## Author: Jake Swanson
from Game import Game
from graphics import *

class GUI:
    def __init__(self, _height, _width, _off):
        self.Game = Game()
        self.screen_height = _height
        self.screen_width = _width
        self.screen_offset = _off
        self.window = GraphWin("Santorini", _width + _off, _height)

    def get_window(self):
        return self.window

    def setup(self):
        win = self.window
        ## Background set to a nice blue
        win.setBackground(color_rgb(108, 158, 240))

        ## Displaying the board relative to the right side of the screen
        BOARD_PADDING = 30
        board_dimension = self.screen_width - 2 * BOARD_PADDING

        ul_board = Point(0 + BOARD_PADDING, 0+BOARD_PADDING)
        br_board = Point(self.screen_width - BOARD_PADDING, self.screen_height - BOARD_PADDING)

        display_board = Rectangle(ul_board, br_board)

        display_board.setFill(color_rgb(81, 237, 94))
        display_board.setOutline(color="white")

        display_board.draw(win)

        ## Displaying the grid of cells on the board
        GRID_COUNT = 6
        COLUMN_WIDTH = 10
        column_spacing = (board_dimension - (GRID_COUNT * COLUMN_WIDTH)) / (GRID_COUNT-1)


        horizontal_grid = [Rectangle
                                (Point(0 + BOARD_PADDING,
                                       column_spacing * i + COLUMN_WIDTH * i + BOARD_PADDING),
                                Point(self.screen_width - BOARD_PADDING,
                                      column_spacing * i + COLUMN_WIDTH * i + COLUMN_WIDTH + BOARD_PADDING))
                         for i in range(GRID_COUNT)]
        vertical_grid = [Rectangle
                            (Point(column_spacing * i + COLUMN_WIDTH * i + BOARD_PADDING,
                                   0 + BOARD_PADDING),
                             Point(column_spacing * i + COLUMN_WIDTH * i + COLUMN_WIDTH + BOARD_PADDING,
                                   self.screen_height - BOARD_PADDING)
                            )

                         for i in range(GRID_COUNT)]

        for i in range(GRID_COUNT):
            v_current_rec = vertical_grid[i]
            h_current_rec = horizontal_grid[i]

            v_current_rec.setFill(color="white")
            h_current_rec.setFill(color="white")

            v_current_rec.draw(win)
            h_current_rec.draw(win)

        ## Setting and returning the new window to the current one
        self.window = win
        return self.get_window()