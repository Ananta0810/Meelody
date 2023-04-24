from typing import Union

from PyQt5.QtCore import QByteArray, QBuffer, QIODevice, QRect, Qt
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath


class PixmapHelper:
    @staticmethod
    def get_pixmap_from_bytes(image_byte: bytes) -> Union[QPixmap, None]:
        if image_byte is None:
            return None
        pixmap = QPixmap()
        pixmap.loadFromData(image_byte)
        return pixmap

    @staticmethod
    def get_bytes_from_pixmap(pixmap: QPixmap) -> bytes:
        byte_array = QByteArray()
        buff = QBuffer(byte_array)
        buff.open(QIODevice.WriteOnly)
        ok = pixmap.save(buff, "JPG")
        assert ok
        return byte_array.data()

    @staticmethod
    def crop_pixmap(pixmap, width: int, height: int, crop_center: bool = True) -> QPixmap:
        w = pixmap.width()
        h = pixmap.height()
        if width > w:
            width = w
        if height > h:
            height = h

        left = (w - width) // 2 if crop_center else 0
        top = (h - height) // 2 if crop_center else 0
        return pixmap.copy(QRect(left, top, width, height))

    @staticmethod
    def scale_pixmap_keeping_ratio(pixmap: QPixmap, smaller_edge_size: int) -> QPixmap:
        temp: QPixmap = pixmap.copy()
        if pixmap.height() <= pixmap.width():
            return temp.scaledToHeight(smaller_edge_size, Qt.SmoothTransformation)
        return temp.scaledToWidth(smaller_edge_size, Qt.SmoothTransformation)

    @staticmethod
    def square_pixmap(pixmap: QPixmap) -> QPixmap:
        w = pixmap.width()
        h = pixmap.height()

        is_squared: bool = w == h
        if is_squared:
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
    def round_pixmap(pixmap: QPixmap, radius: float = 0) -> QPixmap:
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
