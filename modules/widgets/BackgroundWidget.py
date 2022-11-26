from typing import Optional

from PyQt5.QtCore import Qt, QEvent, QObject
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QWidget


class BackgroundWidget(QWidget):
    background: QWidget
    children: list[QWidget]

    def __init__(self, parent: Optional["QWidget"] = None):
        super(BackgroundWidget, self).__init__(parent)
        self.children = []
        self.__init_component_ui()

    def __post_init__(self):
        self.children = self.findChildren(QWidget)
        for child in self.children:
            child.installEventFilter(self)
            child.setAttribute(Qt.WA_Hover)

    def __init_component_ui(self) -> None:
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_Hover, True)

        self.background = QWidget(self)
        self.background.setAttribute(Qt.WA_Hover, True)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.__post_init__()
        self.background.resize(self.size())
        return super().resizeEvent(a0)

    def enterEvent(self, event: QEvent) -> None:
        self.background.enterEvent(event)
        return super().enterEvent(event)

    def leaveEvent(self, a0: QEvent) -> None:
        self.background.leaveEvent(a0)
        self.background.setProperty("hovered", False)
        self.background.style().unpolish(self.background)
        self.background.style().polish(self.background)
        return super().leaveEvent(a0)

    def eventFilter(self, source: QObject, event: QEvent):
        if source in self.children and event.type() in [QEvent.HoverEnter, QEvent.HoverLeave, QEvent.HoverMove]:
            self.background.setProperty("hovered", True)
            self.background.style().unpolish(self.background)
            self.background.style().polish(self.background)
        return super().eventFilter(source, event)

    def setStyleSheet(self, style_sheet: str) -> None:
        self.background.setStyleSheet(style_sheet)