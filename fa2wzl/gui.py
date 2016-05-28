import sys
import threading

import time

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

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

    folders_loaded = QtCore.pyqtSignal(name="foldersLoaded")

    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.app = app

        self.fa_sess = None
        self.wzl_sess = None
        self.worker = None

        self.fa_folder_items = {}
        self.wzl_folder_items = {}

        # TODO: change this
        self.captcha_loaded.connect(self._set_captcha_image)
        self.btnLogin.clicked.connect(self._login)
        self.login_failed.connect(self._login_failed_handler)
        self.login_complete.connect(self._login_complete_handler)
        self.folders_loaded.connect(self._folders_loaded)

        self.fa_sess = FASession("")

        self.mutex = threading.Lock()

        self._get_captcha()

    def _set_captcha_image(self, img_data):
        byte_array = QtCore.QByteArray(img_data)
        pix = QtGui.QPixmap()
        pix.loadFromData(byte_array)
        self.faCaptchaImg.setPixmap(pix)

    def _get_captcha(self):
        def work():
            self.mutex.acquire()
            captcha_data = self.fa_sess.get_captcha()
            self.mutex.release()

            self.captcha_loaded.emit(captcha_data)

        threading.Thread(target=work).start()

    def _login_complete_handler(self):
        self.stackedWidget.setCurrentIndex(1)
        self.statusbar.showMessage("Loading folders")
        self.worker = Worker(self.fa_sess, self.wzl_sess)

        def work():
            with self.mutex:
                self.worker.map_folders()

            self.folders_loaded.emit()

        threading.Thread(target=work).start()

    def _folders_loaded(self):

        fa_root_items = []
        fa_folder_items = {}

        wzl_root_items = []
        wzl_folder_items = {}

        with self.mutex:
            for folder in self.fa_sess.folders:
                item = QtWidgets.QTreeWidgetItem()
                item.setText(0, folder.title)
                fa_folder_items[folder] = item
                fa_root_items.append(item)

                for subfolder in folder.children:
                    subitem = QtWidgets.QTreeWidgetItem()
                    subitem.setText(0, subfolder.title)
                    fa_folder_items[subfolder] = subitem
                    item.addChild(subitem)

            for folder in self.wzl_sess.folders:
                item = QtWidgets.QTreeWidgetItem()
                item.setText(0, folder.title)
                wzl_folder_items[folder] = item
                wzl_root_items.append(item)

                for subfolder in folder.children:
                    subitem = QtWidgets.QTreeWidgetItem()
                    subitem.setText(0, subfolder.title)
                    wzl_folder_items[subfolder] = subitem
                    item.addChild(subitem)

            for folder in self.fa_sess.folders:
                if folder in self.worker.folder_mapping.keys():
                    item = wzl_folder_items[self.worker.folder_mapping[folder]]
                else:
                    item = QtWidgets.QTreeWidgetItem()
                    item.setForeground(0, QtGui.QColor(0, 180, 0))
                    item.setText(0, folder.title + "*")
                    wzl_folder_items[folder] = item
                    wzl_root_items.append(item)

                for subfolder in folder.children:
                    if subfolder in self.worker.folder_mapping.keys():
                        continue

                    subitem = QtWidgets.QTreeWidgetItem()
                    subitem.setForeground(0, QtGui.QColor(0, 180, 0))
                    subitem.setText(0, subfolder.title + "*")
                    wzl_folder_items[subfolder] = subitem
                    item.addChild(subitem)

        self.faFolders.clear()
        self.wzlFolders.clear()

        for item in fa_root_items:
            self.faFolders.invisibleRootItem().addChild(item)

        for item in wzl_root_items:
            self.wzlFolders.invisibleRootItem().addChild(item)

        self.fa_folder_items = fa_folder_items
        self.wzl_folder_items = wzl_folder_items

        self.statusbar.clearMessage()
        self.btnCreateFolders.setEnabled(True)
        self.btnResetFolders.setEnabled(True)

    def _login_failed_handler(self, mask):
        msg = ""

        if mask & 0b01:
            msg += "FurAffinity login credentials are incorrect.\n"
        if mask & 0b10:
            msg += "Weasyl API key is invalid."

        qmsg = QtWidgets.QMessageBox()
        qmsg.warning(None, "Login Failed", msg, qmsg.standardButtons())

        self.faUsername.setEnabled(True)
        self.faPassword.setEnabled(True)
        self.faCaptcha.setEnabled(True)
        self.wzlApiKey.setEnabled(True)
        self.btnLogin.setEnabled(True)
        self.statusbar.clearMessage()

    def _login(self):
        self.faUsername.setEnabled(False)
        self.faPassword.setEnabled(False)
        self.faCaptcha.setEnabled(False)
        self.wzlApiKey.setEnabled(False)
        self.btnLogin.setEnabled(False)

        self.statusbar.showMessage("Logging In")

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

    def __del__(self):
        self.fa_sess.logout()


def main():
    app = QtWidgets.QApplication(sys.argv)

    widget = MainWindow(app)
    widget.show()

    app.exec_()
