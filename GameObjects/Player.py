## Object representing a player in the game ##
##############################################
## Author: Jake Swanson

from graphics import *
from GameObjects.Space import Space


class Player(Space):
    def __init__(self, _x, _y, _n, _l = 0):
        super().__init__(_x, _y)
        self.playerNum = _n
        self.level = _l

    def set_space(self, given_spot):
        self.x = given_spot.getX()
        self.y = given_spot.getY()

    def get_display(self, display_x, display_y):
        # Player will be discs of a certain color depending on the player num
        RADIUS = 30
        player_display = Circle(Point(display_x,display_y), RADIUS)

        if self.playerNum == 1:
            player_display.setFill(color="blue")
        if self.playerNum == 2:
            player_display.setFill(color="gray")

        return player_display

    def set_level(self, _level):
        self.level = _level