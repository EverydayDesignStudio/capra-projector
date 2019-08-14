#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QPushButton, QDialog, QGroupBox, QHBoxLayout, QVBoxLayout
from PyQt5 import QtGui, QtCore
import sys


class Window(QDialog):
    def __init__(self):
        super().__init__()

        title = "PyQt5 Layout Management"
        left = 500
        top = 200
        width = 600
        height = 100
        icon_name = "home.png"

        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon(icon_name))
        self.setGeometry(left, top, width, height)

        # self.setup_button()
        self.create_layout()

        self.show()

    def create_layout(self):
        self.group_box = QGroupBox('What is your favorite ice cream?')
        hbox_layout = QHBoxLayout()

        # button 1
        button = QPushButton('Moose Tracks', self)
        # button.setGeometry(QtCore.QRect(50, 50, 200, 50))
        button.setIconSize(QtCore.QSize(20, 40))
        button.setMinimumHeight(40)
        hbox_layout.addWidget(button)

        # button 2
        button2 = QPushButton('Mint Chocolate Chip', self)
        # button2.setGeometry(QtCore.QRect(300, 50, 200, 50))
        button2.setIconSize(QtCore.QSize(20, 40))
        button2.setMinimumHeight(40)
        hbox_layout.addWidget(button2)

        # button 2
        button3 = QPushButton('Mint Chocolate Chip', self)
        # button3.setGeometry(QtCore.QRect(300, 50, 200, 50))
        button3.setIconSize(QtCore.QSize(20, 40))
        button3.setMinimumHeight(40)
        hbox_layout.addWidget(button3)

        self.group_box.setLayout(hbox_layout)


    # def setup_button(self):
    #     button.clicked.connect(self.click_me)

    # def click_me(self):
    #     print('Hello World')


def main():
    print('hi there')
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())

if __name__ == "__main__":
    main()