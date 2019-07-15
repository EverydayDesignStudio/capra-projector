#!/usr/bin/env python3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

Form, Window = uic.loadUiType('sample1.ui')

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()
app.exec_()
