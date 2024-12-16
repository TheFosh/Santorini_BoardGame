########################################
##### MAIN FILE FOR RUNNING SYSTEM #####
########################################
### Author: Jake Swanson

from graphics import *

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

WIDTH_OFFSET = 300

def main():

    win = GraphWin("Santorini", SCREEN_WIDTH + WIDTH_OFFSET, SCREEN_HEIGHT)

    while True:
        mouse = win.checkMouse()
        if mouse != None:
            mouse.draw(win)
main()