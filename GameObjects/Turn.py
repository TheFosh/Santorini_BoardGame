class Turn:
    def __init__(self, _piece = None, _move = None , _build = None):
        self.id = 0
        self.piece = _piece
        self.move = _move
        self.build = _build
        self.evaluation = -1000000000000

    def __repr__(self):
        return ("Turn with id " + str(self.id) + " says to\n" +
                "First pick piece at: " + str(self.piece) +
                "Next, move that piece to: " + str(self.move) +
                "Next, build that piece at: "+ str(self.build) +
                "This has an evaluation score of: " + str(self.evaluation)+"\n")

    def get_piece(self):
        return self.piece

    def get_move(self):
        return self.move

    def get_build(self):
        return self.build

    def get_evaluation(self):
        return self.evaluation

    def get_id(self):
        return self.id

    def set_evaluation(self, evalu):
        self.evaluation = evalu

    def set_id(self, i):
        self.id = i