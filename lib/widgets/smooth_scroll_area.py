from typing import Optional

from PyQt5.QtCore import QEasingCurve, QVariantAnimation, pyqtSignal
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtWidgets import QScrollArea, QWidget


class SmoothVerticalScrollArea(QScrollArea):
    scrolled = pyqtSignal()


    def __init__(self, parent: Optional[QWidget] = ...) -> None:
        super().__init__(parent=parent)
        self._itemHeight = 0
        self._animation = QVariantAnimation(self, valueChanged=self.__smoothScroll, duration=1000)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)


    def wheelEvent(self, event: QWheelEvent) -> None:
        self._animation.stop()
        return super().wheelEvent(event)

    def setItemHeight(self, height: int) -> None:
        self._itemHeight = height

    def setAnimationDuration(self, duration: int) -> None:
        self._animation.setDuration(duration)

    def setAnimationEasingCurve(self, easingCurve: QEasingCurve) -> None:
        self._animation.setEasingCurve(easingCurve)

    def scrollToItem(self, item: int) -> None:
        endValue: int = item * self._itemHeight
        maxValue: int = self.verticalScrollBar().maximum()
        if endValue > maxValue:
            endValue = maxValue
        self._animation.stop()
        self._animation.setStartValue(self.verticalScrollBar().value())
        self._animation.setEndValue(endValue)
        self._animation.start()

    def __smoothScroll(self, value: float) -> None:
        self.verticalScrollBar().setValue(value)
