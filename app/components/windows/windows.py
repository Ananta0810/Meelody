from typing import overload, Union

from PyQt5.QtCore import Qt, QSize, QMargins
from PyQt5.QtGui import QShowEvent, QResizeEvent, QMouseEvent
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QDesktopWidget, QLayout, QGraphicsDropShadowEffect, QHBoxLayout

from app.components.base import Factory
from app.helpers.stylesheets import Colors, Paddings
from app.resource.qt import Icons


class FramelessWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.__initUI()

    def __initUI(self) -> None:
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._outer = QWidget()
        self.setCentralWidget(self._outer)

        self._background = QWidget(self._outer)
        self._inner = QWidget(self._outer)
        self._mainLayout = QVBoxLayout(self._inner)

        self._outer.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=32, color=Colors.PRIMARY.withAlpha(33).toQColor(), xOffset=0, yOffset=3))

        self._inner.move(32, 32)
        self._background.move(32, 32)
        self._background.setAutoFillBackground(True)

        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainLayout.setSpacing(0)

    def moveToCenter(self):
        qtRectangle = self._outer.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def addLayout(self, widget: QLayout) -> None:
        self._mainLayout.addLayout(widget)

    def addWidget(
        self,
        layout: QWidget,
        stretch: int = 0,
        alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = None
    ) -> None:
        if alignment is None:
            self._mainLayout.addWidget(layout, stretch=stretch)
            return
        self._mainLayout.addWidget(layout, stretch=stretch, alignment=alignment)

    def setFixedHeight(self, h: int) -> None:
        self._background.setFixedHeight(h)
        self._inner.setFixedHeight(h)
        self._outer.setFixedSize(self._inner.width() + 64, self._inner.height() + 64)

    def setFixedWidth(self, w: int) -> None:
        self._background.setFixedWidth(w)
        self._inner.setFixedWidth(w)
        self._outer.setFixedSize(self._inner.width() + 64, self._inner.height() + 64)

    @overload
    def setFixedSize(self, a0: QSize) -> None:
        self._background.setFixedWidth(a0)
        self._inner.setFixedWidth(a0)
        self._outer.setFixedSize(self._inner.width() + 64, self._inner.height() + 64)

    @overload
    def setFixedSize(self, w: int, h: int) -> None:
        self._background.setFixedWidth(w, h)
        self._inner.setFixedWidth(w, h)
        self._outer.setFixedSize(self._inner.width() + 64, self._inner.height() + 64)

    def setFixedSize(self, a0: QSize) -> None:
        self._background.setFixedSize(a0)
        self._inner.setFixedSize(a0)
        self._outer.setFixedSize(self._inner.width() + 64, self._inner.height() + 64)

    def width(self) -> int:
        return self._inner.sizeHint().width()

    def height(self) -> int:
        return self._inner.sizeHint().height()

    @overload
    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self._background.setContentsMargins(left, top, right, bottom)
        self._inner.setContentsMargins(left, top, right, bottom)

    @overload
    def setContentsMargins(self, margins: QMargins) -> None:
        self._background.setContentsMargins(margins)
        self._inner.setContentsMargins(margins)

    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self._background.setContentsMargins(left, top, right, bottom)
        self._inner.setContentsMargins(left, top, right, bottom)

    def showEvent(self, a0: QShowEvent) -> None:
        super().showEvent(a0)
        self._outer.setFixedSize(self._inner.width() + 64, self._inner.height() + 64)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self._background.resize(self.size())
        height_ = self._inner.height() + 64
        self._outer.setFixedSize(self._inner.width() + 64, height_)

    def setStyleSheet(self, style: str) -> None:
        self._background.setStyleSheet(style)


class TitleBar(QWidget):

    def __init__(self, window: QWidget) -> None:
        super().__init__()
        self.__window = window
        self.__offset: int = 0
        self.__initUI()

    def __initUI(self) -> None:
        self._mainLayout = QHBoxLayout()
        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainLayout.setSpacing(8)
        self.setLayout(self._mainLayout)

        self._minimizeBtn = Factory.createIconButton(size=Icons.MEDIUM, padding=Paddings.RELATIVE_50)
        self._minimizeBtn.setLightModeIcon(Icons.MINIMIZE.withColor(Colors.PRIMARY))
        self._minimizeBtn.setClassName("rounded-8 bg-none hover:bg-primary-25")

        self._closeBtn = Factory.createIconButton(size=Icons.MEDIUM, padding=Paddings.RELATIVE_50)
        self._closeBtn.setLightModeIcon(Icons.CLOSE.withColor(Colors.DANGER))
        self._closeBtn.setClassName("rounded-8 bg-danger-25 hover:bg-danger-33")

        self._mainLayout.addStretch()
        self._mainLayout.addWidget(self._minimizeBtn)
        self._mainLayout.addWidget(self._closeBtn)


class TitleBarWindow(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.__initUI()
        self.__offset: int = 0

    def __initUI(self) -> None:
        self._titleBar = QWidget()
        self._titleBar.setContentsMargins(12, 12, 12, 12)
        self._titleBarLayout = QHBoxLayout()
        self._titleBarLayout.setContentsMargins(0, 0, 0, 0)
        self._titleBarLayout.setSpacing(8)
        self._titleBar.setLayout(self._titleBarLayout)

        self._minimizeBtn = Factory.createIconButton(size=Icons.MEDIUM, padding=Paddings.RELATIVE_50)
        self._minimizeBtn.setLightModeIcon(Icons.MINIMIZE.withColor(Colors.PRIMARY))
        self._minimizeBtn.setClassName("rounded-8 bg-none")

        self._closeBtn = Factory.createIconButton(size=Icons.MEDIUM, padding=Paddings.RELATIVE_50)
        self._closeBtn.setLightModeIcon(Icons.CLOSE.withColor(Colors.DANGER))
        self._closeBtn.setClassName("rounded-8 bg-danger-25 hover:bg-danger-33")

        self._titleBarLayout.addStretch()
        self._titleBarLayout.addWidget(self._minimizeBtn)
        self._titleBarLayout.addWidget(self._closeBtn)

        self.addWidget(self._titleBar, alignment=Qt.AlignTop)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)
        if event.pos().y() < self._titleBar.height() and event.button() == Qt.LeftButton:
            self.__offset = event.pos()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        self.__offset = 0

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        super().mouseMoveEvent(event)
        if self.__offset == 0:
            return
        delta = event.pos() - self.__offset
        self.move(self.pos() + delta)
