## Object representing the board of spaces in a game ##
#######################################################
## Author: Jake Swanson

from GameObjects.Space import Space

class Board:
    WIDTH = 5
    HEIGHT = 5

    def __init__(self):
        self.grid = [
                        [Space(i, j) for i in range(self.WIDTH)]
                        for j in range(self.HEIGHT)
                    ]
    
