## Object representing the board of spaces in a game ##
#######################################################
## Author: Jake Swanson
from math import floor

from graphics import *

from GameObjects.Space import Space

class Board:
    WIDTH = 5
    HEIGHT = 5
    COLUMN_WIDTH = 10
    BOARD_PADDING = 30

    def __init__(self, screen_w, screen_h):
        self.grid = [
                        [Space(i, j) for i in range(self.WIDTH)]
                        for j in range(self.HEIGHT)
                    ]

        self.board_dimensions = screen_w - 2 * self.BOARD_PADDING
        self.column_spacing = (self.board_dimensions - ((self.WIDTH + 1) * self.COLUMN_WIDTH)) / self.WIDTH

    def valid_for_player_start(self, _x, _y):
        return (self.WIDTH > _x >= 0 and
                self.HEIGHT > _y >= 0 and
                self.grid[_x][_y].playerNum == 0)

    def get_display(self, screen_w, screen_h, win):
        # Displaying the board relative to the right side of the screen

        ul_board = Point(0 + self.BOARD_PADDING, self.BOARD_PADDING)
        br_board = Point(screen_w - self.BOARD_PADDING, screen_h - self.BOARD_PADDING)

        display_board = Rectangle(ul_board, br_board)

        display_board.setFill(color_rgb(81, 237, 94))

        display_board.draw(win)

        # Displaying the grid of cells on the board

        ## For the bars that are tall. Horizontal refers to how they are spaced.
        horizontal_grid = [Rectangle
                           (Point(0 + self.BOARD_PADDING,
                                  self.column_spacing * i + self.COLUMN_WIDTH * i + self.BOARD_PADDING),
                            Point(screen_w - self.BOARD_PADDING,
                                  self.column_spacing * i + self.COLUMN_WIDTH * i + self.COLUMN_WIDTH + self.BOARD_PADDING))
                           for i in range(self.WIDTH + 1)]

        ## For the bars that are long. Vertical refers to how they are spaced.
        vertical_grid = [Rectangle
                         (Point(self.column_spacing * i + self.COLUMN_WIDTH * i + self.BOARD_PADDING,
                                0 + self.BOARD_PADDING),
                          Point(self.column_spacing * i + self.COLUMN_WIDTH * i + self.COLUMN_WIDTH + self.BOARD_PADDING,
                                screen_h - self.BOARD_PADDING)
                          )

                         for i in range(self.HEIGHT + 1)]

        ## Drawing all bars
        for i in range(self.WIDTH + 1):
            v_current_rec = vertical_grid[i]
            h_current_rec = horizontal_grid[i]

            v_current_rec.setFill(color="white")
            h_current_rec.setFill(color="white")

            v_current_rec.draw(win)
            h_current_rec.draw(win)

        return win

    def validate_board_space(self, selected_point):
        chosen_x = floor((selected_point.getX() - self.BOARD_PADDING) / (self.COLUMN_WIDTH + self.column_spacing))
        chosen_y = floor((selected_point.getY() - self.BOARD_PADDING) / (self.COLUMN_WIDTH + self.column_spacing))

        return Space(chosen_x, chosen_y)


    def get_selected_display(self, cord_spot):
        """Converts given grid coordinates into display coordinates."""
        display_x_cord = self.BOARD_PADDING + self.COLUMN_WIDTH + self.column_spacing/ 2 + cord_spot.getX() * (self.COLUMN_WIDTH + self.column_spacing)
        display_y_cord = self.BOARD_PADDING + self.COLUMN_WIDTH + self.column_spacing/ 2 + cord_spot.getY() * (self.COLUMN_WIDTH + self.column_spacing)
        return Space(display_x_cord, display_y_cord)