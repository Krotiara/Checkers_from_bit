from copy import deepcopy

from Game import ClassCell, CheckerColors as CC,\
    ClassGameEnd as CG, FieldState as FS


class CheckersLogic:
    def __init__(self, size):
        self.size = size
        self.number_of_cell = int((self.size * self.size) / 2)
        self.number = 1
        self.field = self.fill_field()
        self.flag_white_checker = True
        self.white_checkers_count = 0
        self.black_checkers_count = 0
        self.flag_fight = False
        self.on_game_over_win = None
        self.on_game_over_deadhead = None
        for i in range(size):
            if i == size / 2 - 1 or i == size / 2:
                continue
            if i > size / 2:
                self.flag_white_checker = False
            for j in range(size):
                if self.field[i][j].number == self.field[i][j].is_white:
                    continue
                else:
                    if self.flag_white_checker:
                        self.field[i][j].is_checker = True
                        self.field[i][j].color = CC.CheckerColors.black
                        self.field[i][j].king = False
                        self.black_checkers_count += 1
                    if not self.flag_white_checker:
                        self.field[i][j].is_checker = True
                        self.field[i][j].color = CC.CheckerColors.white
                        self.field[i][j].king = False
                        self.white_checkers_count += 1
        self.white_checkers_count //= 2
        self.black_checkers_count //= 2
        self.white_motion = True
        self.flag_correct_motion = None
        self.flag_game_over = False
        self.diags = self.get_alldiags()
        self.list_continue_hack = []
        self.game_list = []
        self.undo_stack = []
        self.redo_stack = []
        self.redo_game_list = []
        self.game_over = False
        self.save_state()
        self.check_step()

    def fill_field(self):
        field = [[None for y in range(self.size)] for x in range(self.size)]
        for y in range(self.size):
            for x in range(self.size):
                field[y][x] = ClassCell.Cell(x, y, self.number)
                if (x + y) % 2 != 0:
                    self.number += 1
        return field

    def get_alldiags(self):
        diags = []
        diags_down = self.search_diags("down")
        diags_right = self.search_diags("right")
        diags_left = self.search_diags("left")
        for i in diags_down:
            if i not in diags:
                diags.append(i)
        for i in diags_right:
            if i not in diags:
                diags.append(i)
        for i in diags_left:
            if i not in diags:
                diags.append(i)
        return diags

    def search_diags(self, param):
        diags = []
        if param == "down":
            for i in range(self.size):
                diag_left = []
                diag_right = []
                if self.field[self.size - 1][i].is_white:
                    continue
                else:
                    x, y = self.size - 1, i
                    while True:
                        if y < 0:
                            break
                        else:
                            diag_left.append(int(self.field[x][y].number))
                            x -= 1
                            y -= 1
                    if len(diag_left) > 1:
                        diags.append(diag_left)
                    x, y = self.size - 1, i
                    while True:
                        if x < 0 or y >= len(self.field):
                            break
                        else:
                            diag_right.append(int(self.field[x][y].number))
                            x -= 1
                            y += 1
                    if len(diag_right) > 1:
                        diags.append(diag_right)
        diags_right_edge = self.find_diags_on_the_edges(self.size - 1, "right")
        diags_left_edge = self.find_diags_on_the_edges(0, "left")
        diags.extend(diags_right_edge)
        diags.extend(diags_left_edge)
        return diags

    def find_diags_on_the_edges(self, index_y, param_edge):
        diags = []
        for i in range(self.size - 1, 0, -1):
            diag = []
            if self.field[i][index_y].is_white:
                continue
            else:
                x, y = i, index_y
                while True:
                    if x < 0 or y >= len(self.field) or y < 0:
                        break
                    else:
                        diag.append(int(self.field[x][y].number))
                        if param_edge == "left":
                            x -= 1
                            y += 1
                        elif param_edge == "right":
                            x -= 1
                            y -= 1
                if len(diag) > 1:
                    diags.append(diag)
        return diags

    def get_diags_for_cell(self, number):
        cells_diag = []
        for i in range(len(self.diags)):
            for j in range(len(self.diags[i])):
                if number == self.diags[i][j]:
                    cells_diag.append(self.diags[i])
        return cells_diag

    def find_cell_coords(self, num_cell):
        if num_cell is not None:
            for i in range(self.size):
                for j in range(self.size):
                    if self.field[i][j].number == num_cell:
                        return i, j

    def find_diag_for_cells(self, first_cell, second_cell):
        diags = self.get_diags_for_cell(first_cell)
        for i in diags:
            first_coor = self.find_cell_posn_in_diag(i, first_cell)
            second_coor = self.find_cell_posn_in_diag(i, second_cell)
            if first_coor != -1 and second_coor != -1:
                return i

    def is_cells_on_one_diag(self, first_cell, second_cell):
        diags = self.get_diags_for_cell(first_cell)
        for i in diags:
            for j in i:
                if j == second_cell:
                    return True
        return False

    def check_motion(self, i, j):
        if self.white_motion and self.field[i][
            j].color == CC.CheckerColors.white:
            self.flag_correct_motion = True
        elif not self.white_motion and self.field[i][
            j].color == CC.CheckerColors.black:
            self.flag_correct_motion = True
        else:
            self.flag_correct_motion = False

    def start_moving(self, first_cell, second_cell):
        flag_move = False
        flag_hack = False
        if self.is_cells_on_one_diag(first_cell, second_cell):
            i, j = self.find_cell_coords(first_cell)
            cell = self.field[i][j]
            if second_cell in cell.where_cell_can_move:
                flag_move = self.move(first_cell, second_cell)
            elif not self.is_cells_between_nums_empty(first_cell, second_cell):
                flag_hack = self.hack(first_cell, second_cell)
            if flag_hack or flag_move:
                self.check_step()
            return flag_hack or flag_move
        else:
            return False

    def move(self, first_cell, second_cell):
        x0, y0 = self.find_cell_coords(first_cell)
        x, y = self.find_cell_coords(second_cell)
        cell = self.field[x0][y0]
        self.check_motion(x0, y0)
        diag = self.find_diag_for_cells(first_cell, second_cell)
        checker_color = self.find_clr_of_num_cell(first_cell)
        second_color = self.find_clr_of_num_cell(second_cell)
        first_coor = self.find_cell_posn_in_diag(diag, first_cell)
        second_coor = self.find_cell_posn_in_diag(diag, second_cell)
        if not cell.is_king:
            if not self.is_move_back(checker_color, first_coor, second_coor) \
                    and second_cell in cell.where_cell_can_move \
                    and not self.flag_fight \
                    and second_color != checker_color:
                self.game_list.append(
                    ["white" if self.white_motion else "black",
                     str((x0, y0)),
                     "- " + str((x, y))])
                self.redo_stack.clear()
                self.field_change_move(first_cell, second_cell)
                return True
            return False
        else:
            if self.flag_correct_motion \
                    and second_cell in cell.where_cell_can_move \
                    and not self.flag_fight:
                self.game_list.append(
                    ["white" if self.white_motion else "black",
                     str((x0, y0)),
                     "- " + str((x, y))])
                self.redo_stack.clear()
                self.field_change_move(first_cell, second_cell)
                return True
            return False

    def hack(self, first, third):
        x0, y0 = self.find_cell_coords(first)
        x, y = self.find_cell_coords(third)
        first_cell = self.field[x0][y0]
        third_cell = self.field[x][y]
        self.check_motion(x0, y0)
        list_between_cells = self.get_cells_between_cells(first, third)
        if not first_cell.is_king:
            if len(list_between_cells) != 1:
                return
            second = list_between_cells[0]
            f, g = self.find_cell_coords(second)
            second_cell = self.field[f][g]
            if self.flag_correct_motion \
                    and second in first_cell.where_cell_can_hack:
                self.game_list.append(
                    ["white" if self.white_motion else "black",
                     str((x0, y0)),
                     ": " + str((x, y))])
                self.redo_stack.clear()
                self.field_change_hack(first_cell, second_cell, third_cell)
                self.changing_course_hack(third)
                return True
            return False
        else:
            for i in list_between_cells:
                if i in first_cell.where_cell_can_hack \
                        and third in first_cell.list_move_after_hack \
                        and self.flag_correct_motion:
                    f, g = self.find_cell_coords(i)
                    second_cell = self.field[f][g]
                    self.game_list.append(
                        ["white" if self.white_motion else "black",
                         str((x0, y0)),
                         ": " + str((x, y))])
                    self.redo_stack.clear()
                    self.field_change_hack(first_cell, second_cell, third_cell)
                    self.changing_course_hack(third)
                    return True
            return False

    def changing_course_hack(self, cell_number):
        k, q = self.find_cell_coords(cell_number)
        cell = self.field[k][q]
        self.turn_decision_hack(cell_number)
        if not cell.where_cell_can_hack:
            self.white_motion = not self.white_motion
            self.save_state()
            self.list_continue_hack.clear()
        else:
            self.save_state()
            self.list_continue_hack.append(cell_number)

    def field_change_hack(self, first_cell, second_cell, third_cell):
        third_cell.color = first_cell.color
        third_cell.is_checker = True
        third_cell.king = first_cell.king
        third_cell.weight = first_cell.weight
        if second_cell.color == CC.CheckerColors.black:
            self.black_checkers_count -= 1
        if second_cell.color == CC.CheckerColors.white:
            self.white_checkers_count -= 1
        second_cell.color = CC.CheckerColors.not_checker
        second_cell.is_checker = False
        second_cell.king = False
        second_cell.weight = 1
        first_cell.color = CC.CheckerColors.not_checker
        first_cell.is_checker = False
        first_cell.king = False
        first_cell.weight = 1
        self.clear_checkers_lists()

    def field_change_move(self, first, second):
        i, j = self.find_cell_coords(first)
        k, q = self.find_cell_coords(second)
        second_cell = self.field[k][q]
        first_cell = self.field[i][j]
        if second_cell.color == CC.CheckerColors.black:
            self.black_checkers_count -= 1
        if second_cell.color == CC.CheckerColors.white:
            self.white_checkers_count -= 1
        second_cell.color = first_cell.color
        first_cell.color = CC.CheckerColors.not_checker
        second_cell.is_checker = first_cell.is_checker
        first_cell.is_checker = False
        second_cell.king = first_cell.king
        first_cell.king = False
        second_cell.weight = first_cell.weight
        first_cell.weight = 1
        self.white_motion = not self.white_motion
        self.clear_checkers_lists()
        self.save_state()

    def clear_checkers_lists(self):
        for p in range(1, self.number_of_cell + 1):
            i, j = self.find_cell_coords(p)
            cell = self.field[i][j]
            cell.where_cell_can_move.clear()
            cell.where_cell_can_hack.clear()
            cell.list_move_after_hack.clear()

    def check_game_over(self):
        flag_no_move = False
        flag_no_hack = False
        checkers_color = CC.CheckerColors.white if self.white_motion \
            else CC.CheckerColors.black
        checkers = self.find_checkers(checkers_color)
        if self.white_checkers_count <= 0 or self.black_checkers_count <= 0:
            return CG.GameEndStates.win
        for cell in checkers:
            self.turn_decision_move(cell)
            i, j = self.find_cell_coords(cell)
            if not self.field[i][j].where_cell_can_move:
                flag_no_move = True
            else:
                flag_no_move = False
                break
            if not self.field[i][j].where_cell_can_hack:
                flag_no_hack = True
            else:
                flag_no_hack = False
                break
        if flag_no_hack and flag_no_move:
            return CG.GameEndStates.win
        return CG.GameEndStates.not_end

    def check_step(self):
        whos_step_color = CC.CheckerColors.white if self.white_motion \
            else CC.CheckerColors.black
        checkers = self.find_checkers(whos_step_color)
        self.flag_fight = False
        self.seaching_kings()
        if not self.list_continue_hack:
            for cell in checkers:
                self.turn_decision_hack(cell)
        else:
            for cell in self.list_continue_hack:
                self.turn_decision_hack(cell)
        if self.is_lack_of_fight():
            self.flag_fight = False

    def find_checkers(self, color):
        list = []
        for cell in range(1, self.number_of_cell + 1):
            color_cell = self.find_clr_of_num_cell(cell)
            if color_cell == color:
                list.append(cell)
        return list

    def get_list_neighbors(self, diag, pos_cell, param):
        neighbors = []
        if param == "hack":
            for i in range(-2, 3):
                if pos_cell + i > len(diag) - 1 or pos_cell + i < 0:
                    continue
                else:
                    neighbors.append(diag[pos_cell + i])
            return neighbors
        else:
            for i in range(-1, 2):
                if pos_cell + i > len(diag) - 1 or pos_cell + i < 0:
                    continue
                else:
                    neighbors.append(diag[pos_cell + i])
            return neighbors

    def turn_decision_move(self, cell_number):
        i, j = self.find_cell_coords(cell_number)
        cell = self.field[i][j]
        diags_cell_in = self.get_diags_for_cell(cell_number)
        if not cell.is_king:
            for diag in diags_cell_in:
                pos_cell = self.find_cell_posn_in_diag(diag, cell_number)
                list_neibs_move = self.get_list_neighbors(diag, pos_cell,
                                                          "move")
                for fir, sec in zip(list_neibs_move[:-1],
                                    list_neibs_move[1:]):
                    if fir == cell_number:
                        self.desision_of_move(fir, sec, False)
                    if sec == cell_number:
                        self.desision_of_move(sec, fir, False)
        else:
            for diag in diags_cell_in:
                for cell in diag:
                    if cell != cell_number:
                        self.desision_of_move(cell_number, cell, True)



    def turn_decision_hack(self, cell_number):
        cell_color = self.find_clr_of_num_cell(cell_number)
        i, j = self.find_cell_coords(cell_number)
        cell = self.field[i][j]
        diags_cell_in = self.get_diags_for_cell(cell_number)
        if not cell.is_king:
            for diag in diags_cell_in:
                pos_cell = self.find_cell_posn_in_diag(diag, cell_number)
                list_neibs_hack = self.get_list_neighbors(diag, pos_cell,
                                                          "hack")
                for fir, sec, thd in zip(list_neibs_hack[:-2],
                                         list_neibs_hack[1:-1],
                                         list_neibs_hack[2:]):
                    if fir == cell_number:
                        self.decision_of_hack(fir, sec, thd, False)
                    if thd == cell_number:
                        self.decision_of_hack(thd, sec, fir, False)
        else:
            for diag in diags_cell_in:
                for cell in diag:
                    if cell != cell_number:
                        i = self.find_cell_posn_in_diag(diag, cell_number)
                        j = self.find_cell_posn_in_diag(diag, cell)
                        if j < i:
                            list_between = self.get_cells_between_cells(
                                diag[0], cell)
                            list_between.append(diag[0])
                        elif i < j:
                            list_between = \
                                self.get_cells_between_cells(
                                    cell, diag[len(diag) - 1])
                            list_between.append(diag[len(diag) - 1])
                        for third_cell in list_between:
                            self.decision_of_hack(cell_number, cell,
                                                  third_cell, True)

    def decision_of_hack(self, first_cell, second_cell, third_cell, param_king):
        x, y = self.find_cell_coords(first_cell)
        cell = self.field[x][y]
        fir_color = self.find_clr_of_num_cell(first_cell)
        sec_color = self.find_clr_of_num_cell(second_cell)
        thd_color = self.find_clr_of_num_cell(third_cell)
        if not param_king:
            if self.is_correct_conditions_to_hack(fir_color, sec_color,
                                                  thd_color):
                self.flag_fight = True
                if second_cell not in cell.where_cell_can_hack:
                    cell.where_cell_can_hack.append(second_cell)
                if third_cell not in cell.list_move_after_hack:
                    cell.list_move_after_hack.append(third_cell)
        else:
            if self.is_correct_conditions_to_hack(fir_color, sec_color,
                                                  thd_color) and \
                    self.is_cells_between_nums_empty(second_cell,
                                                     third_cell) and \
                    self.is_cells_between_nums_empty(first_cell, second_cell):
                self.flag_fight = True
                if second_cell not in cell.where_cell_can_hack:
                    cell.where_cell_can_hack.append(second_cell)
                if third_cell not in cell.list_move_after_hack:
                    cell.list_move_after_hack.append(third_cell)

    def desision_of_move(self, first_cell, second_cell, param_king):
        x, y = self.find_cell_coords(first_cell)
        fir_color = self.find_clr_of_num_cell(first_cell)
        sec_color = self.find_clr_of_num_cell(second_cell)
        diag = self.find_diag_for_cells(first_cell, second_cell)
        fir_coor = self.find_cell_posn_in_diag(diag, first_cell)
        sec_coor = self.find_cell_posn_in_diag(diag, second_cell)
        cell = self.field[x][y]
        if not param_king:
            if fir_color != CC.CheckerColors.not_checker and \
                            sec_color == CC.CheckerColors.not_checker \
                    and fir_color != sec_color \
                    and not self.flag_fight \
                    and not self.is_move_back(fir_color, fir_coor, sec_coor) \
                    and not cell.where_cell_can_hack:
                if second_cell not in cell.where_cell_can_move:
                    cell.where_cell_can_move.append(second_cell)
        if param_king:
            list_move = self.get_cells_between_cells(first_cell, second_cell)
            cells_empty = True
            for i in list_move:
                color_cel = self.find_clr_of_num_cell(i)
                if color_cel != CC.CheckerColors.not_checker:
                    cells_empty = False
            if cells_empty and sec_color == CC.CheckerColors.not_checker:
                if second_cell not in cell.where_cell_can_move and len(
                        cell.where_cell_can_hack) == 0:
                    cell.where_cell_can_move.append(second_cell)

    def seaching_kings(self):
        for x in range(self.size):
            for y in range(self.size):
                color_cell = self.field[x][y].color
                if x == 0 and color_cell == CC.CheckerColors.white:
                    self.field[x][y].king = True
                elif x == len(self.field) - 1 \
                        and color_cell == CC.CheckerColors.black:
                    self.field[x][y].king = True

    def is_move_back(self, color_cell, fir_coor, sec_coor):
        return color_cell == CC.CheckerColors.white and \
               fir_coor > sec_coor or \
               color_cell == CC.CheckerColors.black and \
               sec_coor > fir_coor

    def is_correct_conditions_to_hack(self, fir_clr, sec_clr, thd_clr):
        return fir_clr != CC.CheckerColors.not_checker and \
               fir_clr != sec_clr and \
               sec_clr != CC.CheckerColors.not_checker and \
               thd_clr == CC.CheckerColors.not_checker

    def get_cells_between_cells(self, first_cell, second_cell):
        diag = self.find_diag_for_cells(first_cell, second_cell)
        list_cells = []
        i = self.find_cell_posn_in_diag(diag, first_cell)
        j = self.find_cell_posn_in_diag(diag, second_cell)
        if i < j:
            for q in range(i + 1, j):
                list_cells.append(diag[q])
        else:
            for q in range(i - 1, j, -1):
                list_cells.append(diag[q])
        return list_cells

    def is_cells_between_nums_empty(self, first_cell, second_cell):
        cells_empty = True
        list_move = self.get_cells_between_cells(first_cell, second_cell)
        if len(list_move) != 0:
            for i in list_move:
                color_cell = self.find_clr_of_num_cell(i)
                if color_cell != CC.CheckerColors.not_checker:
                    cells_empty = False
        return cells_empty

    def find_cell_posn_in_diag(self, diag, cell):
        for i in range(len(diag)):
            if diag[i] == cell:
                return i
        return -1

    def is_lack_of_fight(self):
        for i in range(1, self.number_of_cell + 1):
            x, y = self.find_cell_coords(i)
            if self.field[x][y].where_cell_can_hack:
                return False
        return True

    def find_clr_of_num_cell(self, cell_number):
        x, y = self.find_cell_coords(cell_number)
        return self.field[x][y].color

    def save_state(self):
        field = deepcopy(self.field)
        list_continue_hack = deepcopy(self.list_continue_hack)
        white_motion = deepcopy(self.white_motion)
        flag_fight = deepcopy(self.flag_fight)
        white_checkers = deepcopy(self.white_checkers_count)
        black_checkers = deepcopy(self.black_checkers_count)
        field_state = FS.FieldState(field, white_motion,
                                    flag_fight,
                                    list_continue_hack,
                                    white_checkers,
                                    black_checkers)
        self.undo_stack.append(field_state)

    def undo(self):
        if len(self.undo_stack) > 1:
            self.redo_stack.append(deepcopy(self.undo_stack.pop()))
            self.redo_game_list.append(self.game_list.pop())
            if len(self.undo_stack) != 0:
                field_state = self.undo_stack[-1]
                self.field = deepcopy(field_state.field)
                self.white_motion = deepcopy(field_state.white_motion)
                self.flag_fight = deepcopy(field_state.flag_fight)
                self.list_continue_hack = deepcopy(
                    field_state.list_continue_hack)
                self.white_checkers_count = field_state.white_checkers
                self.black_checkers_count = field_state.black_checkers
                self.check_step()

    def redo(self):
        if len(self.redo_stack) != 0:
            self.undo_stack.append(deepcopy(self.redo_stack.pop()))
            self.game_list.append(self.redo_game_list.pop())
            field_state = self.undo_stack[-1]
            self.field = deepcopy(field_state.field)
            self.white_motion = deepcopy(field_state.white_motion)
            self.flag_fight = deepcopy(field_state.flag_fight)
            self.list_continue_hack = deepcopy(
                field_state.list_continue_hack)
            self.white_checkers_count = field_state.white_checkers
            self.black_checkers_count = field_state.black_checkers
            self.check_step()
