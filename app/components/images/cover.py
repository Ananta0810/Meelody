from typing import Optional

from PyQt5.QtCore import QVariantAnimation, QEasingCurve, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget

from app.utils.base import Bytes
from app.utils.qt.pixmaps import Pixmaps
from app.utils.reflections import memoizeResult, suppressException


class Cover(QLabel):
    class Props:

        def __init__(self, data: bytes, width: int, height: int, radius: int, ):
            self.__data: bytes = data
            self.__pixmap: QPixmap | None = None
            self.__width: int = width
            self.__height: int = height
            self.__radius: int = radius

        def __eq__(self, o: 'Cover.Props') -> bool:
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
        @memoizeResult
        def fromBytes(imageByte: bytes, width: int = 0, height: int = 0, radius: int = 0, cropCenter: bool = True) -> Optional['Cover.Props']:
            if imageByte is None:
                return None

            props = Cover.Props(imageByte, width, height, radius)

            pixmap = Pixmaps.toQPixmap(imageByte)
            if pixmap.isNull():
                return props

            if width > 0 or height > 0:
                pixmap = Pixmaps.scaleKeepingRatio(pixmap, max(width, height))
                pixmap = Pixmaps.crop(pixmap, width, height, cropCenter)

            if radius > 0:
                pixmap = Pixmaps.round(pixmap, radius)

            props.__pixmap = pixmap
            return props

    def __init__(self, parent: Optional[QWidget] = None):
        self._currentCover: Optional[Cover.Props] = None
        QLabel.__init__(self, parent)

    def currentCover(self) -> 'Cover.Props':
        return self._currentCover

    @suppressException
    def setCover(self, cover: 'Cover.Props') -> None:
        self._currentCover = cover
        super().setPixmap(cover.content())


class CoverWithPlaceHolder(Cover):

    def __init__(self, parent: Optional[QWidget] = None):
        Cover.__init__(self, parent)
        self.__defaultCover: Optional[Cover.Props] = None

    def setPlaceHolderCover(self, cover: Cover.Props) -> None:
        self.__defaultCover = cover
        self.setCover(cover)

    @suppressException
    def setCover(self, cover: Cover.Props) -> None:
        super().setCover(cover or self.__defaultCover)


class ZoomCover(Cover):

    def __init__(self, parent: Optional[QWidget] = None):
        Cover.__init__(self, parent)
        self.__value: float = 0
        self.__start: float = 0
        self.__end: float = 0
        self.__animation = QVariantAnimation(self, valueChanged=self.__zoom)
        self.__animation.setEasingCurve(QEasingCurve.OutCubic)

    def setAnimation(self, duration: float, start: float, end: float) -> None:
        self.__start = start
        self.__end = end
        self.__animation.setDuration(duration)

    def __zoom(self, value: float) -> None:
        self.__value = value
        if self._currentCover is None or self.__animation is None:
            return

        pixmap = self._currentCover.content().copy()
        pixmap = pixmap.scaledToHeight(int(self.height() * value), Qt.SmoothTransformation)
        pixmap = Pixmaps.crop(pixmap, self.width(), self.height())
        pixmap = Pixmaps.round(pixmap, radius=self._currentCover.radius())
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
