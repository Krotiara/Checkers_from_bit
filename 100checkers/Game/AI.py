from Game import CheckerColors as CC


class AI:
    def __init__(self, color, Ch, depth):
        self.color = color
        self.field_size = Ch.size
        self.Ch = Ch
        self.field = self.Ch.field
        self.list_checkers = []
        self.depth = depth
        self.best_move = None
        self.on_motion_player = None

    def find_checkers(self, color):
        list = []
        for cell in range(1, self.Ch.number_of_cell + 1):
            color_cell = self.Ch.find_clr_of_num_cell(cell)
            if color_cell == color:
                list.append(cell)
        return list

    def alpha_beta(self, depth, color, alpha, beta):
        if depth == 0:
            # оценка конечной позиции
            return self.evaluate(color)
        color_enemy = CC.CheckerColors.black \
            if color == CC.CheckerColors.white else CC.CheckerColors.white
        all_motions = self.get_all_motions(color)
        if not all_motions:
            return -1
        best_move = all_motions[0]
        while all_motions and alpha < beta:
            motion = all_motions.pop()
            if self.Ch.start_moving(motion[0], motion[1]):
                if self.Ch.white_checkers_count <= 0 \
                        or self.Ch.black_checkers_count <= 0:
                    return -1
                tmp = - self.alpha_beta(depth - 1, color_enemy, -beta, -alpha)
                self.Ch.undo()
                if tmp > alpha:
                    alpha = tmp
                    best_move = motion
        self.best_move = best_move
        self.Ch.flag_fight = False
        self.on_game_over_win = None
        self.on_game_over_deadhead = None
        return alpha

    def evaluate(self, color):
        color_other = CC.CheckerColors.black \
            if color == CC.CheckerColors.white else CC.CheckerColors.white
        sum_for_color = 0
        sum_for_other = 0
        for i in range(self.field_size):
            for j in range(self.field_size):
                cell = self.field[i][j]
                if cell.color == color:
                    sum_for_color += cell.weight
                elif cell.color == color_other:
                    sum_for_other += cell.weight
        if sum_for_other == sum_for_color:
            return 0
        elif sum_for_color > sum_for_other:
            return 1
        else:
            return -1

    def step_ai(self):
        if self.color == CC.CheckerColors.black \
                and not self.Ch.white_motion \
                or self.color == CC.CheckerColors.white \
                        and self.Ch.white_motion:
            self.alpha_beta(self.depth, self.color, float('-inf'), float('inf'))
            step = self.best_move
            self.Ch.turn_decision_hack(step[0])
            self.Ch.turn_decision_move(step[0])
            self.Ch.start_moving(step[0], step[1])

    def fill_list_motion(self, param_hack, list_checkers):
        list_motions = []
        for cell in list_checkers:
            i, j = self.Ch.find_cell_coords(cell)
            checker = self.Ch.field[i][j]
            if param_hack:
                if checker.where_cell_can_hack:
                    for third_cell in checker.list_move_after_hack:
                        list_motions.append((cell, third_cell))
            else:
                if checker.where_cell_can_move:
                    for second_cell in checker.where_cell_can_move:
                        list_motions.append((cell, second_cell))
        return list_motions

    def get_all_motions(self, color):
        list_checkers = self.find_checkers(color)
        self.Ch.check_step()
        for cell in list_checkers:
            self.Ch.turn_decision_move(cell)
        if self.Ch.flag_fight:
            list_motions = self.fill_list_motion(True, list_checkers)
        else:
            list_motions = self.fill_list_motion(False, list_checkers)
        return list_motions
