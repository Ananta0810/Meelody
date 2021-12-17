from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow


class FramelessWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.Window | Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.titleBarHeight = 80
        self.offset = None

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if (
            event.pos().y() < self.titleBarHeight
            and event.button() == Qt.LeftButton
        ):
            self.offset = event.pos()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.offset = None

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.offset is None:
            return
        delta = event.pos() - self.offset
        self.move(self.pos() + delta)

    def setTitleBarHeight(self, height: int):
        self.titleBarHeight = height
