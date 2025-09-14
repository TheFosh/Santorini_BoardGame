########################################
##### MAIN FILE FOR RUNNING SYSTEM #####
########################################
### Author: Jake Swanson
import copy
import time

from graphics import GraphWin

from GUI import GUI
from GameObjects.Space import Space

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
WIDTH_OFFSET = 50
BOARD_CELL_COUNT = 5

IS_HASH = False
IS_AI = True

GAME_GUI = GUI(SCREEN_HEIGHT, SCREEN_WIDTH, WIDTH_OFFSET, BOARD_CELL_COUNT, ai_on=IS_AI, _is_hash= IS_HASH)

def main():
    GAME_GUI.setup()
    GAME_GUI.setup_game(is_hash=IS_HASH)

    win = GAME_GUI.get_window()

    GAME_GUI.start_game()



    # while True:
    #     mouse = win.checkMouse()
    #     if mouse != None:
    #         GAME_GUI.next_turn(mouse.getX(), mouse.getY(), ai_on=True)
    #         win.update()
    #         mouse.draw(win)
    #
    #     #GAME_GUI.update_ai()

    while True:
        continue
main()