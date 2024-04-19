from io import BytesIO
from typing import Union, final

from PIL import Image
from PyQt5.QtCore import QByteArray, QBuffer, QIODevice, QRect, Qt
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath

from app.helpers.stylesheets import Color


@final
class Pixmaps:

    @staticmethod
    def toQPixmap(imageByte: bytes) -> Union[QPixmap, None]:
        if imageByte is None:
            return None
        pixmap = QPixmap()
        pixmap.loadFromData(imageByte)
        return pixmap

    @staticmethod
    def bytesOf(pixmap: QPixmap) -> bytes:
        byteArray = QByteArray()
        buff = QBuffer(byteArray)
        buff.open(QIODevice.WriteOnly)
        ok = pixmap.save(buff, "JPG")
        assert ok
        return byteArray.data()

    @staticmethod
    def crop(pixmap, width: int, height: int, cropCenter: bool = True) -> QPixmap:
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
    def scaleKeepingRatio(pixmap: QPixmap, smallerEdgeSize: int) -> QPixmap:
        temp: QPixmap = pixmap.copy()
        if pixmap.height() <= pixmap.width():
            return temp.scaledToHeight(smallerEdgeSize, Qt.SmoothTransformation)
        return temp.scaledToWidth(smallerEdgeSize, Qt.SmoothTransformation)

    @staticmethod
    def square(pixmap: QPixmap) -> QPixmap:
        w = pixmap.width()
        h = pixmap.height()

        isSquared: bool = w == h
        if isSquared:
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
    def round(pixmap: QPixmap, radius: float = 0) -> QPixmap:
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
    def getDominantColor(pixmap: QPixmap) -> Color:
        pixmapBytes: bytes = Pixmaps.bytesOf(pixmap)
        image: Image = Image.open(BytesIO(pixmapBytes))
        BLURRED_IMAGE_SIZE: int = 200

        image.thumbnail((BLURRED_IMAGE_SIZE, BLURRED_IMAGE_SIZE))

        imagePalette = image.convert("P", palette=Image.ADAPTIVE, colors=16)

        colorCount = sorted(imagePalette.getcolors(), reverse=True)
        paletteIndex = colorCount[0][1]
        red, green, blue = imagePalette.getpalette()[paletteIndex * 3: paletteIndex * 3 + 3]
        return Color(red, green, blue)

    @staticmethod
    def getDominantColorAt(rect: QRect, of: QPixmap) -> Color:
        return Pixmaps.getDominantColor(of.copy(rect))
