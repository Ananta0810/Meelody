from typing import Optional

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFontMetrics, QResizeEvent
from PyQt5.QtWidgets import QLabel, QLineEdit

from app.helpers.base import override


class LabelWithDefaultText(QLabel):
    __defaultText: str = ""
    __displayingText: str = ""
    __ellipsis: bool = True

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)

    def enable_ellipsis(self, a0: bool) -> None:
        self.__ellipsis = a0

    @override
    def resizeEvent(self, a0: QResizeEvent) -> None:
        super().resizeEvent(a0)
        self.setText(self.__displayingText)

    @override
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


class Input(QLineEdit):
    __defaultText: str = ""
    onChange: pyqtSignal = pyqtSignal(str)

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)

    @override
    def keyPressEvent(self, a0):
        super().keyPressEvent(a0)
        if a0.key() != Qt.Key_Return:
            return
        self.onChange.emit(self.text())

    @override
    def setText(self, text: str) -> None:
        super().setText(text or self.__defaultText)
        metrics = self.fontMetrics()
        self.setMinimumWidth(metrics.boundingRect(text).width() + 4)
