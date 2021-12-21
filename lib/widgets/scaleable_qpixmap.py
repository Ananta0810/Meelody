from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ScaleAblePixmap(QPixmap):
    def __init__(self):
        super().__init__()
        self._radius = 0
        self._original = None
        self._isZooming = False
        self._animation = None
        self._duration = 0
        self._start = 1
        self._end = 1.25

    def eventFilter(self, event):
        super().eventFilter(event)
        if self.animation is None:
            return
        if event.type() == QEvent.Enter:
            self.startAnimation()
        elif event.type() == QEvent.Leave:
            self.start_leave_animation()

    def reverseAllChanges(self):
        self.setPixmap(self._original)

    def setAnimation(self, duration: float, start: float, end: float):
        self._animation = QVariantAnimation(
            self, valueChanged=self._animate, startValue=start, endValue=end, duration=duration
        )

    def animate(self, value: float):
        self.zoom(value)

    def startAnimation(self):
        self._animation.start()

    def stopAnimation(self):
        self._animation.stop()
        self._animation.setStartValue(self.widget.pos())
        self._animation.setEndValue(self._start_value)
        self._animation.start()

    def setPixmap(self, pixmap):
        super().setPixmap(pixmap)
        self._original = pixmap

    def zoom(self, scale: float):
        if not self._isZooming:
            self._original = self.copy()
        self.scaledToHeight(self.height() * scale, Qt.SmoothTransformation)

    def setRadius(self, radius: int = 0):
        self._radius = radius

    def round(self):
        target = QPixmap(self.size())
        target.fill(Qt.transparent)

        painter = QPainter(target)
        painter.setRenderHint(QPainter.Antialiasing, True)

        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), self._radius, self._radius)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, self)
        painter.end()
        return target

    def square(self):
        w = self.width()
        h = self.height()

        isQuared: bool = w == h
        if isQuared:
            return

        edge: int = min(w, h)
        left = 0
        top = 0

        if h <= w:
            left = (w - edge) // 2
        else:
            top = (h - edge) // 2
        return self.copy(QRect(left, top, edge, edge))

    def crop(self, width: int, height: int, cropCenter: bool = True):
        w = self.width()
        h = self.height()
        if width > w:
            width = w
        if height > h:
            height = h

        left = (w - width) // 2 if cropCenter else 0
        top = (h - height) // 2 if cropCenter else 0
        return self.copy(QRect(left, top, width, height))

    def scalePixmapKeepingRatio(self, smallerEdgeSize: int):
        temp: QPixmap = self.copy()
        if self.height() <= self.width():
            return temp.scaledToHeight(smallerEdgeSize, Qt.SmoothTransformation)
        return temp.scaledToWidth(smallerEdgeSize, Qt.SmoothTransformation)
