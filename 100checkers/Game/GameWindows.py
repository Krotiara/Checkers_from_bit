from PyQt5 import QtWidgets
from Game import CheckerColors as CC, FieldException as FE, GameMods as GM, \
    FieldState as FS, Checkers as Ch, ClassGameEnd as CG, AI
from copy import deepcopy
from PyQt5.QtCore import QPoint, QTimer, Qt
from PyQt5.QtGui import QPainter, QColor
import Game.OnlineGame as OG
import Game.OnlineModes as OM



class OnlineWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 200, 150)
        self.setFixedSize(200, 150)
        self.center()
        self.init_gui()


    def init_gui(self):
        self.online_mode = False
        self.fir_player = OM.OnlinePlayers.OFFLINE
        self.sec_player = OM.OnlinePlayers.OFFLINE
        self.ip_text = None
        self.v_box = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel("Choose online mode")
        self.combo = QtWidgets.QComboBox(self)
        self.combo.addItems(["Offline", "Client", "Server"])
        self.combo.currentText = "Offline"
        self.combo.activated[str].connect(self.on_activated)
        self.buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.btn_input)
        self.buttons.rejected.connect(self.btn_close)
        self.v_box.addWidget(self.label)
        self.v_box.addWidget(self.combo)
        self.v_box.addWidget(self.buttons)
        self.fixed_len_box = len(self.v_box) - 1
        self.setLayout(self.v_box)


    def on_activated(self, text):
        self.clearLayout()
        if text == "Offline":
            self.v_box.addWidget(self.buttons)
        if text == "Client":
            self.clearLayout()
            self.online_mode = True
            self.fir_player = OM.OnlinePlayers.CLIENT
            self.sec_player = OM.OnlinePlayers.SERVER
            self.label_ip = QtWidgets.QLabel("Input server ip")
            self.line_edit = QtWidgets.QLineEdit()
            self.v_box.removeWidget(self.buttons)
            self.v_box.addWidget(self.label_ip)
            self.v_box.addWidget(self.line_edit)
            self.v_box.addWidget(self.buttons)
        elif text == "Server":
            self.clearLayout()
            self.online_mode = True
            self.fir_player = OM.OnlinePlayers.SERVER
            self.sec_player = OM.OnlinePlayers.CLIENT
            self.v_box.addWidget(self.buttons)


    def btn_input(self):
        text = self.label_ip.text()
        if not text:
            return
        self.ip_text = text
        self.get_start_window()

    def btn_close(self):
        self.close()


    def get_start_window(self):
        game_characters = dict(online_mode=self.online_mode,
                               first_player=self.fir_player,
                               second_player=self.sec_player,
                               ip = self.ip_text)
        if self.fir_player == OM.OnlinePlayers.CLIENT:
            pass
            self.start_window = OG.Client()
            #как то получить номер
        else:
            self.start_window = StartWindow(game_characters)
            self.close()

    def clearLayout(self):
        while self.v_box.count() > self.fixed_len_box:
            item = self.v_box.takeAt(len(self.v_box) - 1)
            if not item:
                continue
            w = item.widget()
            if w:
                w.setParent(None)

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class StartWindow(QtWidgets.QWidget):
    #game_settings
    def __init__(self):
        super().__init__()
        self.field_size = 0
        self.setGeometry(0, 0, 300, 400)
        self.setFixedSize(200, 350)
        self.center()
        self.online_mod = game_settings.get('online_mode')
        self.first_player = game_settings.get('first_player')
        self.second_player = game_settings.get('second_player')
        self.ip = game_settings.get('ip')
        self.init_ui()

    def init_ui(self):
        self.v_box = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel("Input field size")
        self.flag_first = True
        self.game_mode = QtWidgets.QLabel("Choose game mode")
        self.choosing_game_mode = None
        self.le = QtWidgets.QLineEdit("10")
        self.buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.w = None
        self.combo = QtWidgets.QComboBox(self)
        self.combo.addItems(["2 players", "Player vs AI", "AI vs AI"])
        self.combo.currentText = "2 players"
        self.combo.activated[str].connect(self.on_activated)
        self.fir_pr_color = None
        self.sec_pr_color = None
        self.depth_first_bot = None
        self.depth_second_bot = None
        self.label_player = None
        self.new_window(self.game_mode, self.combo)
        self.fixed_len_box = len(self.v_box) - 1
        self.first_bot = True
        self.setLayout(self.v_box)
        self.setWindowTitle('Start window for game')
        self.on_activated(self.combo.currentText)

        self.buttons.accepted.connect(self.btn_input)
        self.buttons.rejected.connect(self.btn_close)

    def new_window(self, widget, combo):
        self.v_box.addWidget(self.label)
        self.v_box.addWidget(self.le)
        self.v_box.addWidget(widget)
        self.v_box.addWidget(combo)
        self.v_box.addWidget(self.buttons)

    def clearLayout(self):
        if self.flag_first:
            self.flag_first = not self.flag_first
            return
        while self.v_box.count() > self.fixed_len_box:
            item = self.v_box.takeAt(len(self.v_box) - 1)
            if not item:
                continue
            w = item.widget()
            if w:
                w.setParent(None)

    def on_activated(self, text):
        self.clearLayout()
        self.choosing_game_mode = text
        if text == GM.GameMods.two_players.value:
            self.v_box.removeWidget(self.buttons)
            self.set_params_choosing("Choose color for first player")
            self.v_box.addWidget(self.buttons)
        elif text == GM.GameMods.player_vs_ai.value \
                or text == GM.GameMods.ai_vs_ai.value:
            self.setGeometry(0, 0, 300, 300)
            self.setFixedSize(200, 300)
            self.center()
            self.v_box.removeWidget(self.buttons)
            if text == GM.GameMods.player_vs_ai.value:
                self.set_params_choosing("Choose color for AI")
            self.set_params_choosing_ai("Choose ai level")
            if text == GM.GameMods.ai_vs_ai.value:
                self.set_params_choosing_ai("Choose second ai level")
            self.v_box.addWidget(self.buttons)


    def set_params_choosing(self, text_label):
        self.label_player = QtWidgets.QLabel(text_label)
        self.b = QtWidgets.QComboBox(self)
        self.b.addItems(["Black", "White"])
        self.b.setCurrentIndex(0)
        self.b.activated[str].connect(self.set_players_characters)
        self.v_box.addWidget(self.label_player)
        self.v_box.addWidget(self.b)

    def set_params_choosing_ai(self, text):
        self.label_player = QtWidgets.QLabel(text)
        self.b = QtWidgets.QComboBox(self)
        self.b.addItems(["Easy", "Normal", "Hard"])
        self.b.setCurrentIndex(0)
        self.b.activated[str].connect(self.set_ai_level)
        self.v_box.addWidget(self.label_player)
        self.v_box.addWidget(self.b)

    def set_ai_level(self, text):
        if text == GM.GameMods.easy_ai.value or text is None:
            if self.first_bot:
                self.depth_first_bot = 1
            else:
                self.depth_second_bot = 1
        elif text == GM.GameMods.normal_ai.value:
            if self.first_bot:
                self.depth_first_bot = 2
            else:
                self.depth_second_bot = 2
        else:
            if self.first_bot:
                self.depth_first_bot = 3
            else:
                self.depth_second_bot = 3
        self.first_bot = False

    def set_players_characters(self, text):
        if text == GM.GameMods.white_color.value or text is None:
            self.fir_pr_color = CC.CheckerColors.white
            self.sec_pr_color = CC.CheckerColors.black
        else:
            self.fir_pr_color = CC.CheckerColors.black
            self.sec_pr_color = CC.CheckerColors.white

    def btn_input(self):
        try:
            text = self.le.text()
            if int(text) <= 3 :
                raise FE.FieldCizeErr("incorrect field size")
            else:
                self.field_size = int(text)
        except ValueError:
            self.le.clear()
            return
        except FE.FieldCizeErr:
            self.le.clear()
            return
        self.get_interface()

    def btn_close(self):
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_interface(self):
        game_characters = dict(game_mode=self.choosing_game_mode,
                               first_player_color=self.fir_pr_color,
                               second_player_color=self.sec_pr_color,
                               first_bot_ai=self.depth_first_bot,
                               second_bot_ai=self.depth_second_bot)
        self.w = Interface(self.field_size, game_characters)
        self.close()


class GameEndWindow(QtWidgets.QWidget):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.setGeometry(0, 0, 300, 100)
        self.setFixedSize(300, 100)
        self.center()
        self.init_gui()

    def init_gui(self):
        label = QtWidgets.QLabel(self.text)
        self.label_new = QtWidgets.QLabel("Do you want play again?")
        self.button_ok = QtWidgets.QPushButton('Ok', self)
        self.game = None
        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(label)
        v_box.addWidget(self.label_new)
        v_box.addWidget(self.button_ok)
        v_box.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        self.setLayout(v_box)
        self.setWindowTitle('Gave over')
        self.button_ok.clicked.connect(self.accept)

    def accept(self):
        self.game = StartWindow()
        self.game.show()
        self.close()

    def reject(self):
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class Interface(QtWidgets.QMainWindow):
    def __init__(self, field_size, game_characters):
        super().__init__()
        self.saved_game = None
        self.initGUI(field_size, game_characters)

    def initGUI(self, field_cize, game_characters):
        self.width = 8 * QtWidgets.QApplication.desktop().width() / 9
        self.height = 8 * QtWidgets.QApplication.desktop().height() // 9
        self.size_window = min(self.width, self.height)
        self.cell_size = self.size_window // field_cize

        self.setGeometry(10, 30, self.size_window, self.size_window)
        self.center()
        wigth_fixed = self.size_window + 2 * self.cell_size
        height_fixed = self.size_window + self.cell_size // 2
        self.setFixedSize(wigth_fixed, height_fixed)
        self.game = InterfaceGame(field_cize, self.size_window,
                                  game_characters)
        self.setCentralWidget(self.game)
        self.label = self.get_motion_window()
        self.logo_window = self.get_logo_window()
        max_height = self.cell_size
        self.label.setMaximumWidth(wigth_fixed - self.size_window)
        self.label.setMaximumHeight(max_height)
        self.game.on_motion = self.change_windows
        self.game.on_new = self.close_game
        self.game.Ch.on_game_over_win = self.end_game_win
        self.game.Ch.on_game_over_deadhead = self.end_game_deadhead
        self.addDockWidget(Qt.RightDockWidgetArea, self.label)
        self.addDockWidget(Qt.RightDockWidgetArea, self.logo_window)
        self.label.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.logo_window.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.setWindowTitle("Checkers")
        self.start_window = None
        self.create_menu()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def close_game(self):
        self.close()

    def end_game_win(self):
        who_win = "White" if not self.game.Ch.white_motion else "Black"
        text = "Game over: " + who_win + " win"
        self.w = GameEndWindow(text)
        self.w.show()
        self.close()

    def end_game_deadhead(self):
        text = "Game over: Dead head"
        self.w = GameEndWindow(text)
        self.w.show()
        self.close()

    def get_logo_window(self):
        self.logo = QtWidgets.QTextEdit(self)
        self.logo.setReadOnly(True)
        logo = QtWidgets.QDockWidget(self)
        logo.setWidget(self.logo)
        return logo

    def get_motion_window(self):
        self.label_motion = QtWidgets.QLabel(self)
        font = self.label_motion.font()
        font.setPointSize(15)
        self.label_motion.setFont(font)
        self.set_label_motion()
        w = QtWidgets.QDockWidget(self)
        w.setWidget(self.label_motion)
        return w

    def change_windows(self):
        self.set_label_motion()
        self.set_logo_text()

    def set_logo_text(self):
        list_motions = self.game.Ch.game_list
        text = ""
        for list in list_motions:
            text_list = " ".join(list)
            text_list += "\n"
            text += text_list
        self.logo.setText(text)

    def set_label_motion(self):
        if self.game.Ch.white_motion:
            text = "Move: \n white"
        else:
            text = "Move: \n black"
        self.label_motion.setText(text)

    def create_menu(self):
        self.bar = self.menuBar()
        self.file = self.bar.addMenu('File')
        self.edit = self.bar.addMenu('Edit')

        self.new_action = QtWidgets.QAction('New', self)

        self.undo_action = QtWidgets.QAction('Undo', self)
        self.undo_action.setShortcut('Ctrl+Z')

        self.redo_action = QtWidgets.QAction("Redo", self)
        self.redo_action.setShortcut('Ctrl+Y')

        self.save_action = QtWidgets.QAction('Save', self)
        self.save_action.setShortcut('Ctrl+S')

        self.load_action = QtWidgets.QAction('Load', self)
        self.load_action.setShortcut('Ctrl+L')

        self.quit_action = QtWidgets.QAction('Quit', self)
        self.quit_action.setShortcut('Ctrl+Q')

        self.clear_logo_action = QtWidgets.QAction('Clear Logo', self)

        self.file.addAction(self.new_action)
        self.file.addAction(self.save_action)
        self.file.addAction(self.load_action)
        self.file.addAction(self.quit_action)

        self.edit.addAction(self.undo_action)
        self.edit.addAction(self.redo_action)

        self.new_action.triggered.connect(self.game.new_game)
        self.save_action.triggered.connect(self.game.save_game)
        self.quit_action.triggered.connect(self.game.exit_game)
        self.load_action.triggered.connect(self.game.load_game)
        self.undo_action.triggered.connect(self.game.undo_game)
        self.undo_action.triggered.connect(self.change_windows)
        self.redo_action.triggered.connect(self.game.redo_game)
        self.redo_action.triggered.connect(self.change_windows)


class InterfaceGame(QtWidgets.QWidget):
    def __init__(self, field_size, size_window, game_characters):
        super().__init__()
        self.ai_vs_ai_flag = False
        self.ai_vs_player_flag = False
        self.field_size = field_size
        self.size_window = size_window
        self.Ch = Ch.CheckersLogic(self.field_size)
        self.timer = QTimer()
        self.timer.timeout.connect(self.step_bot)
        self.timer.start(1000)
        if game_characters.get('game_mode') is None:
            self.game_mode = GM.GameMods.two_players.value
            self.first_player = CC.CheckerColors.white
            self.second_player = CC.CheckerColors.black
            self.is_fir_bot = False
            self.is_sec_bot = False
        else:
            self.game_mode = game_characters.get('game_mode')
            self.first_player = None
            self.second_player = None
            self.is_fir_bot = None
            self.is_sec_bot = None
            self.set_players(game_characters)
        self.step_list = []
        self.paint_list_motions = [[False for y in range(self.field_size)] for x
                                   in range(self.field_size)]
        self.white_color_cell = "#F5DEB3"
        self.black_color_cell = "#A0522D"
        self.white_color_checker = "#EEE5DE"
        self.black_color_checker = "#3D2B1F"
        self.possible_move_color = "#1E90FF"
        self.set_color = QColor(0, 0, 0)
        self.number_color = '#1C1C1C'
        self.cell_size = self.size_window // self.Ch.size
        if self.field_size >= 16 and self.field_size < 24:
            self.checker_r = self.cell_size // 2 - self.Ch.size // 2
        elif self.field_size >= 24:
            self.checker_r = self.cell_size // 2 - self.Ch.size // 3
        else:
            self.checker_r = self.cell_size // 2 - self.Ch.size
        self.on_motion = None
        self.on_new = None
        self.saved_game = None

    def set_players(self, game_characters):
        if game_characters.get('game_mode') == GM.GameMods.two_players.value:
            self.first_player = game_characters.get('first_player_color')
            self.second_player = game_characters.get('second_player_color')
            if self.first_player is None:
                self.first_player = CC.CheckerColors.white
            if self.second_player is None:
                self.second_player = CC.CheckerColors.black
            self.is_fir_bot = False
            self.is_sec_bot = False
        elif game_characters.get('game_mode') == GM.GameMods.player_vs_ai.value:
            self.ai_vs_player_flag = True
            ai_color = game_characters.get('first_player_color')
            ai_depth = game_characters.get('first_bot_ai')
            if ai_color is None:
                ai_color = CC.CheckerColors.black
            if ai_depth is None:
                ai_depth = 1
            self.first_player = AI.AI(ai_color, self.Ch, ai_depth)
            self.second_player = game_characters.get('second_player_color')
            if self.second_player is None:
                self.second_player = CC.CheckerColors.white \
                    if ai_color == CC.CheckerColors.black \
                    else CC.CheckerColors.black
            self.is_fir_bot = True
            self.is_sec_bot = False
        elif game_characters.get('game_mode') == GM.GameMods.ai_vs_ai.value:
            first_ai_color = game_characters.get('first_player_color')
            second_ai_color = game_characters.get('second_player_color')
            first_ai_depth = game_characters.get('first_bot_ai')
            second_ai_depth = game_characters.get('second_bot_ai')
            if first_ai_color is None:
                first_ai_color = CC.CheckerColors.black
            if second_ai_color is None:
                second_ai_color = CC.CheckerColors.white \
                    if first_ai_color == CC.CheckerColors.black \
                    else CC.CheckerColors.black
            if first_ai_depth is None:
                first_ai_depth = 1
            if second_ai_depth is None:
                second_ai_depth = 2
            self.first_player = AI.AI(first_ai_color, self.Ch,
                                      first_ai_depth)
            self.second_player = AI.AI(second_ai_color, self.Ch,
                                       second_ai_depth)
            self.ai_vs_ai_flag = True
            self.is_fir_bot = True
            self.is_sec_bot = True

    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        self.draw_board(paint, event)
        paint.end()

    def mousePressEvent(self, event):
        self.get_field_position(event)
        if len(self.step_list) > 2:
            self.step_list = []
        if len(self.step_list) == 2:
            if self.step():
                self.repaint()
        else:
            event.ignore()
        self.repaint()

    def get_field_position(self, event):
        x = event.x()
        y = event.y()
        i, j = self.get_i_j_coors(x, y)
        cell = self.Ch.field[i][j]
        try:
            if cell.color_cell == CC.CheckerColors.white_cell:
                return
        except IndexError:
            return
        if self.Ch.flag_game_over:
            QtWidgets.qApp.quit()
        self.Ch.turn_decision_move(cell.number)
        self.fill_list_motions(event, i, j)
        if len(self.step_list) == 2:
            self.step_list = []
        self.step_list.append((i, j))

    def fill_list_motions(self, event, i, j):
        if self.Ch.white_motion \
                and self.Ch.field[i][j].color == CC.CheckerColors.white \
                or not self.Ch.white_motion \
                        and self.Ch.field[i][j].color == CC.CheckerColors.black:
            cell = self.Ch.field[i][j]
            if cell.where_cell_can_hack:
                for i in cell.list_move_after_hack:
                    k, q = self.Ch.find_cell_coords(i)
                    self.paint_list_motions[k][q] = True
            else:
                for i in cell.where_cell_can_move:
                    k, q = self.Ch.find_cell_coords(i)
                    self.paint_list_motions[k][q] = True

    def clear_list_motions(self):
        for i in range(len(self.paint_list_motions)):
            for j in range(len(self.paint_list_motions)):
                if self.paint_list_motions[i][j]:
                    self.paint_list_motions[i][j] = False

    def check_game_over(self):
        if self.Ch.check_game_over() == CG.GameEndStates.win:
            self.timer.stop()
            if self.Ch.on_game_over_win:
                self.Ch.on_game_over_win()
        elif self.Ch.check_game_over() == CG.GameEndStates.dead_head:
            self.timer.stop()
            if self.Ch.on_game_over_deadhead:
                self.Ch.on_game_over_deadhead()

    def bot_move(self, bot):
        if self.possible_move_bot(bot):
            self.clear_list_motions()
            if not self.Ch.list_continue_hack:
                if self.on_motion:
                    self.on_motion()
                    self.check_game_over()
            self.repaint()

    def check_is_player(self, player):
        return player == CC.CheckerColors.black \
               or player == CC.CheckerColors.white

    def possible_move_bot(self, bot):
        if self.Ch.white_motion \
                and bot.color == CC.CheckerColors.white \
                or not self.Ch.white_motion \
                        and bot.color == CC.CheckerColors.black:
            bot.step_ai()
            return True
        else:
            return

    def step_bot(self):
        if not self.check_is_player(self.first_player):
            self.bot_move(self.first_player)
        if not self.check_is_player(self.second_player):
            self.bot_move(self.second_player)

    def step(self):
        x0, y0 = self.step_list[0]
        x, y = self.step_list[1]
        cell = self.Ch.field[x0][y0]
        if cell.color == CC.CheckerColors.black \
                and not self.Ch.white_motion \
                or cell.color == CC.CheckerColors.white \
                        and self.Ch.white_motion:
            if (x0, y0) == (x, y):
                self.step_list = []
                return False
            first_cell = self.Ch.field[x0][y0].number
            second_cell = self.Ch.field[x][y].number
            #if self.client_mode:
                #self.O
            if self.Ch.start_moving(first_cell, second_cell):
                self.clear_list_motions()
                if self.on_motion:
                    self.on_motion()
                self.check_game_over()
                return True
            else:
                self.clear_list_motions()
                self.repaint()
                return False
        else:
            self.step_list.clear()
            return False

    def get_i_j_coors(self, x, y):
        return int(y // self.cell_size), int(x // self.cell_size)

    def draw_board(self, paint, event):
        field = self.Ch.field
        for i in range(len(field)):
            for j in range(len(field[i])):
                if field[i][j].color_cell == CC.CheckerColors.white_cell:
                    self.draw_white_cell(paint, i, j)
                elif field[i][j].color_cell == CC.CheckerColors.black_cell:
                    self.draw_black_cell(paint, i, j)
                    self.draw_possible_mot(paint, i, j)

    def draw_possible_mot(self, paint, x, y):
        self.set_color.setNamedColor(self.possible_move_color)
        paint.setPen(self.set_color)
        paint.setBrush(self.set_color)
        for i in range(len(self.paint_list_motions)):
            for j in range(len(self.paint_list_motions)):
                if self.paint_list_motions[j][i]:
                    x_center = i * self.cell_size + self.cell_size // 2
                    y_center = j * self.cell_size + self.cell_size // 2
                    center = QPoint(x_center, y_center)
                    paint.drawEllipse(center, self.checker_r // 2,
                                      self.checker_r // 2)

    def draw_white_cell(self, paint, x, y):
        self.set_color.setNamedColor(self.white_color_cell)
        paint.setPen(self.set_color)
        paint.setBrush(self.set_color)
        paint.drawRect(x * self.cell_size, y * self.cell_size, self.cell_size,
                       self.cell_size)

    def draw_black_cell(self, paint, x, y):
        self.set_color.setNamedColor(self.black_color_cell)
        paint.setPen(self.set_color)
        paint.setBrush(self.set_color)
        paint.drawRect(x * self.cell_size, y * self.cell_size, self.cell_size,
                       self.cell_size)
        if self.Ch.field[y][x].color == CC.CheckerColors.black and not \
                self.Ch.field[y][x].king:
            self.painting_checkers(paint, x, y, self.black_color_checker, False)
        if self.Ch.field[y][x].color == CC.CheckerColors.white and not \
                self.Ch.field[y][x].king:
            self.painting_checkers(paint, x, y, self.white_color_checker, False)
        if self.Ch.field[y][x].color == CC.CheckerColors.black and \
                self.Ch.field[y][x].king:
            self.painting_checkers(paint, x, y, self.black_color_checker, True)
        if self.Ch.field[y][x].color == CC.CheckerColors.white and \
                self.Ch.field[y][x].king:
            self.painting_checkers(paint, x, y, self.white_color_checker, True)

    def painting_checkers(self, paint, x, y, color, param_king):
        self.set_color.setNamedColor(color)
        paint.setPen(self.set_color)
        paint.setBrush(self.set_color)
        x_center = x * self.cell_size + self.cell_size // 2
        y_center = y * self.cell_size + self.cell_size // 2
        center = QPoint(x_center, y_center)
        paint.drawEllipse(center, self.checker_r, self.checker_r)
        if param_king:
            if color == self.black_color_checker:
                self.set_color.setNamedColor(self.black_color_cell)
                paint.setPen(self.set_color)
                paint.setBrush(self.set_color)
            else:
                self.set_color.setNamedColor(self.white_color_cell)
                paint.setPen(self.set_color)
                paint.setBrush(self.set_color)
            paint.drawEllipse(center, self.checker_r // 2, self.checker_r // 2)

    def new_game(self):
        self.start_window = StartWindow()
        self.start_window.show()
        self.close()
        if self.on_new:
            self.on_new()

    def save_game(self):
        if self.saved_game is None:
            field = self.Ch.field
            self.saved_game = FS.FieldState(field, self.Ch.white_motion,
                                            self.Ch.flag_fight,
                                            self.Ch.list_continue_hack,
                                            self.Ch.white_checkers_count,
                                            self.Ch.black_checkers_count)

    def load_game(self):
        self.Ch.field = deepcopy(self.saved_game.field)
        self.Ch.white_motion = self.saved_game.white_motion
        self.Ch.list_continue_hack = deepcopy(
            self.saved_game.list_continue_hack)
        self.Ch.flag_fight = self.saved_game.flag_fight
        self.Ch.white_checkers_count = self.saved_game.white_checkers
        self.Ch.black_checkers_count = self.saved_game.black_checkers
        self.repaint()

    def exit_game(self):
        QtWidgets.qApp.quit()

    def undo_game(self):
        if not self.ai_vs_ai_flag:
            self.timer.stop()
            self.Ch.undo()
            self.repaint()
            self.timer.start(1000)
        if self.ai_vs_player_flag:
            whos_step_color = CC.CheckerColors.white if self.Ch.white_motion \
                else CC.CheckerColors.black
            if whos_step_color == self.first_player.color:
                self.Ch.undo()
                whos_step_color = CC.CheckerColors.white if self.Ch.white_motion \
                    else CC.CheckerColors.black
                if whos_step_color == self.first_player.color:
                    self.Ch.undo()
                self.repaint()

    def redo_game(self):
        if not self.ai_vs_ai_flag:
            self.timer.stop()
            self.Ch.redo()
            self.repaint()
            self.timer.start(1000)
