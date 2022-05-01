from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel,QTextEdit, QPushButton
from PyQt5 import uic
import sys


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        uic.loadUi("main_window.ui", self)
        self.show()


app = QApplication(sys.argv)
UiWINDOW = UI()
app.exec_()
