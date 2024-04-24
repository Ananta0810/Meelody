from typing import Optional

from PyQt5.QtCore import pyqtSignal, QVariantAnimation, QEasingCurve
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtWidgets import QWidget

from app.components.scroll_areas.style_scroll_area import StyleScrollArea
from app.helpers.base import Numbers


class SmoothVerticalScrollArea(StyleScrollArea):
    scrolled = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)
        # TODO: Try to remove item height.
        self.__itemHeight = 0
        self.__animation = QVariantAnimation(self, valueChanged=self.__smoothScroll, duration=1000)
        self.__animation.setEasingCurve(QEasingCurve.OutCubic)

    def wheelEvent(self, event: QWheelEvent) -> None:
        self.__animation.stop()
        return super().wheelEvent(event)

    def setItemHeight(self, height: int) -> None:
        self.__itemHeight = height

    def setAnimationDuration(self, duration: int) -> None:
        self.__animation.setDuration(duration)

    def setAnimationEasingCurve(self, easing_curve: QEasingCurve) -> None:
        self.__animation.setEasingCurve(easing_curve)

    def getCurrentItemIndex(self):
        return self.verticalScrollBar().value() // self.__itemHeight

    def _scrollToItemAt(self, index: int) -> None:
        maxValue: int = self.verticalScrollBar().maximum()
        endValue: int = Numbers.clamp(index * self.__itemHeight, 0, maxValue)
        self.__animation.stop()
        self.__animation.setStartValue(self.verticalScrollBar().value())
        self.__animation.setEndValue(endValue)
        self.__animation.start()

    def __smoothScroll(self, value: int) -> None:
        self.verticalScrollBar().setValue(value)
