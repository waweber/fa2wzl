import json

from PyQt5 import QtCore, QtWidgets, QtGui

from fa2wzl.fa.models import Folder as FAFolder, Submission as FASubmission
from fa2wzl.wzl.models import Folder as WZLFolder, Submission as WZLSubmission


class FolderTree(QtWidgets.QTreeWidget):
    folder_dropped = QtCore.pyqtSignal(int, WZLFolder, name="folderDropped")

    def mimeTypes(self):
        return ["application/x-fa2wzl-folders"]

    def mimeData(self, Iterable, QTreeWidgetItem=None):
        data = []

        for item in Iterable:
            folder = item.data(0, QtCore.Qt.UserRole)

            if isinstance(folder, FAFolder):
                data.append(folder.id)

        md = QtCore.QMimeData()
        md.setData("application/x-fa2wzl-folders",
                   json.dumps(data).encode("utf-8"))

        return md

    def dropMimeData(self, parent_item, child_idx, mdata, action):
        text = bytes(mdata.data("application/x-fa2wzl-folders")).decode("utf-8")

        if not text:
            return False

        folder = parent_item.data(0, QtCore.Qt.UserRole)
        if not isinstance(folder, WZLFolder):
            return False

        data = json.loads(text)

        if len(data) != 1:
            return False

        self.folder_dropped.emit(data[0], folder)

        return True


class SubmissionTree(QtWidgets.QTreeWidget):
    submissions_dropped = QtCore.pyqtSignal(list, list,
                                            name="submissionsDropped")

    def mimeTypes(self):
        return ["application/x-fa2wzl-submissions"]

    def mimeData(self, Iterable, QTreeWidgetItem=None):
        data = []

        for item in Iterable:
            sub = item.data(0, QtCore.Qt.UserRole)
            if isinstance(sub, FASubmission):
                data.append(sub.id)

        mdata = QtCore.QMimeData()
        mdata.setData("application/x-fa2wzl-submissions",
                      json.dumps(data).encode("utf-8"))

        return mdata

    def dropMimeData(self, parent_item, child_idx, mdata, action):
        text = bytes(mdata.data("application/x-fa2wzl-submissions")).decode(
            "utf-8")

        data = json.loads(text)


        if parent_item is None:
            folder = None
        else:
            folder = parent_item.data(0, QtCore.Qt.UserRole)
            if not isinstance(folder, WZLFolder):
                return False

        self.submissions_dropped.emit(data, [folder])

        return True
