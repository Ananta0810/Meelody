from typing import Optional

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFontMetrics, QResizeEvent
from PyQt5.QtWidgets import QLabel, QLineEdit, QWidget

from app.components.base import Component
from app.helpers.base import Strings


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


class Label(QLabel, Component):

    def __init__(self, parent: Optional[QWidget] = None, autoChangeTheme: bool = True):
        super().__init__(parent)
        super()._initComponent(autoChangeTheme)
        self.setWordWrap(True)


class LabelWithDefaultText(QLabel, Component):

    def __init__(self, parent: Optional[QWidget] = None, autoChangeTheme: bool = True):
        super().__init__(parent)

        self.__defaultText: Optional[str] = None
        self.__displayingText: str = ""
        self.__ellipsis: bool = True

        super()._initComponent(autoChangeTheme)

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
        if Strings.isBlank(text):
            super().setText("")
            self.__displayingText = ""
            return

        self.__displayingText = text or self.__defaultText or ""
        if self.__ellipsis:
            metrics = QFontMetrics(self.font())
            displayTextWithDot = metrics.elidedText(text, Qt.ElideRight, self.width())
            super().setText(displayTextWithDot)
            return
        return super().setText(self.__displayingText)

    def text(self) -> str:
        return self.__displayingText

    def ellipsisText(self) -> str:
        return QFontMetrics(self.font()).elidedText(self.__displayingText, Qt.ElideRight, self.width())

    def setDefaultText(self, text: str) -> None:
        if self.__defaultText is None or self.__defaultText == self.text():
            self.setText(text)

        self.__defaultText = text


class Input(QLineEdit, Component):
    changed: pyqtSignal = pyqtSignal(str)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        super()._initComponent()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        self.changed.emit(self.text())
