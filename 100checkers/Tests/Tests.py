import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir))
from Game import Checkers as CH, CheckerColors as CC


class Test(unittest.TestCase):
    def setUp(self):
        self.game = CH.CheckersLogic(10)
        self.game_8 = CH.CheckersLogic(8)
        self.game_4 = CH.CheckersLogic(4)

    def testPossibleMove(self):
        game = self.game
        game.turn_decision_move(35)
        game.turn_decision_move(32)
        game.turn_decision_move(50)
        assert_list_move_35 = [30]
        assert_list_move_32 = [28, 27]
        assert_list_move_50 = []
        i, j = game.find_cell_coords(35)
        k, q = game.find_cell_coords(32)
        p, g = game.find_cell_coords(50)
        cell_35 = game.field[i][j]
        cell_32 = game.field[k][q]
        cell_50 = game.field[p][g]
        self.assertEqual(cell_35.where_cell_can_move, assert_list_move_35)
        self.assertEqual(cell_32.where_cell_can_move, assert_list_move_32)
        self.assertEqual(cell_50.where_cell_can_move, assert_list_move_50)

    def testMove(self):
        game = self.game
        game.turn_decision_move(35)
        game.move(35, 30)
        i, j = game.find_cell_coords(30)
        k, q = game.find_cell_coords(35)
        cell_30 = game.field[i][j]
        cell_35 = game.field[k][q]
        assert_color_30 = CC.CheckerColors.white
        assert_checker_30 = True
        assert_color_35 = CC.CheckerColors.not_checker
        assert_checker_35 = False
        self.assertEqual(assert_checker_30, cell_30.is_checker)
        self.assertEqual(assert_checker_35, cell_35.is_checker)
        self.assertEqual(assert_color_30, cell_30.color)
        self.assertEqual(assert_color_35, cell_35.color)

    def testMotionSwitch(self):
        game = self.game
        game.turn_decision_move(35)
        assert_white_motion_before = True
        assert_white_motion_after = False
        self.assertEqual(assert_white_motion_before, game.white_motion)
        game.move(35, 30)
        self.assertEqual(assert_white_motion_after, game.white_motion)

    def testWrongMove(self):
        game = self.game
        game.turn_decision_move(35)
        flag_correct_motion = game.move(35, 24)
        self.assertEqual(flag_correct_motion, False)

    def testPossibleHack(self):
        game = self.game
        game.turn_decision_move(35)
        game.move(35, 30)
        game.turn_decision_move(19)
        game.move(19, 24)
        game.check_step()
        i, j = game.find_cell_coords(30)
        k, q = game.find_cell_coords(34)
        cell_30 = game.field[i][j]
        cell_34 = game.field[k][q]
        assert_hack_list_30 = [24]
        assert_hack_list_34 = []
        self.assertEqual(assert_hack_list_30, cell_30.where_cell_can_hack)
        self.assertEqual(assert_hack_list_34, cell_34.where_cell_can_hack)

    def testHack(self):
        game = self.game
        game.turn_decision_move(35)
        game.move(35, 30)
        game.turn_decision_move(19)
        game.move(19, 24)
        game.check_step()
        game.hack(30, 19)
        i, j = game.find_cell_coords(24)
        k, q = game.find_cell_coords(30)
        t, r = game.find_cell_coords(19)
        cell_30 = game.field[k][q]
        cell_24 = game.field[i][j]
        cell_19 = game.field[t][r]
        assert_color_24 = CC.CheckerColors.not_checker
        assert_checker_24 = False
        assert_color_30 = CC.CheckerColors.not_checker
        assert_checker_30 = False
        assert_color_19 = CC.CheckerColors.white
        assert_checker_19 = True
        self.assertEqual(assert_color_30, cell_30.color)
        self.assertEqual(assert_color_24, cell_24.color)
        self.assertEqual(assert_color_19, cell_19.color)
        self.assertEqual(assert_checker_30, cell_30.is_checker)
        self.assertEqual(assert_checker_24, cell_24.is_checker)
        self.assertEqual(assert_checker_19, cell_19.is_checker)

    def testWrongHack(self):
        game = self.game
        flag_correct_motion = game.hack(30, 19)
        self.assertEqual(flag_correct_motion, False)

    def testContinueHack(self):
        game = self.game_8
        game.turn_decision_move(22)
        game.move(22, 18)
        game.turn_decision_move(10)
        game.move(10, 14)
        game.turn_decision_move(23)
        game.move(23, 19)
        game.check_step()
        game.hack(14, 23)
        assert_list_hack = [23]
        self.assertEqual(assert_list_hack, game.list_continue_hack)

    def testCorrectKing(self):
        game = self.game_4
        game.turn_decision_move(7)
        game.move(7, 5)
        game.turn_decision_move(2)
        game.move(2, 4)
        game.check_step()
        game.hack(5, 2)
        game.seaching_kings()
        i, j = game.find_cell_coords(2)
        cell = game.field[i][j]
        assert_king = True
        self.assertEqual(assert_king, cell.king)

    def testCorrectDiags(self):
        game = self.game_4
        asser_diags = [[7, 5, 4, 2], [8, 5, 3], [8, 6], [6, 4, 1], [3, 1]]
        self.assertEqual(asser_diags, game.diags)

    def testUndo(self):
        game = self.game_4
        game.turn_decision_move(7)
        game.move(7, 5)
        game.undo()
        i, j = game.find_cell_coords(7)
        k, q = game.find_cell_coords(5)
        cell_7 = game.field[i][j]
        cell_5 = game.field[k][q]
        assert_color_7 = CC.CheckerColors.white
        assert_checker_7 = True
        assert_color_5 = CC.CheckerColors.not_checker
        assert_checker_5 = False
        self.assertEqual(assert_checker_7, cell_7.is_checker)
        self.assertEqual(assert_checker_5, cell_5.is_checker)
        self.assertEqual(assert_color_7, cell_7.color)
        self.assertEqual(assert_color_5, cell_5.color)

    def testRedo(self):
        game = self.game_4
        game.turn_decision_move(7)
        game.move(7, 5)
        game.undo()
        game.redo()
        i, j = game.find_cell_coords(7)
        k, q = game.find_cell_coords(5)
        cell_7 = game.field[i][j]
        cell_5 = game.field[k][q]
        assert_color_7 = CC.CheckerColors.not_checker
        assert_checker_7 = False
        assert_color_5 = CC.CheckerColors.white
        assert_checker_5 = True
        self.assertEqual(assert_checker_7, cell_7.is_checker)
        self.assertEqual(assert_checker_5, cell_5.is_checker)
        self.assertEqual(assert_color_7, cell_7.color)
        self.assertEqual(assert_color_5, cell_5.color)


if __name__ == '__main__':
    unittest.main()
