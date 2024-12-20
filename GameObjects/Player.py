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
    def get_display(self):
        # Player will be discs of a certain color depending on the player num
        RADIUS = 30
        player_display = Circle(Point(self.x_cord, self.y_cord), RADIUS)

        if self.label == 1:
            player_display.setFill(color="blue")
        if self.label == 2:
            player_display.setFill(color="gray")

        return player_display

    def set_space(self, given_spot):
        self.x_cord = given_spot.getX()
        self.y_cord = given_spot.getY()

