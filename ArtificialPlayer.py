from GameObjects.Board import Board


class ArtificialPlayer:
    def __init__(self, _d, _board: Board):
        self.Depth = _d              ## The depth to look into the future for
        self.current_board = _board  ## The board to analyse
        self.insight_count = 0       ## The count of how many possible moves the AI has looked at

