from typing import Callable, Self, Optional

from PyQt5.QtCore import QEasingCurve, Qt, QVariantAnimation
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget

from modules.helpers.PixmapHelper import PixmapHelper


class ImageViewer(QLabel):
    def __init__(self, parent: Optional["QWidget"] = None) -> Self:
        QLabel.__init__(self, parent)
        self._default_pixmap = None
        self._current_pixmap = None
        self._value = 0
        self._start = 0
        self._end = 0
        self._radius = 0
        self._animation = None

    def set_default_pixmap(self, pixmap: QPixmap) -> None:
        self._default_pixmap = pixmap
        self.setPixmap(pixmap)

    def set_radius(self, radius: int) -> None:
        self._radius = radius

    def set_pixmap(self, pixmap: QPixmap) -> None:
        if pixmap is None:
            pixmap = self._default_pixmap
        self._current_pixmap = pixmap
        super().setPixmap(pixmap)

    def set_animation(self, duration: float, start: float, end: float, on_value_changed: Callable) -> None:
        self._start = start
        self._end = end
        self._animation = QVariantAnimation(self, valueChanged=on_value_changed, duration=duration)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)

    def zoom(self, value: float) -> None:
        self._value = value
        if self._current_pixmap is None:
            return
        pixmap = self._current_pixmap.copy()
        pixmap = pixmap.scaledToHeight(int(self.height() * value), Qt.SmoothTransformation)
        pixmap = PixmapHelper.crop_pixmap(pixmap, self.width(), self.height())
        pixmap = PixmapHelper.round_pixmap(pixmap, radius=24)
        self.__set_hover_pixmap(pixmap)

    def animationOnEnteredHover(self) -> None:
        if self._animation is None:
            return
        self._animation.stop()
        self._animation.setStartValue(self._start)
        self._animation.setEndValue(self._end)
        self._animation.start()

    def animationOnLeavedHover(self) -> None:
        if self._animation is None:
            return
        self._animation.setStartValue(self._value)
        self._animation.setEndValue(self._start)
        self._animation.start()

    def __set_hover_pixmap(self, pixmap: QPixmap) -> None:
        super().setPixmap(pixmap)
