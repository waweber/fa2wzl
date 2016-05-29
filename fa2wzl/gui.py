import sys
import threading

import time

from PyQt5 import QtWidgets, QtCore, QtGui

from fa2wzl import exceptions
from fa2wzl.fa.session import FASession
from fa2wzl.form import Ui_MainWindow
from fa2wzl.wzl.session import WZLSession


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)


def main():
    app = QtWidgets.QApplication(sys.argv)

    widget = MainWindow(app)
    widget.show()

    app.exec_()
