## Object for setting up the Graphical User Interface ##
########################################################
## Author: Jake Swanson
from math import floor
from Game import Game
from graphics import *

from GameObjects.Space import Space


class GUI:
    def __init__(self, _height, _width, _off, _cell_num):
        self.Game = Game(_width, _height, _cell_num)

        self.screen_height = _height
        self.screen_width = _width
        self.screen_offset = _off
        self.window = GraphWin("Santorini", _width, _height + _off)
        self.instruction_message = ""

        self.COLUMN_WIDTH = 10
        self.BOARD_PADDING = 30
        self.board_dimensions = _width - 2 * self.BOARD_PADDING
        self.column_spacing = (self.board_dimensions - ((_cell_num + 1) * self.COLUMN_WIDTH)) / _cell_num

        self.player_displays = []

########################################
########### GETTERS & SETTERS ##########
    def get_window(self):
        return self.window

    def get_screen_width(self):
        return self.screen_width

    def get_screen_height(self):
        return self.screen_height
########################################

    @staticmethod
    def get_player_display(space, label):
        # Player will be discs of a certain color depending on the player num
        RADIUS = 30
        player_display = Circle(Point(space.getX(), space.getY()), RADIUS)

        if label == 1:
            player_display.setFill(color="blue")
        if label == 2:
            player_display.setFill(color="gray")

        return player_display

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

        ## Drawing all bars
        for i in range(cell_per_row + 1):
            v_current_rec = vertical_grid[i]
            h_current_rec = horizontal_grid[i]

            v_current_rec.setFill(color="white")
            h_current_rec.setFill(color="white")

            v_current_rec.draw(win)
            h_current_rec.draw(win)

        ## Setting and returning the new window to the current one
        self.window = win
        return self.get_window()

    def setup_game(self):
        """
        Will ask the player to select where on the screen, they would
        like their player piece to be. It will do this for all pieces,
        according to the order of determined by the game object.
        """
        win = self.get_window()

        text_point = Point(self.screen_width / 2, self.screen_height)
        instruction_display = Text(text_point, self.instruction_message)
        instruction_display.draw(win)

        pieces = self.Game.get_order()
        for i in range(len(pieces)):
            self.instruction_message = "Player " + str(pieces[i]) + ", select position for piece: "
            instruction_display.setText(self.instruction_message)
            ## Loops until all characters are validly placed
            while True:
                chosen_cell = self.ask_for_grid_point(win)
                ## Checks if picked spot is valid
                if self.Game.pick_player_spot(chosen_cell, pieces[i]):
                    middle_spot = self.get_selected_display(chosen_cell)
                    player_display = self.get_player_display(middle_spot, pieces[i])
                    self.player_displays.append(player_display)
                    self.player_displays.__getitem__(i).draw(win)
                    break
                else:
                    continue

    def ask_for_grid_point(self, win):
        mouse = win.getMouse()
        return self.convert_display_to_grid(mouse)

    def convert_display_to_grid(self, selected_point):
        chosen_x = floor((selected_point.getX() - self.BOARD_PADDING) / (self.COLUMN_WIDTH + self.column_spacing))
        chosen_y = floor((selected_point.getY() - self.BOARD_PADDING) / (self.COLUMN_WIDTH + self.column_spacing))

        return Space(chosen_x, chosen_y)

    def get_selected_display(self, cord_spot):
        """
        Converts given grid coordinates into display coordinates.
        Display coordinates should be centered in the chosen cell.
        """
        display_x_cord = self.BOARD_PADDING + self.COLUMN_WIDTH + self.column_spacing/ 2 + cord_spot.getX() * (self.COLUMN_WIDTH + self.column_spacing)
        display_y_cord = self.BOARD_PADDING + self.COLUMN_WIDTH + self.column_spacing/ 2 + cord_spot.getY() * (self.COLUMN_WIDTH + self.column_spacing)
        return Space(display_x_cord, display_y_cord)

    def start_game(self, num_players):
        while True:
            for i in range(num_players):
                while True:
                    chosen_point = self.ask_for_grid_point(self.get_window())
                    if self.Board.valid_player_select(chosen_point, i + 1):
                        chosen_player_piece = self.Board.get_chosen_grid_space(chosen_point)
                        win = self.get_window()
                        picked_player = Player(chosen_player_piece.getX(), chosen_player_piece.getY(), i + 1)
                        TESTING_DISPLAY = picked_player.get_display()
                        TESTING_DISPLAY.setFill(color="red")

                        TESTING_DISPLAY.draw(win)

