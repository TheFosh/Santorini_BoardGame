########################################
##### MAIN FILE FOR RUNNING SYSTEM #####
########################################
### Author: Jake Swanson

from graphics import *

from GUI import GUI
from Game import Game

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
WIDTH_OFFSET = 50
BOARD_CELL_COUNT = 5

GAME_GUI = GUI(SCREEN_HEIGHT, SCREEN_WIDTH, WIDTH_OFFSET, BOARD_CELL_COUNT)

def main():
    GAME_GUI.setup()
    GAME_GUI.setup_game()
    GAME_GUI.start_game(2) # Gives number of players

    win = GAME_GUI.get_window()

    while True:
        mouse = win.checkMouse()
        if mouse != None:
            mouse.draw(win)
main()