class Turn:
    def __init__(self, _piece, _move, _build):
        self.piece = _piece
        self.move = _move
        self.build = _build
        self.evaluation = 0

    def __repr__(self):
        return ("First pick piece at: " + str(self.piece) +
                "Next, move that piece to: " + str(self.move) +
                "Next, build that piece at: "+ str(self.build) )

    def get_piece(self):
        return self.piece

    def get_move(self):
        return self.move

    def get_build(self):
        return self.build

    def get_eval(self):
        return self.evaluation