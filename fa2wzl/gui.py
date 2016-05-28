import sys
import threading

import time

from PyQt5 import QtWidgets, QtCore, QtGui

from fa2wzl import exceptions
from fa2wzl.fa.session import FASession
from fa2wzl.form import Ui_MainWindow
from fa2wzl.worker import Worker
from fa2wzl.wzl.session import WZLSession


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    # Custom signals
    captcha_loaded = QtCore.pyqtSignal(bytes, name="captchaLoaded")
    login_complete = QtCore.pyqtSignal(name="loginComplete")
    login_failed = QtCore.pyqtSignal(int, name="loginFailed")

    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.app = app

        self.fa_sess = None
        self.wzl_sess = None
        self.worker = None

        # TODO: change this
        self.captcha_loaded.connect(self.set_captcha_image)
        self.btnLogin.clicked.connect(self.login)
        self.login_failed.connect(self._login_failed_handler)
        self.login_complete.connect(self._login_complete_handler)

        self.fa_sess = FASession("")

        self.mutex = threading.Lock()

        self.get_captcha()

    def set_captcha_image(self, img_data):
        byte_array = QtCore.QByteArray(img_data)
        pix = QtGui.QPixmap()
        pix.loadFromData(byte_array)
        self.faCaptchaImg.setPixmap(pix)

    def get_captcha(self):
        def work():
            self.mutex.acquire()
            captcha_data = self.fa_sess.get_captcha()
            self.mutex.release()

            self.captcha_loaded.emit(captcha_data)

        threading.Thread(target=work).start()

    def _login_complete_handler(self):
        self.stackedWidget.setCurrentIndex(1)

    def _login_failed_handler(self, mask):
        msg = ""

        if mask & 0b01:
            msg += "FurAffinity login credentials are incorrect.\n"
        if mask & 0b10:
            msg += "Weasyl API key is invalid."

        qmsg = QtWidgets.QMessageBox()
        qmsg.warning(None, "Login Failed", msg, qmsg.standardButtons())

        self.btnLogin.setEnabled(True)

    def login(self):
        self.btnLogin.setEnabled(False)

        def work():

            username = self.faUsername.text()
            password = self.faPassword.text()
            captcha = self.faCaptcha.text()
            apikey = self.wzlApiKey.text()

            errormask = 0b0

            self.mutex.acquire()
            self.fa_sess.username = username
            try:
                self.fa_sess.login(password, captcha)
            except exceptions.AuthenticationError:
                errormask |= 0b01

            try:
                self.wzl_sess = WZLSession(apikey)
                wzl_username = self.wzl_sess.username
            except exceptions.AuthenticationError:
                errormask |= 0b10

            self.mutex.release()

            if errormask != 0:
                self.login_failed.emit(errormask)
            else:
                self.login_complete.emit()

        threading.Thread(target=work).start()


def main():
    app = QtWidgets.QApplication(sys.argv)

    widget = MainWindow(app)
    widget.show()

    app.exec_()
