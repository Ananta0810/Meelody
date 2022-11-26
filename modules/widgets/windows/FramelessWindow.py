from typing import Self

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow


class FramelessWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.title_bar_height: int = 72
        self.offset: int = 0

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.pos().y() < self.title_bar_height and event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.offset = 0

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.offset is 0:
            return
        delta = event.pos() - self.offset
        self.move(self.pos() + delta)

    def with_height(self, height: int) -> Self:
        self.title_bar_height = height
        return self
