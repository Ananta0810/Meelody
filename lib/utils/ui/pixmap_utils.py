from modules.models.image import MyByteImage
from PyQt5.QtCore import QBuffer, QByteArray, QIODevice, QRect, Qt
from PyQt5.QtGui import QPainter, QPainterPath, QPixmap


class PixmapUtils:
    @staticmethod
    def getPixmapFromBytes(byteImage: bytes) -> QPixmap:
        if byteImage is None:
            return None
        pixmap = QPixmap()
        pixmap.loadFromData(byteImage)
        return pixmap

    @staticmethod
    def getBytesFromPixmap(pixmap: QPixmap) -> bytes:
        bytearray = QByteArray()
        buff = QBuffer(bytearray)
        buff.open(QIODevice.WriteOnly)
        ok = pixmap.save(buff, "JPG")
        assert ok
        return bytearray.data()

    @staticmethod
    def cropPixmap(pixmap, width: int, height: int, cropCenter: bool = True) -> QPixmap:
        w = pixmap.width()
        h = pixmap.height()
        if width > w:
            width = w
        if height > h:
            height = h

        left = (w - width) // 2 if cropCenter else 0
        top = (h - height) // 2 if cropCenter else 0
        return pixmap.copy(QRect(left, top, width, height))

    @staticmethod
    def scalePixmapKeepingRatio(pixmap: QPixmap, smallerEdgeSize: int) -> QPixmap:
        temp: QPixmap = pixmap.copy()
        if pixmap.height() <= pixmap.width():
            return temp.scaledToHeight(smallerEdgeSize, Qt.SmoothTransformation)
        return temp.scaledToWidth(smallerEdgeSize, Qt.SmoothTransformation)

    @staticmethod
    def squarePixmap(pixmap: QPixmap) -> QPixmap:
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

    @staticmethod
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

    @staticmethod
    def getPixmapBrightness(pixmap: QPixmap):
        pixmapBytes: bytes = PixmapUtils.getBytesFromPixmap(pixmap)
        return MyByteImage(pixmapBytes).getContrastLevel()
