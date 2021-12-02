from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ImageDisplayer(QLabel):
    clicked = pyqtSignal()
    doubleClicked = pyqtSignal()
    onHover = pyqtSignal()
    offHover = pyqtSignal()

    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self._defaultPixmap = None

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        self.doubleClicked.emit()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.offHover.emit()

    def enterEvent(self, event):
        super().enterEvent(event)
        self.onHover.emit()

    def setDefaultPixmap(self, pixmap: QPixmap):
        self._defaultPixmap = pixmap

    def setPixmap(self, pixmap: QPixmap):
        if pixmap is None:
            pixmap = self._defaultPixmap
        super().setPixmap(pixmap)
