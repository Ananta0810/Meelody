from abc import ABC, abstractmethod

from PyQt5.QtCore import QEasingCurve, QEvent, Qt, QVariantAnimation, pyqtSignal
from utils.ui.pixmap_utils import PixmapUtils


class Animation(ABC):
    @abstractmethod
    def animate(self):
        pass


class ScaleAnimation(ABC):
    start: float
    end: float
    value: float

    def __init__(self, label, pixmap):
        self.start = 1.0
        self.end = 1.0
        self.value = 1.0
        self.label = label
        self.pixmap = pixmap

    def animate(self):
        pass

    def eventFilter(self, obj, event):
        super().eventFilter(obj, event)
        if obj is not self.label:
            return
        if event.type() == QEvent.Enter:
            self.animationOnEnteredHover()
            return
        if event.type() == QEvent.Leave:
            self.animationOnLeavedHover()

    def zoom(self, value: float):
        self._value = value
        pixmap = self.pixmap.copy()
        pixmap = pixmap.scaledToHeight(self.height() * value, Qt.SmoothTransformation)
        pixmap = PixmapUtils.cropPixmap(pixmap, self.width(), self.height())
        pixmap = PixmapUtils.roundPixmap(pixmap, radius=24)
        self.label.setPixmap(pixmap)

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
        self._animation.stop()
        self._animation.setStartValue(self._value)
        self._animation.setEndValue(self._start)
        self._animation.start()
