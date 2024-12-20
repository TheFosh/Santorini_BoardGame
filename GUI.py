## Object for setting up the Graphical User Interface ##
########################################################
## Author: Jake Swanson
from math import floor
from Game import Game
from graphics import *
from GameObjects.Board import Board


class GUI:
    def __init__(self, _height, _width, _off):
        self.Game = Game()
        self.Board = Board(_width, _height)
        self.screen_height = _height
        self.screen_width = _width
        self.screen_offset = _off
        self.board_padding = 30
        self.window = GraphWin("Santorini", _width, _height + _off)

    def get_window(self):
        return self.window

    def get_screen_width(self):
        return self.screen_width

    def get_screen_height(self):
        return self.screen_height

    def setup(self):
        win = self.window
        # Background set to a nice blue
        win.setBackground(color_rgb(108, 158, 240))

        win = self.Board.get_display(self.get_screen_width(), self.get_screen_height(), win)

        ## Setting and returning the new window to the current one
        self.window = win
        return self.get_window()

    def start_game(self):
        win = self.get_window()

        text_point = Point(self.screen_width / 2, self.screen_height)
        instruction_message = ""
        instruction_display = Text(text_point, instruction_message)
        instruction_display.draw(win)

        pieces = self.Game.get_players()
        for i in range(len(pieces)):
            instruction_message = "Player " + str(pieces[i]) + ", select position for piece: "
            instruction_display.setText(instruction_message)

            while True:
                mouse = win.getMouse()
                chosen_cell = self.Board.validate_board_space(mouse)

                if self.Board.valid_for_player_start(chosen_cell.getX(), chosen_cell.getY()):
                    break


