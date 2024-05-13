from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent, QFontMetrics
from PyQt5.QtWidgets import QLabel, QWidget

from app.common.others import translator
from app.components.base import Component
from app.utils.base import Strings


class Label(QLabel, Component):

    def __init__(self, parent: Optional[QWidget] = None, autoChangeTheme: bool = True):
        super().__init__(parent)
        super()._initComponent(autoChangeTheme)
        self.setWordWrap(True)


class AutoTranslateLabel(QLabel, Component):

    def __init__(self, parent: Optional[QWidget] = None, autoChangeTheme: bool = True):
        super().__init__(parent)
        super()._initComponent(autoChangeTheme)
        self.__translateKey = None

    def setTranslateText(self, text: str) -> None:
        self.__translateKey = text
        self.translateUI()

    def translateUI(self) -> None:
        if self.__translateKey is not None:
            self.setText(translator.translate(self.__translateKey))


class LabelWithPlaceHolder(QLabel, Component):

    def __init__(self, parent: Optional[QWidget] = None, autoChangeTheme: bool = True):
        super().__init__(parent)

        self.__placeholder: Optional[str] = None
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

        self.__displayingText = text or self.__placeholder or ""
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

    def setPlaceHolder(self, text: str) -> None:
        if self.__placeholder is None or self.__placeholder == self.text():
            self.setText(text)

        self.__placeholder = text
