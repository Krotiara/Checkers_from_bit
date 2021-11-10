import copy


class FieldState:
    def __init__(self, field, white_motion, flag_fight,
                 list_continue_hack, white_checkers, black_checkers):
        self.field = copy.deepcopy(field)
        self.white_motion = copy.deepcopy(white_motion)
        self.flag_fight = copy.deepcopy(flag_fight)
        self.list_continue_hack = copy.deepcopy(list_continue_hack)
        self.white_checkers = copy.deepcopy(white_checkers)
        self.black_checkers = copy.deepcopy(black_checkers)
