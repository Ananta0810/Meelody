from typing import Optional

from PyQt5.QtCore import Qt, QEvent, QObject
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QWidget

from app.helpers import override


class BackgroundWidget(QWidget):
    __background: QWidget
    __children: list[QWidget]

    def __init__(self, parent: Optional["QWidget"] = None):
        super(BackgroundWidget, self).__init__(parent)
        self.__children = []
        self.__init_ui()

    def __post_init__(self):
        self.__children = self.findChildren(QWidget)
        for child in self.__children:
            child.installEventFilter(self)
            child.setAttribute(Qt.WA_Hover)

    def __init_ui(self) -> None:
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_Hover, True)

        self.__background = QWidget(self)
        self.__background.setAttribute(Qt.WA_Hover, True)

    @override
    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.__post_init__()
        self.__background.resize(self.size())
        return super().resizeEvent(a0)

    @override
    def enterEvent(self, event: QEvent) -> None:
        self.__background.enterEvent(event)
        return super().enterEvent(event)

    @override
    def leaveEvent(self, a0: QEvent) -> None:
        self.__background.leaveEvent(a0)
        self.__background.setProperty("hovered", False)
        self.__background.style().unpolish(self.__background)
        self.__background.style().polish(self.__background)
        return super().leaveEvent(a0)

    def eventFilter(self, source: QObject, event: QEvent):
        if source in self.__children and event.type() in [QEvent.HoverEnter, QEvent.HoverLeave, QEvent.HoverMove]:
            self.__background.setProperty("hovered", True)
            self.__background.style().unpolish(self.__background)
            self.__background.style().polish(self.__background)
        return super().eventFilter(source, event)

    @override
    def setStyleSheet(self, style: str) -> None:
        self.__background.setStyleSheet(style)
