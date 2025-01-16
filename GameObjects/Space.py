## Object representing a single space in a board ##
###################################################
## Author: Jake Swanson

class Space:

    def __init__(self, _x_cord, _y_cord):
        self.x = _x_cord   # X-Cord for space
        self.y = _y_cord    # Y-Cord for space
        self.playerNum = 0  # Player num in space. 0 = No one
        self.level = 0      # Floor Level

    def __repr__(self):
        return ("x - " + str(self.x) +
                " y - " + str(self.y) +
                " pnum - " + str(self.playerNum) +
                " l - " + str(self.level)) + "\n"

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def set_player(self, num):
        self.playerNum = num

    def get_player(self):
        return self.playerNum

    def build_level(self):
        if self.level < 4:
            self.level += 1

        return self.level < 4

    def remove_level(self):
        if self.level > 0:
            self.level -= 1

        return self.level > 0

    def get_level(self):
        return self.level

    def set_cords(self, _x, _y):
        self.x = _x
        self.y = _y

    def same_spot(self, check_spot):
        return (self.level == check_spot.get_level() and
                self.playerNum == check_spot.get_player())