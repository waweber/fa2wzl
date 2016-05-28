import sys
from PyQt5 import QtWidgets

from fa2wzl.form import Ui_mainUi

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_mainUi()
    ui.setupUi(widget)

    ui.stackedWidget.setCurrentIndex(0)

    widget.show()

    exit(app.exec_())
