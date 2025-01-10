########################################
##### MAIN FILE FOR RUNNING SYSTEM #####
########################################
### Author: Jake Swanson
from tkinter import Radiobutton

from graphics import GraphWin

from ArtificialPlayer import GameEvaluator
from GUI import GUI
from RandomPlayer import RandomPlayer

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
WIDTH_OFFSET = 50
BOARD_CELL_COUNT = 5

GAME_GUI = GUI(SCREEN_HEIGHT, SCREEN_WIDTH, WIDTH_OFFSET, BOARD_CELL_COUNT)

random_player = RandomPlayer(GAME_GUI.Game, 2)
Score_Predictor = GameEvaluator(2, GAME_GUI.get_board(), 2)

def main_player_turn(win):
    game_state = True
    current_player = GAME_GUI.Game.get_player_turn()
    while current_player == 1:
        mouse = win.getMouse()
        game_state = GAME_GUI.next_turn(mouse.getX(), mouse.getY())
        current_player = GAME_GUI.Game.get_player_turn()

    return game_state


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