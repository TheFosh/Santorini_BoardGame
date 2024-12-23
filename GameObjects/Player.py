## Object representing a player in the game ##
##############################################
## Author: Jake Swanson
from graphics import *


class Player:
    def __init__(self, _x, _y, _l):
        self.x_cord = _x
        self.y_cord = _y
        self.label = _l

    ## Makes the display of a player as a circle

    def set_space(self, given_spot):
        self.x_cord = given_spot.getX()
        self.y_cord = given_spot.getY()

