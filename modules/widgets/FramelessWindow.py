import typing

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent, QMouseEvent
from PyQt5.QtWidgets import QMainWindow, QWidget

from modules.helpers.types.Decorators import override


class FramelessWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.__titleBarHeight: int = 72
        self.__offset: int = 0

        self.__background = QWidget(self)
        self.__inner = QWidget(self)

        self.__init_ui()

    def __init_ui(self) -> None:
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCentralWidget(self.__inner)

        self._add_body_to(self.__inner)

    def setTitleHeight(self, height: int) -> None:
        self.__titleBarHeight = height

    def _add_body_to(self, parent: QWidget) -> None:
        ...

    @override
    def setFixedHeight(self, h: int) -> None:
        self.__background.setFixedHeight(h)
        self.__inner.setFixedHeight(h)

    @override
    def setFixedWidth(self, w: int) -> None:
        self.__background.setFixedWidth(w)
        self.__inner.setFixedWidth(w)

    @typing.overload
    @override
    def setFixedSize(self, a0: QtCore.QSize) -> None:
        self.__background.setFixedWidth(a0)
        self.__inner.setFixedWidth(a0)

    @typing.overload
    @override
    def setFixedSize(self, w: int, h: int) -> None:
        self.__background.setFixedWidth(w, h)
        self.__inner.setFixedWidth(w, h)

    @override
    def setFixedSize(self, a0: QtCore.QSize) -> None:
        self.__background.setFixedSize(a0)
        self.__inner.setFixedSize(a0)

    @typing.overload
    @override
    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self.__background.setContentsMargins(left, top, right, bottom)
        self.__inner.setContentsMargins(left, top, right, bottom)

    @typing.overload
    @override
    def setContentsMargins(self, margins: QtCore.QMargins) -> None:
        self.__background.setContentsMargins(margins)
        self.__inner.setContentsMargins(margins)

    @override
    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self.__background.setContentsMargins(left, top, right, bottom)
        self.__inner.setContentsMargins(left, top, right, bottom)

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.__background.resize(self.size())
        return super().resizeEvent(event)

    @override
    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)
        if event.pos().y() < self.__titleBarHeight and event.button() == Qt.LeftButton:
            self.__offset = event.pos()

    @override
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        self.__offset = 0

    @override
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        super().mouseMoveEvent(event)
        if self.__offset == 0:
            return
        delta = event.pos() - self.__offset
        self.move(self.pos() + delta)

    @override
    def setStyleSheet(self, style: str) -> None:
        self.__background.setStyleSheet(style)
