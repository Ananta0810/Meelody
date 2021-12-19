from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget


class HoverableWidget(QWidget):
    onHover = pyqtSignal()
    leaveHover = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def enterEvent(self, event):
        self.onHover.emit()

    def leaveEvent(self, event):
        self.leaveHover.emit()
