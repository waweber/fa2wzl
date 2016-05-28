from PyQt5.QtWidgets import QTreeWidget


class CustomDropTreeWidget(QTreeWidget):
    def dropEvent(self, QDropEvent):
        QDropEvent.ignore()
        print("DROP")