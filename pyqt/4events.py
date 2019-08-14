#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow
from PyQt5 import QtGui, QtCore
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "PyQt5 Events and Signals"
        left = 500
        top = 200
        width = 640
        height = 480
        icon_name = "home.png"

        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon(icon_name))
        self.setGeometry(left, top, width, height)

        self.setup_button()

        self.show()

    def setup_button(self):
        button = QPushButton('Click Me', self)
        # button.move(100, 100)
        button.setGeometry(QtCore.QRect(100, 100, 110, 50))
        button.setIcon(QtGui.QIcon('icon.png'))
        button.setIconSize(QtCore.QSize(20, 40))
        button.setToolTip('This is a button')

        button.clicked.connect(self.click_me)

    def click_me(self):
        print('Hello World')


def main():
    print('hi there')
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())

if __name__ == "__main__":
    main()