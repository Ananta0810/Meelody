from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics, QResizeEvent
from PyQt5.QtWidgets import QLabel, QWidget

from app.components.base import Component


class EllipsisLabel(QLabel, Component):

    def __init__(self, parent: Optional[QWidget] = None, autoChangeTheme: bool = True):
        super().__init__(parent)

        self.__text: str = ""
        self.__ellipsis: bool = True
        self.enableEllipsis(True)

        super()._initComponent(autoChangeTheme)

    def enableEllipsis(self, a0: bool = True) -> None:
        self.__ellipsis = a0
        super().setWordWrap(not a0)

    def setWordWrap(self, on: bool) -> None:
        super().setWordWrap(on)
        self.__ellipsis = not on

    def resizeEvent(self, a0: QResizeEvent) -> None:
        super().resizeEvent(a0)
        self.setText(self.__text)

    def setText(self, text: str) -> None:
        self.__text = text
        if self.__ellipsis:
            metrics = QFontMetrics(self.font())
            ellipsisText = metrics.elidedText(text, Qt.ElideRight, self.width())
            super().setText(ellipsisText)
            return
        return super().setText(self.__text)

    def text(self) -> str:
        return self.__text

    def ellipsisText(self) -> str:
        return QFontMetrics(self.font()).elidedText(self.__text, Qt.ElideRight, self.width())
