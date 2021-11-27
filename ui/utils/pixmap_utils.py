from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class PixmapUtils:
    @staticmethod
    def getPixmapFromBytes(byteImage: bytes) -> QPixmap:
        if byteImage is None:
            return None
        pixmap = QPixmap()
        pixmap.loadFromData(byteImage)
        return pixmap

    def cropPixmap(pixmap, size: int):
        temp: QPixmap = pixmap.copy()
        if pixmap.height() <= pixmap.width():
            return temp.scaledToHeight(size, Qt.SmoothTransformation)
        return temp.scaledToWidth(size, Qt.SmoothTransformation)

    def squarePixmap(pixmap):
        w = pixmap.width()
        h = pixmap.height()

        isQuared: bool = w == h
        if isQuared:
            return pixmap

        edge: int = min(w, h)
        left = 0
        top = 0

        if h <= w:
            left = (w - edge) // 2
        else:
            top = (h - edge) // 2
        return pixmap.copy(QRect(left, top, edge, edge))

    def roundPixmap(pixmap: QPixmap, radius: float = 0) -> QPixmap:
        target = QPixmap(pixmap.size())
        target.fill(Qt.transparent)

        painter = QPainter(target)
        painter.setRenderHint(QPainter.Antialiasing, True)

        path = QPainterPath()
        path.addRoundedRect(0, 0, pixmap.width(), pixmap.height(), radius, radius)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        return target
