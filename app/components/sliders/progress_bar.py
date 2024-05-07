from typing import Optional

from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QWidget

from app.components.widgets import ExtendableStyleWidget, StyleWidget
from app.helpers.base import Numbers, Strings, suppressException


class ProgressBar(ExtendableStyleWidget):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.__value: float = 0
        self._initComponent()

    def _createUI(self) -> None:
        self._bar = StyleWidget(self)

    def setValue(self, value: float) -> None:
        self.__value = Numbers.clamp(float(value), float(0), float(100))
        self.__updateProgress()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        super().resizeEvent(a0)
        self.__updateProgress()

    def __updateProgress(self):
        self._bar.setFixedWidth(int(self.__value * self.width() / 100))

    @suppressException
    def setClassName(self, *classNames: str) -> None:
        self._bar.setClassName(Strings.join(" ", classNames))

    def applyLightMode(self) -> None:
        self._bar.applyLightMode()

    def applyDarkMode(self) -> None:
        self._bar.applyDarkMode()
