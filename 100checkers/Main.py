import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from Game import GameWindows

if __name__ == "__main__":
    
    QtWidgets.QApplication.addLibraryPath(".")
    app = QApplication(sys.argv)
    game = GameWindows.StartWindow()
    game.show()
    sys.exit(app.exec_())
