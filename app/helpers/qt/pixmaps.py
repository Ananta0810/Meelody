from io import BytesIO
from typing import Union, final, Optional

from PIL import Image
from PyQt5.QtCore import QByteArray, QBuffer, QIODevice, QRect, Qt
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath
from colorthief import MMCQ

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
    def toBytes(pixmap: QPixmap) -> Optional[bytes]:
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
    def getDominantColors(pixmap: QPixmap, maxColors: int = 10) -> list[Color]:
        pixmapBytes: bytes = Pixmaps.toBytes(pixmap)
        image: Image = Image.open(BytesIO(pixmapBytes))

        palettes = Pixmaps.__getPalettes(image, maxColors, 10)
        return [Color(red, green, blue) for red, green, blue in palettes]

    @staticmethod
    def __getPalettes(image: Image, color_count=10, quality=10):
        image = image.convert('RGBA')
        width, height = image.size
        pixels = image.getdata()
        pixelCount = width * height
        validPixels = []
        for i in range(0, pixelCount, quality):
            r, g, b, a = pixels[i]
            # If pixel is mostly opaque and not white
            if a >= 125:
                if not (r > 250 and g > 250 and b > 250):
                    validPixels.append((r, g, b))

        # Send array to quantize function which clusters values
        # using median cut algorithm
        cmap = MMCQ.quantize(validPixels, color_count)
        return cmap.palette

    @staticmethod
    def getDominantColorsAt(rect: QRect, of: QPixmap, maxColors: int = 10) -> list[Color]:
        return Pixmaps.getDominantColors(of.copy(rect), maxColors)
