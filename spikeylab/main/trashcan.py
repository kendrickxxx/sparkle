import os

from PyQt4 import QtGui, QtCore

class TrashWidget(QtGui.QPushButton):
    itemTrashed = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        QtGui.QPushButton.__init__(self, parent)

        thisfolder = os.path.dirname(os.path.realpath(__file__))
        self.trashIcon = QtGui.QIcon(os.path.join(thisfolder,'trash.png'))
        self.setFlat(True)
        self.setIcon(self.trashIcon)
        self.setIconSize(QtCore.QSize(25,25))
        self.setAcceptDrops(True)

        self._underMouse = False

    def dragEnterEvent(self, event):
        self.setFlat(False)
        event.accept()

    def dragLeaveEvent(self, event):
        self.setFlat(True)
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def leaveEvent(self, event):
        self.setFlat(True)
        event.accept()

    def dropEvent(self, event):
        super(TrashWidget, self).dropEvent(event)
        self.itemTrashed.emit()

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.ChildRemoved and self.underMouse():
            return True
        else:
            return super(type(self.parent()), self.parent()).eventFilter(source, event)