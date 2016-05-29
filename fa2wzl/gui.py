import sys
import threading

import time

from PyQt5 import QtWidgets, QtCore, QtGui

from fa2wzl import exceptions, compare
from fa2wzl.fa.session import FASession
from fa2wzl.form import Ui_MainWindow
from fa2wzl.wzl.session import WZLSession


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    # Custom signals
    captcha_loaded = QtCore.pyqtSignal(bytes, name="captchaLoaded")
    login_complete = QtCore.pyqtSignal(bool, str, name="loginComplete")
    folders_loaded = QtCore.pyqtSignal(name="foldersLoaded")
    folders_created = QtCore.pyqtSignal(name="foldersCreated")
    submissions_loaded = QtCore.pyqtSignal(name="submissionsLoaded")

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # Session stuff
        self.lock = threading.Lock()
        self.fa_sess = FASession("")
        self.wzl_sess = None

        self.folder_mapping = {}
        self.submission_mapping = {}

        # Signals/slots
        self.captcha_loaded.connect(self._set_captcha_img)
        self.btnLogin.clicked.connect(self._login)
        self.login_complete.connect(self._login_complete)
        self.folders_loaded.connect(self._folders_loaded)
        self.wzlFolders.folder_dropped.connect(self._folder_dropped)
        self.btnResetFolders.clicked.connect(self._reload_folders)
        self.btnCreateFolders.clicked.connect(self._create_folders)
        self.folders_created.connect(self._folders_created)
        self.submissions_loaded.connect(self._submissions_loaded)

        self._load_captcha()

    def _load_captcha(self):
        def work():
            with self.lock:
                captcha = self.fa_sess.get_captcha()
            self.captcha_loaded.emit(captcha)

        threading.Thread(target=work).start()

    def _set_captcha_img(self, data):
        bytes = QtCore.QByteArray(data)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(bytes)
        self.faCaptchaImg.setPixmap(pixmap)

    def _login(self):
        self._set_login_inputs_enabled(False)

        def work():

            fa_user = self.faUsername.text()
            fa_pwd = self.faPassword.text()
            fa_captcha = self.faCaptcha.text()
            wzl_key = self.wzlApiKey.text()

            fa_error = False
            wzl_error = False

            with self.lock:
                try:
                    self.fa_sess.username = fa_user
                    self.fa_sess.login(fa_pwd, fa_captcha)
                except exceptions.AuthenticationError:
                    fa_error = True

                try:
                    self.wzl_sess = WZLSession(wzl_key)
                    wzl_user = self.wzl_sess.username
                except exceptions.AuthenticationError:
                    wzl_error = True

            msg = ""

            if fa_error:
                msg += "FurAffinity credentials incorrect.\n"
            if wzl_error:
                msg += "Weasyl API key incorrect.\n"

            self.login_complete.emit(fa_error or wzl_error, msg)

        self.statusbar.showMessage("Logging in")
        threading.Thread(target=work).start()

    def _login_complete(self, error, msg):
        self._set_login_inputs_enabled(True)

        if error:
            box = QtWidgets.QMessageBox()
            box.warning(None, "Login Failed", msg, QtWidgets.QMessageBox.Ok)
            self.statusbar.clearMessage()
        else:
            self.stackedWidget.setCurrentIndex(1)
            self._load_folders()

    def _set_login_inputs_enabled(self, enabled):
        self.faUsername.setEnabled(enabled)
        self.faPassword.setEnabled(enabled)
        self.faCaptcha.setEnabled(enabled)
        self.wzlApiKey.setEnabled(enabled)
        self.btnLogin.setEnabled(enabled)

    def _load_folders(self):
        def work():
            with self.lock:
                mapping_list = compare.map_folders(self.fa_sess.folders,
                                                   self.wzl_sess.folders)

                self.folder_mapping = {fa_folder: wzl_folder for
                                       fa_folder, wzl_folder in mapping_list}

            self.folders_loaded.emit()

        self.statusbar.showMessage("Loading folders")
        threading.Thread(target=work).start()

    def _folders_loaded(self):
        self.statusbar.clearMessage()
        self._render_folders()
        self.btnCreateFolders.setEnabled(True)
        self.btnResetFolders.setEnabled(True)

    def _reload_folders(self):
        self.btnCreateFolders.setEnabled(False)
        self.btnResetFolders.setEnabled(False)
        self._load_folders()

    def _render_folders(self):

        fa_items = []
        wzl_items = []
        folder_item_mapping = {}

        with self.lock:
            # Populate each site's folders
            for folder in self.fa_sess.folders:
                item = QtWidgets.QTreeWidgetItem()
                item.setData(0, QtCore.Qt.UserRole, folder)
                item.setText(0, folder.title)
                fa_items.append(item)

                for subfolder in folder.children:
                    subitem = QtWidgets.QTreeWidgetItem()
                    subitem.setData(0, QtCore.Qt.UserRole, subfolder)
                    subitem.setText(0, subfolder.title)
                    item.addChild(subitem)

            for folder in self.wzl_sess.folders:
                item = QtWidgets.QTreeWidgetItem()
                item.setData(0, QtCore.Qt.UserRole, folder)
                mappings = []

                for fa_folder, wzl_folder in self.folder_mapping.items():
                    if wzl_folder is folder:
                        mappings.append(fa_folder.title)

                item.setText(0, "%s (%s)" % (folder.title, ", ".join(mappings)))
                folder_item_mapping[folder] = item
                wzl_items.append(item)

                for subfolder in folder.children:
                    subitem = QtWidgets.QTreeWidgetItem()
                    subitem.setData(0, QtCore.Qt.UserRole, subfolder)

                    mappings = []

                    for fa_folder, wzl_folder in self.folder_mapping.items():
                        if wzl_folder is subfolder:
                            mappings.append(fa_folder.title)

                    subitem.setText(0, "%s (%s)" % (
                        subfolder.title, ", ".join(mappings)))

                    item.addChild(subitem)

            # Populate unmapped folders
            for folder in self.fa_sess.folders:
                if folder in self.folder_mapping.keys():
                    item = folder_item_mapping[self.folder_mapping[folder]]
                else:
                    item = QtWidgets.QTreeWidgetItem()
                    item.setData(0, QtCore.Qt.UserRole, folder)
                    item.setText(0, folder.title + "*")
                    item.setForeground(0, QtGui.QColor(0, 150, 0))
                    folder_item_mapping[folder] = item
                    wzl_items.append(item)

                for subfolder in folder.children:
                    if subfolder in self.folder_mapping.keys():
                        continue

                    subitem = QtWidgets.QTreeWidgetItem()
                    subitem.setData(0, QtCore.Qt.UserRole, subfolder)
                    subitem.setText(0, subfolder.title + "*")
                    subitem.setForeground(0, QtGui.QColor(0, 150, 0))
                    item.addChild(subitem)

        self.faFolders.clear()
        for item in fa_items:
            self.faFolders.invisibleRootItem().addChild(item)

        self.wzlFolders.clear()
        for item in wzl_items:
            self.wzlFolders.invisibleRootItem().addChild(item)

    def _folder_dropped(self, src_id, wzl_folder):
        folders = {}

        with self.lock:
            for folder in self.fa_sess.folders:
                folders[folder.id] = folder
                for subfolder in folder.children:
                    folders[subfolder.id] = subfolder

            src_folder = folders[src_id]

            self.folder_mapping[src_folder] = wzl_folder

        self._render_folders()

    def _create_folders(self):
        def work():
            with self.lock:
                mapping = [(fa_folder, wzl_folder) for fa_folder, wzl_folder in
                           self.folder_mapping.items()]

                compare.create_unmapped_folders(
                    self.fa_sess,
                    self.wzl_sess,
                    mapping,
                )

            self.folders_created.emit()

        self.btnResetFolders.setEnabled(False)
        self.btnCreateFolders.setEnabled(False)

        self.statusbar.showMessage("Creating folders")
        threading.Thread(target=work).start()

    def _folders_created(self):
        self.statusbar.clearMessage()
        self.stackedWidget.setCurrentIndex(2)
        self._load_submissions()

    def _load_submissions(self):
        def work():
            with self.lock:
                fa_gallery = self.fa_sess.gallery
                fa_scraps = self.fa_sess.scraps
                wzl_gallery = self.wzl_sess.gallery

                mapping = compare.map_submissions(fa_gallery + fa_scraps,
                                                  wzl_gallery)
                print("Mapping: %r" % mapping)

                self.submission_mapping = {f: w for f, w in mapping}

            self.submissions_loaded.emit()

        self.statusbar.showMessage("Loading submissions")
        threading.Thread(target=work).start()

    def _submissions_loaded(self):
        self.statusbar.clearMessage()
        self._render_submissions()

    def _render_submissions(self):
        wzl_items = []

        folder_items = {}
        submission_items = {}

        with self.lock:

            # Remap folders
            folder_mapping = compare.map_folders(self.fa_sess.folders,
                                                 self.wzl_sess.folders)
            self.folder_mapping = {f: w for f, w in folder_mapping}

            # Create folders
            item = QtWidgets.QTreeWidgetItem()
            item.setData(0, QtCore.Qt.UserRole, None)
            item.setText(0, "Gallery")
            fa_gallery_folder = item

            item = QtWidgets.QTreeWidgetItem()
            item.setData(0, QtCore.Qt.UserRole, None)
            item.setText(0, "Scraps")
            fa_scraps_folder = item

            # FA Folders
            for folder in self.fa_sess.folders:
                item = QtWidgets.QTreeWidgetItem()
                item.setData(0, QtCore.Qt.UserRole, folder)
                item.setText(0, folder.title)
                folder_items[folder] = item
                fa_gallery_folder.addChild(item)

                parent_item = item

                for submission in folder.submissions:
                    item = QtWidgets.QTreeWidgetItem()
                    item.setData(0, QtCore.Qt.UserRole, submission)
                    item.setText(0, submission.title)
                    parent_item.addChild(item)

                for subfolder in folder.children:
                    item = QtWidgets.QTreeWidgetItem()
                    item.setData(0, QtCore.Qt.UserRole, subfolder)
                    item.setText(0, subfolder.title)
                    folder_items[subfolder] = item
                    parent_item.addChild(item)

                    subfolder_item = item

                    for submission in subfolder.submissions:
                        item = QtWidgets.QTreeWidgetItem()
                        item.setData(0, QtCore.Qt.UserRole, submission)
                        item.setText(0, submission.title)
                        subfolder_item.addChild(item)

            # FA gallery
            for submission in self.fa_sess.gallery:
                item = QtWidgets.QTreeWidgetItem()
                item.setData(0, QtCore.Qt.UserRole, submission)
                item.setText(0, submission.title)
                fa_gallery_folder.addChild(item)

            # FA Scraps
            for submission in self.fa_sess.scraps:
                item = QtWidgets.QTreeWidgetItem()
                item.setData(0, QtCore.Qt.UserRole, submission)
                item.setText(0, submission.title)
                fa_scraps_folder.addChild(item)

            wzl_subs_in_root = set(self.wzl_sess.gallery)

            # WZL Folder
            for folder in self.wzl_sess.folders:
                item = QtWidgets.QTreeWidgetItem()
                item.setData(0, QtCore.Qt.UserRole, folder)
                item.setText(0, folder.title)
                folder_items[folder] = item
                wzl_items.append(item)

                parent_item = item

                for submission in folder.submissions:
                    item = QtWidgets.QTreeWidgetItem()
                    item.setData(0, QtCore.Qt.UserRole, submission)

                    item.setText(0, submission.title)

                    for f_s, w_s in self.submission_mapping.items():
                        if w_s is submission:
                            item.setText(0, "%s (%s)" % (
                                submission.title, f_s.title))

                    wzl_subs_in_root.remove(submission)

                    parent_item.addChild(item)

                for subfolder in folder.children:
                    item = QtWidgets.QTreeWidgetItem()
                    item.setData(0, QtCore.Qt.UserRole, subfolder)
                    item.setText(0, subfolder.title)
                    folder_items[subfolder] = item
                    parent_item.addChild(item)

                    subfolder_item = item

                    for submission in subfolder.submissions:
                        item = QtWidgets.QTreeWidgetItem()
                        item.setData(0, QtCore.Qt.UserRole, submission)

                        item.setText(0, submission.title)

                        for f_s, w_s in self.submision_mapping.items():
                            if w_s is submission:
                                item.setText(0, "%s (%s)" % (
                                    submission.title, f_s.title))

                        wzl_subs_in_root.remove(submission)

                        subfolder_item.addChild(item)

            # WZL root
            for submission in wzl_subs_in_root:
                item = QtWidgets.QTreeWidgetItem()
                item.setData(0, QtCore.Qt.UserRole, submission)

                item.setText(0, submission.title)

                for f_s, w_s in self.submission_mapping.items():
                    if w_s is submission:
                        item.setText(0, "%s (%s)" % (
                            submission.title, f_s.title))

                wzl_items.append(item)

            # Now add unmapped submissions
            unmapped_subs = compare.get_unmapped_submissions(
                self.fa_sess.gallery + self.fa_sess.scraps,
                [(f, w) for f, w in self.submission_mapping.items()])

            wzl_subs_in_root.clear()
            wzl_subs_in_root.update(unmapped_subs)

            print("Unmapped: %r" % unmapped_subs)

            assoc = compare.associate_submissions_with_folders(self.fa_sess,
                                                               unmapped_subs,
                                                               [(f, w) for f, w
                                                                in
                                                                self.folder_mapping.items()])

            for submission, folder in assoc:
                folder_item = folder_items[folder]

                item = QtWidgets.QTreeWidgetItem()
                item.setData(0, QtCore.Qt.UserRole, submission)
                item.setText(0, submission.title + "*")
                item.setForeground(0, QtGui.QColor(0, 150, 0))
                folder_item.addChild(item)

                wzl_subs_in_root.remove(submission)

            for submission in wzl_subs_in_root:
                item = QtWidgets.QTreeWidgetItem()
                item.setData(0, QtCore.Qt.UserRole, submission)
                item.setText(0, submission.title + "*")
                item.setForeground(0, QtGui.QColor(0, 150, 0))

                wzl_items.append(item)

        self.faSubmissions.clear()
        self.faSubmissions.invisibleRootItem().addChild(fa_gallery_folder)
        self.faSubmissions.invisibleRootItem().addChild(fa_scraps_folder)

        self.wzlSubmissions.clear()
        for item in wzl_items:
            self.wzlSubmissions.invisibleRootItem().addChild(item)

    def __del__(self):
        self.fa_sess.logout()


def main():
    app = QtWidgets.QApplication(sys.argv)

    widget = MainWindow()
    widget.show()

    try:
        code = app.exec_()
        exit(code)
    except Exception:
        exit(1)
