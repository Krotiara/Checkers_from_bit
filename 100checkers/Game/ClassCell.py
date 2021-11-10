from Game import CheckerColors as CC


class Cell:
    def __init__(self, x, y, number):
        self.color = CC.CheckerColors.not_checker
        self.is_checker = False
        if (x + y) % 2 == 0:
            self.color_cell = CC.CheckerColors.white_cell
            self.number = None
        else:
            self.number = number
            self.color_cell = CC.CheckerColors.black_cell
        self.where_cell_can_hack = []
        self.where_cell_can_move = []
        self.list_move_after_hack = []
        self.king = False
        if self.king:
            self.weight = 3
        else:
            self.weight = 1

    @property
    def is_white(self):
        return self.number is None

    @property
    def is_king(self):
        return self.king
