# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms/form.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 490)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.loginPage = QtWidgets.QWidget()
        self.loginPage.setObjectName("loginPage")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.loginPage)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_14 = QtWidgets.QLabel(self.loginPage)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_11.addWidget(self.label_14)
        self.label_15 = QtWidgets.QLabel(self.loginPage)
        self.label_15.setObjectName("label_15")
        self.verticalLayout_11.addWidget(self.label_15)
        self.groupBox_10 = QtWidgets.QGroupBox(self.loginPage)
        self.groupBox_10.setObjectName("groupBox_10")
        self.formLayout_5 = QtWidgets.QFormLayout(self.groupBox_10)
        self.formLayout_5.setObjectName("formLayout_5")
        self.label_16 = QtWidgets.QLabel(self.groupBox_10)
        self.label_16.setObjectName("label_16")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_16)
        self.faUsername = QtWidgets.QLineEdit(self.groupBox_10)
        self.faUsername.setObjectName("faUsername")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.faUsername)
        self.label_17 = QtWidgets.QLabel(self.groupBox_10)
        self.label_17.setObjectName("label_17")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_17)
        self.faPassword = QtWidgets.QLineEdit(self.groupBox_10)
        self.faPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.faPassword.setObjectName("faPassword")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.faPassword)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.faCaptchaImg = QtWidgets.QLabel(self.groupBox_10)
        self.faCaptchaImg.setMinimumSize(QtCore.QSize(120, 60))
        self.faCaptchaImg.setObjectName("faCaptchaImg")
        self.horizontalLayout_7.addWidget(self.faCaptchaImg)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.formLayout_5.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_7)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_5.setItem(2, QtWidgets.QFormLayout.LabelRole, spacerItem1)
        self.label_18 = QtWidgets.QLabel(self.groupBox_10)
        self.label_18.setObjectName("label_18")
        self.formLayout_5.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_18)
        self.faCaptcha = QtWidgets.QLineEdit(self.groupBox_10)
        self.faCaptcha.setObjectName("faCaptcha")
        self.formLayout_5.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.faCaptcha)
        self.verticalLayout_11.addWidget(self.groupBox_10)
        self.groupBox_11 = QtWidgets.QGroupBox(self.loginPage)
        self.groupBox_11.setObjectName("groupBox_11")
        self.formLayout_6 = QtWidgets.QFormLayout(self.groupBox_11)
        self.formLayout_6.setObjectName("formLayout_6")
        self.label_19 = QtWidgets.QLabel(self.groupBox_11)
        self.label_19.setObjectName("label_19")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_19)
        self.wzlApiKey = QtWidgets.QLineEdit(self.groupBox_11)
        self.wzlApiKey.setObjectName("wzlApiKey")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.wzlApiKey)
        self.verticalLayout_11.addWidget(self.groupBox_11)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_11.addItem(spacerItem2)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem3)
        self.btnLogin = QtWidgets.QPushButton(self.loginPage)
        self.btnLogin.setObjectName("btnLogin")
        self.horizontalLayout_8.addWidget(self.btnLogin)
        self.verticalLayout_11.addLayout(self.horizontalLayout_8)
        self.stackedWidget.addWidget(self.loginPage)
        self.folderPage_2 = QtWidgets.QWidget()
        self.folderPage_2.setObjectName("folderPage_2")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.folderPage_2)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.label_20 = QtWidgets.QLabel(self.folderPage_2)
        self.label_20.setObjectName("label_20")
        self.verticalLayout_12.addWidget(self.label_20)
        self.label_21 = QtWidgets.QLabel(self.folderPage_2)
        self.label_21.setTextFormat(QtCore.Qt.AutoText)
        self.label_21.setWordWrap(True)
        self.label_21.setObjectName("label_21")
        self.verticalLayout_12.addWidget(self.label_21)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.groupBox_12 = QtWidgets.QGroupBox(self.folderPage_2)
        self.groupBox_12.setObjectName("groupBox_12")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.groupBox_12)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.faFolders = QtWidgets.QTreeWidget(self.groupBox_12)
        self.faFolders.setDragEnabled(False)
        self.faFolders.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.faFolders.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.faFolders.setAutoExpandDelay(-1)
        self.faFolders.setItemsExpandable(True)
        self.faFolders.setColumnCount(1)
        self.faFolders.setObjectName("faFolders")
        self.faFolders.headerItem().setText(0, "Folder Name")
        self.verticalLayout_13.addWidget(self.faFolders)
        self.horizontalLayout_9.addWidget(self.groupBox_12)
        self.groupBox_13 = QtWidgets.QGroupBox(self.folderPage_2)
        self.groupBox_13.setObjectName("groupBox_13")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.groupBox_13)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.wzlFolders = FolderTree(self.groupBox_13)
        self.wzlFolders.setDragEnabled(True)
        self.wzlFolders.setDragDropOverwriteMode(True)
        self.wzlFolders.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.wzlFolders.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.wzlFolders.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.wzlFolders.setAutoExpandDelay(-1)
        self.wzlFolders.setItemsExpandable(True)
        self.wzlFolders.setObjectName("wzlFolders")
        self.wzlFolders.headerItem().setText(0, "Folder Name")
        self.verticalLayout_14.addWidget(self.wzlFolders)
        self.horizontalLayout_9.addWidget(self.groupBox_13)
        self.verticalLayout_12.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.btnResetFolders = QtWidgets.QPushButton(self.folderPage_2)
        self.btnResetFolders.setEnabled(False)
        self.btnResetFolders.setObjectName("btnResetFolders")
        self.horizontalLayout_10.addWidget(self.btnResetFolders)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem4)
        self.btnCreateFolders = QtWidgets.QPushButton(self.folderPage_2)
        self.btnCreateFolders.setEnabled(False)
        self.btnCreateFolders.setObjectName("btnCreateFolders")
        self.horizontalLayout_10.addWidget(self.btnCreateFolders)
        self.verticalLayout_12.addLayout(self.horizontalLayout_10)
        self.stackedWidget.addWidget(self.folderPage_2)
        self.submissionPage_2 = QtWidgets.QWidget()
        self.submissionPage_2.setObjectName("submissionPage_2")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.submissionPage_2)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.label_23 = QtWidgets.QLabel(self.submissionPage_2)
        self.label_23.setObjectName("label_23")
        self.verticalLayout_15.addWidget(self.label_23)
        self.label_24 = QtWidgets.QLabel(self.submissionPage_2)
        self.label_24.setWordWrap(True)
        self.label_24.setObjectName("label_24")
        self.verticalLayout_15.addWidget(self.label_24)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.groupBox_15 = QtWidgets.QGroupBox(self.submissionPage_2)
        self.groupBox_15.setObjectName("groupBox_15")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.groupBox_15)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.faSubmissions = QtWidgets.QTreeWidget(self.groupBox_15)
        self.faSubmissions.setObjectName("faSubmissions")
        self.faSubmissions.headerItem().setText(0, "Submission Title")
        self.verticalLayout_16.addWidget(self.faSubmissions)
        self.horizontalLayout_11.addWidget(self.groupBox_15)
        self.groupBox_16 = QtWidgets.QGroupBox(self.submissionPage_2)
        self.groupBox_16.setObjectName("groupBox_16")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.groupBox_16)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.wzlSubmissions = SubmissionTree(self.groupBox_16)
        self.wzlSubmissions.setDragEnabled(True)
        self.wzlSubmissions.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.wzlSubmissions.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.wzlSubmissions.setObjectName("wzlSubmissions")
        self.wzlSubmissions.headerItem().setText(0, "Submission Title")
        self.verticalLayout_17.addWidget(self.wzlSubmissions)
        self.horizontalLayout_11.addWidget(self.groupBox_16)
        self.groupBox_17 = QtWidgets.QGroupBox(self.submissionPage_2)
        self.groupBox_17.setObjectName("groupBox_17")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.groupBox_17)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.submissionPreview = QtWidgets.QLabel(self.groupBox_17)
        self.submissionPreview.setMaximumSize(QtCore.QSize(200, 200))
        self.submissionPreview.setObjectName("submissionPreview")
        self.verticalLayout_18.addWidget(self.submissionPreview)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_18.addItem(spacerItem5)
        self.horizontalLayout_11.addWidget(self.groupBox_17)
        self.verticalLayout_15.addLayout(self.horizontalLayout_11)
        self.groupBox_18 = QtWidgets.QGroupBox(self.submissionPage_2)
        self.groupBox_18.setObjectName("groupBox_18")
        self.formLayout_8 = QtWidgets.QFormLayout(self.groupBox_18)
        self.formLayout_8.setObjectName("formLayout_8")
        self.label_25 = QtWidgets.QLabel(self.groupBox_18)
        self.label_25.setObjectName("label_25")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_25)
        self.btnDelay = QtWidgets.QSpinBox(self.groupBox_18)
        self.btnDelay.setMinimum(1)
        self.btnDelay.setObjectName("btnDelay")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.btnDelay)
        self.label = QtWidgets.QLabel(self.groupBox_18)
        self.label.setObjectName("label")
        self.formLayout_8.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.btnGenerateNotifications = QtWidgets.QCheckBox(self.groupBox_18)
        self.btnGenerateNotifications.setText("")
        self.btnGenerateNotifications.setObjectName("btnGenerateNotifications")
        self.formLayout_8.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.btnGenerateNotifications)
        self.verticalLayout_15.addWidget(self.groupBox_18)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.btnResetSubmissions = QtWidgets.QPushButton(self.submissionPage_2)
        self.btnResetSubmissions.setEnabled(False)
        self.btnResetSubmissions.setObjectName("btnResetSubmissions")
        self.horizontalLayout_12.addWidget(self.btnResetSubmissions)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem6)
        self.btnCreateSubmissions = QtWidgets.QPushButton(self.submissionPage_2)
        self.btnCreateSubmissions.setEnabled(False)
        self.btnCreateSubmissions.setObjectName("btnCreateSubmissions")
        self.horizontalLayout_12.addWidget(self.btnCreateSubmissions)
        self.verticalLayout_15.addLayout(self.horizontalLayout_12)
        self.stackedWidget.addWidget(self.submissionPage_2)
        self.progressPage_2 = QtWidgets.QWidget()
        self.progressPage_2.setObjectName("progressPage_2")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.progressPage_2)
        self.verticalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.label_26 = QtWidgets.QLabel(self.progressPage_2)
        self.label_26.setObjectName("label_26")
        self.verticalLayout_19.addWidget(self.label_26)
        self.overallProgress = QtWidgets.QProgressBar(self.progressPage_2)
        self.overallProgress.setProperty("value", 24)
        self.overallProgress.setObjectName("overallProgress")
        self.verticalLayout_19.addWidget(self.overallProgress)
        self.waitProgress = QtWidgets.QProgressBar(self.progressPage_2)
        self.waitProgress.setProperty("value", 24)
        self.waitProgress.setTextVisible(False)
        self.waitProgress.setObjectName("waitProgress")
        self.verticalLayout_19.addWidget(self.waitProgress)
        self.log = QtWidgets.QTextEdit(self.progressPage_2)
        self.log.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.log.setReadOnly(True)
        self.log.setObjectName("log")
        self.verticalLayout_19.addWidget(self.log)
        self.stackedWidget.addWidget(self.progressPage_2)
        self.verticalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FurAffinity To Weasyl"))
        self.label_14.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt;\">Authenticate</span></p></body></html>"))
        self.label_15.setText(_translate("MainWindow", "<html><head/><body><p>Enter your FurAffinity credentials, and a Weasyl API key.</p></body></html>"))
        self.groupBox_10.setTitle(_translate("MainWindow", "FurAffinity Login"))
        self.label_16.setText(_translate("MainWindow", "Username:"))
        self.label_17.setText(_translate("MainWindow", "Password:"))
        self.faCaptchaImg.setText(_translate("MainWindow", "Image"))
        self.label_18.setText(_translate("MainWindow", "CAPTCHA:"))
        self.groupBox_11.setTitle(_translate("MainWindow", "Weasyl Login"))
        self.label_19.setText(_translate("MainWindow", "API Key:"))
        self.btnLogin.setText(_translate("MainWindow", "Log In"))
        self.label_20.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt;\">Folders</span></p></body></html>"))
        self.label_21.setText(_translate("MainWindow", "<html><head/><body><p>Copy your gallery folder structure from FurAffinity to Weasyl. The tree on the right shows the final structure. Items in green will be created. You may drag a new folder onto an existing folder to merge them together.</p></body></html>"))
        self.groupBox_12.setTitle(_translate("MainWindow", "FurAffinity Folders"))
        self.groupBox_13.setTitle(_translate("MainWindow", "Weasyl Folders"))
        self.wzlFolders.headerItem().setText(1, _translate("MainWindow", "FA Folders"))
        self.btnResetFolders.setText(_translate("MainWindow", "Reset"))
        self.btnCreateFolders.setText(_translate("MainWindow", "Create Folders"))
        self.label_23.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt;\">Submissions</span></p></body></html>"))
        self.label_24.setText(_translate("MainWindow", "<html><head/><body><p>Copy submissions from FurAffinity to Weasyl. The final result will be displayed on the right. Items in green will be created. You may drag new submissions into different folders to change their destination. Weasyl only supports sorting submissions into at most one folder.</p></body></html>"))
        self.groupBox_15.setTitle(_translate("MainWindow", "FurAffinity Submissions"))
        self.groupBox_16.setTitle(_translate("MainWindow", "Weasyl Submissions"))
        self.wzlSubmissions.headerItem().setText(1, _translate("MainWindow", "FA Submission"))
        self.groupBox_17.setTitle(_translate("MainWindow", "Submission Info"))
        self.submissionPreview.setText(_translate("MainWindow", "Preview"))
        self.groupBox_18.setTitle(_translate("MainWindow", "Upload Settings"))
        self.label_25.setText(_translate("MainWindow", "Minutes To Wait Between Uploads:"))
        self.label.setText(_translate("MainWindow", "Generate Notifications:"))
        self.btnResetSubmissions.setText(_translate("MainWindow", "Reset"))
        self.btnCreateSubmissions.setText(_translate("MainWindow", "Upload"))
        self.label_26.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt;\">Copying Gallery</span></p></body></html>"))

from fa2wzl.widget import FolderTree, SubmissionTree
