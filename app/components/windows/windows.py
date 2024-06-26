from typing import Union

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QShowEvent, QResizeEvent, QMouseEvent
from PyQt5.QtWidgets import QMainWindow, QWidget, QLayout, QHBoxLayout, QGraphicsDropShadowEffect, QApplication

from app.common.statics.qt import Icons
from app.common.statics.styles import Colors
from app.common.statics.styles import Paddings
from app.components.base import Component
from app.components.buttons import ButtonFactory
from app.components.widgets import Box, StyleWidget
from app.helpers.stylesheets import Color
from app.utils.base import Strings


class FramelessWindow(QMainWindow, Component):

    def __init__(self) -> None:
        super().__init__()

        self.__shadowHeight = 0

        self.__initUI()
        self.setShadow(Colors.gray, 32)

    def __initUI(self) -> None:
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._inner = StyleWidget()
        self._inner.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self._inner)

        self._mainLayout = Box(self._inner)
        self._mainLayout.setSpacing(0)
        self._mainLayout.setContentsMargins(0, 0, 0, 0)

    def setShadow(self, color: Color, size: int) -> None:
        self.__shadowHeight = size

        self._inner.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=size, color=color.withAlpha(50).toQColor(), xOffset=0, yOffset=3))
        super().setContentsMargins(size * 2, size * 2, size * 2, size * 2)

    def moveToCenter(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def addLayout(self, widget: QLayout) -> None:
        self._mainLayout.addLayout(widget)

    def addWidget(self, widget: QWidget, stretch: int = None, alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = None) -> None:
        self._mainLayout.addWidget(widget, stretch=stretch, alignment=alignment)

    def addSpacing(self, size: int) -> None:
        self._mainLayout.addSpacing(size)

    def setFixedHeight(self, h: int) -> None:
        self._inner.setFixedHeight(h)

    def setFixedWidth(self, w: int) -> None:
        self._inner.setFixedWidth(w)

    def setFixedSize(self, w: int, h: int) -> None:
        self._inner.setFixedSize(w, h)

    def sizeHint(self) -> QtCore.QSize:
        return self._inner.sizeHint()

    def width(self) -> int:
        return self._inner.sizeHint().width()

    def height(self) -> int:
        return self._inner.sizeHint().height()

    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self._inner.setContentsMargins(left, top, right, bottom)

    def showEvent(self, a0: QShowEvent) -> None:
        super().showEvent(a0)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self._inner.resize(self.size())

    def setClassName(self, *classNames: str) -> None:
        self._inner.setClassName(Strings.join(" ", classNames))


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

        self._minimizeBtn = ButtonFactory.createIconButton(size=Icons.medium, padding=Paddings.relative50)
        self._minimizeBtn.setLightModeIcon(Icons.minimize.withColor(Colors.primary))
        self._minimizeBtn.setDarkModeIcon(Icons.minimize.withColor(Colors.white))
        self._minimizeBtn.setClassName("rounded-8 hover:bg-black-12 bg-none dark:hover:bg-white-20")

        self._maximizeBtn = ButtonFactory.createIconButton(size=Icons.medium, padding=Paddings.relative50)
        self._maximizeBtn.setLightModeIcon(Icons.maximize.withColor(Colors.primary))
        self._maximizeBtn.setDarkModeIcon(Icons.maximize.withColor(Colors.white))
        self._maximizeBtn.setClassName("rounded-8 hover:bg-black-12 bg-none dark:hover:bg-white-20")

        self._closeBtn = ButtonFactory.createIconButton(size=Icons.medium, padding=Paddings.relative50)
        self._closeBtn.setLightModeIcon(Icons.close.withColor(Colors.danger))
        self._closeBtn.setDarkModeIcon(Icons.close.withColor(Colors.white))
        self._closeBtn.setClassName("rounded-8 bg-danger-25 hover:bg-danger-33 dark:bg-danger dark:hover:bg-danger-[b120]")

        self._titleBarLayout.addStretch()
        self._titleBarLayout.addWidget(self._minimizeBtn)
        self._titleBarLayout.addWidget(self._maximizeBtn)
        self._titleBarLayout.addWidget(self._closeBtn)

        self.addWidget(self._titleBar, alignment=Qt.AlignTop)

    def translateUI(self) -> None:
        super().translateUI()
        self._minimizeBtn.setToolTip(self.translate("TITLE_BAR.MINIMIZE_BNT"))
        self._closeBtn.setToolTip(self.translate("TITLE_BAR.CLOSE_BTN"))

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)
        if event.pos().y() - 64 < self._titleBar.height() and event.button() == Qt.LeftButton:
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
