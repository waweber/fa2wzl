from PyQt5 import QtCore, QtWidgets, QtGui

from fa2wzl.fa.models import Folder as FAFolder
from fa2wzl.wzl.models import Folder as WZLFolder


class FolderTree(QtWidgets.QTreeWidget):
    folder_dropped = QtCore.pyqtSignal(int, WZLFolder, name="folderDropped")

    def mimeTypes(self):
        return ["application/x-fa2wzl-folders"]

    def mimeData(self, Iterable, QTreeWidgetItem=None):
        text = ""

        for item in Iterable:
            folder = item.data(0, QtCore.Qt.UserRole)

            if isinstance(folder, FAFolder):
                text = "%d\n" % folder.id

        md = QtCore.QMimeData()
        md.setData("application/x-fa2wzl-folders", text.encode("utf-8"))

        return md

    def dropMimeData(self, parent_item, child_idx, mdata, action):
        text = bytes(mdata.data("application/x-fa2wzl-folders")).decode("utf-8")

        if not text:
            return False

        folder = parent_item.data(0, QtCore.Qt.UserRole)
        if not isinstance(folder, WZLFolder):
            return False

        self.folder_dropped.emit(int(text), folder)

        return True
