#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow
from PyQt5 import QtGui
import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "PyQt5 Push Button"
        left = 500
        top = 200
        width = 640
        height = 480
        icon_name = "home.png"

        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon(icon_name))
        self.setGeometry(left, top, width, height)

        self.setup_ui()

        self.show()

    def setup_ui(self):
        button = QPushButton('Click Me', self)
        button.move(100, 100)


def main():
    print('hi there')
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())

if __name__ == "__main__":
    main()
