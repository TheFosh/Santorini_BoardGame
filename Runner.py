########################################
##### MAIN FILE FOR RUNNING SYSTEM #####
########################################
### Author: Jake Swanson
from graphics import GraphWin

from GUI import GUI

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
WIDTH_OFFSET = 50
BOARD_CELL_COUNT = 5

GAME_GUI = GUI(SCREEN_HEIGHT, SCREEN_WIDTH, WIDTH_OFFSET, BOARD_CELL_COUNT)

def main():
    GAME_GUI.setup()
    GAME_GUI.setup_game()
    ##GAME_GUI.start_game()

    win = GAME_GUI.get_window()
    game_state = True
    while game_state:
        mouse = win.checkMouse()
        if mouse != None:
            mouse.draw(win)
            ### GAME_NEXT_TURN_METHOD(mouse) ###
            game_state = GAME_GUI.next_turn(mouse.getX(), mouse.getY())

        ### AI_STEP_METHOD(Game.Board)

    while True:
        continue
main()