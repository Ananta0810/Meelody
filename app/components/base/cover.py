from typing import Optional, Callable

from PyQt5.QtCore import QVariantAnimation, QEasingCurve
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget

from app.helpers.base import Bytes
from app.helpers.qt.pixmaps import Pixmaps


class CoverProps:

    def __init__(self, data: bytes, width: int, height: int, radius: int, ):
        self.__data: bytes = data
        self.__pixmap: QPixmap | None = None
        self.__width: int = width
        self.__height: int = height
        self.__radius: int = radius

    def __eq__(self, o: 'CoverProps') -> bool:
        return (
            self.__data == o.__data and
            self.__width == o.__width and
            self.__height == o.__height and
            self.__radius == o.__radius
        )

    def __hash__(self) -> int:
        return hash((Bytes.decode(self.__data), self.__width, self.__height, self.__radius))

    def data(self) -> bytes:
        return self.__data

    def radius(self) -> int:
        return self.__radius

    def content(self) -> QPixmap:
        return self.__pixmap

    @staticmethod
    def fromBytes(imageByte: bytes, width: int = 0, height: int = 0, radius: int = 0, cropCenter: bool = True, ) -> Optional['CoverProps']:
        if imageByte is None:
            return None

        props = CoverProps(imageByte, width, height, radius)

        pixmap = Pixmaps.toQPixmap(imageByte)
        if pixmap.isNull():
            return None
        if width > 0 or height > 0:
            pixmap = Pixmaps.scaleKeepingRatio(pixmap, max(width, height))
            pixmap = Pixmaps.crop(pixmap, width, height, cropCenter)
        if radius > 0:
            pixmap = Pixmaps.round(pixmap, radius)

        props.__pixmap = pixmap
        return props


class Cover(QLabel):
    __defaultCover: CoverProps
    __currentCover: CoverProps
    __value: float = 0
    __start: float = 0
    __end: float = 0
    __radius: int = 0
    __animation: QVariantAnimation

    def __init__(self, parent: Optional[QWidget] = None):
        QLabel.__init__(self, parent)

    def setDefaultCover(self, cover: CoverProps) -> None:
        self.__defaultCover = cover
        self.setCover(cover)

    def currentCover(self) -> CoverProps:
        return self.__currentCover

    def setRadius(self, radius: int) -> None:
        self.__radius = radius

    def setCover(self, cover: CoverProps) -> None:
        if cover is None:
            cover = self.__defaultCover

        self.__currentCover = cover
        self.setRadius(cover.radius())
        super().setPixmap(cover.content())

    def setAnimation(self, duration: float, start: float, end: float, on_value_changed: Callable) -> None:
        self.__start = start
        self.__end = end
        self.__animation = QVariantAnimation(self, valueChanged=on_value_changed, duration=duration)
        self.__animation.setEasingCurve(QEasingCurve.OutCubic)

    def zoom(self, value: float) -> None:
        self.__value = value
        if self.__currentCover is None:
            return
        pixmap = self.__currentCover.content().copy()
        pixmap = pixmap.scaledToHeight(int(self.height() * value), Qt.SmoothTransformation)
        pixmap = Pixmaps.crop(pixmap, self.width(), self.height())
        pixmap = Pixmaps.round(pixmap, radius=self.__radius)
        self.__setHoverPixmap(pixmap)

    def animationOnEnteredHover(self) -> None:
        if self.__animation is None:
            return
        self.__animation.stop()
        self.__animation.setStartValue(self.__start)
        self.__animation.setEndValue(self.__end)
        self.__animation.start()

    def animationOnLeftHover(self) -> None:
        if self.__animation is None:
            return
        self.__animation.setStartValue(self.__value)
        self.__animation.setEndValue(self.__start)
        self.__animation.start()

    def __setHoverPixmap(self, pixmap: QPixmap) -> None:
        super().setPixmap(pixmap)
