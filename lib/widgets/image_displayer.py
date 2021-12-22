from typing import Callable

from PyQt5.QtCore import QEasingCurve, Qt, QVariantAnimation
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from utils.ui.pixmap_utils import PixmapUtils


class ImageDisplayer(QLabel):
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self._defaultPixmap = None
        self._currentPixmap = None
        self._value = 0
        self._start = 0
        self._end = 0
        self._radius = 0
        self._animation = None

    def setDefaultPixmap(self, pixmap: QPixmap):
        self._defaultPixmap = pixmap
        self.setPixmap(pixmap)

    def setRadius(self, radius: int):
        self._radius = radius

    def setPixmap(self, pixmap: QPixmap):
        if pixmap is None:
            pixmap = self._defaultPixmap
        self._currentPixmap = pixmap
        super().setPixmap(pixmap)

    def setAnimation(self, duration: float, start: float, end: float, type: Callable):
        self._start = start
        self._end = end
        self._animation = QVariantAnimation(self, valueChanged=type, duration=duration)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)

    def zoom(self, value: float):
        self._value = value
        if self._currentPixmap is None:
            return
        pixmap = self._currentPixmap.copy()
        pixmap = pixmap.scaledToHeight(int(self.height() * value), Qt.SmoothTransformation)
        pixmap = PixmapUtils.cropPixmap(pixmap, self.width(), self.height())
        pixmap = PixmapUtils.roundPixmap(pixmap, radius=24)
        self.__setHoverPixmap(pixmap)

    def animationOnEnteredHover(self):
        if self._animation is None:
            return
        self._animation.stop()
        self._animation.setStartValue(self._start)
        self._animation.setEndValue(self._end)
        self._animation.start()

    def animationOnLeavedHover(self):
        if self._animation is None:
            return
        self._animation.setStartValue(self._value)
        self._animation.setEndValue(self._start)
        self._animation.start()

    def __setHoverPixmap(self, pixmap: QPixmap) -> None:
        super().setPixmap(pixmap)
