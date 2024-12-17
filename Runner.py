########################################
##### MAIN FILE FOR RUNNING SYSTEM #####
########################################
### Author: Jake Swanson

from graphics import *

from GUI import GUI

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

WIDTH_OFFSET = 200

def main():
    my_GUI = GUI(SCREEN_HEIGHT, SCREEN_WIDTH, WIDTH_OFFSET)
    my_GUI.setup()

    win = my_GUI.get_window()
    while True:
        mouse = win.checkMouse()
        if mouse != None:
            mouse.draw(win)
main()