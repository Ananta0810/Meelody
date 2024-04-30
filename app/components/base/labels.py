from typing import Optional

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFontMetrics, QResizeEvent
from PyQt5.QtWidgets import QLabel, QLineEdit, QWidget

from app.components.base import Component
from app.helpers.base import Strings


class EllipsisLabel(QLabel, Component):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.__text: str = ""
        self.__ellipsis: bool = True

        super()._initComponent()

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


class LabelWithDefaultText(QLabel, Component):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.__defaultText: str = ""
        self.__displayingText: str = ""
        self.__ellipsis: bool = True

        super()._initComponent()

    def enableEllipsis(self, a0: bool = True) -> None:
        self.__ellipsis = a0
        super().setWordWrap(not a0)

    def setWordWrap(self, on: bool) -> None:
        super().setWordWrap(on)
        self.__ellipsis = not on

    def resizeEvent(self, a0: QResizeEvent) -> None:
        super().resizeEvent(a0)
        self.setText(self.__displayingText)

    def setText(self, text: str) -> None:
        self.__displayingText = text or self.__defaultText
        if self.__ellipsis:
            metrics = QFontMetrics(self.font())
            displayTextWithDot = metrics.elidedText(text, Qt.ElideRight, self.width())
            super().setText(displayTextWithDot)
            return
        return super().setText(self.__displayingText)

    def text(self) -> str:
        return self.__displayingText

    def setDefaultText(self, text: str) -> None:
        self.__defaultText = text
        if Strings.isBlank(self.text()):
            self.setText(text)


class Input(QLineEdit, Component):
    __defaultText: str = ""
    changed: pyqtSignal = pyqtSignal(str)
    pressed: pyqtSignal = pyqtSignal(str)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        super()._initComponent()

    def keyPressEvent(self, a0):
        super().keyPressEvent(a0)
        if a0.key() != Qt.Key_Return:
            self.changed.emit(self.text())
            return
        self.pressed.emit(self.text())

    def setText(self, text: str) -> None:
        super().setText(text or self.__defaultText)
        metrics = self.fontMetrics()
        self.setMinimumWidth(metrics.boundingRect(text).width() + 4)
