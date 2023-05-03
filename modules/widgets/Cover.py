from typing import Callable, Optional, Union

from PyQt5.QtCore import QEasingCurve, Qt, QVariantAnimation
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget

from modules.helpers import Pixmaps
from modules.helpers.types.Bytes import Bytes


class CoverProp:
    __created_covers: dict['CoverProp', QPixmap] = {}

    def __init__(self,
                 data: bytes,
                 width: int,
                 height: int,
                 radius: int,
                 ):
        self.__data: bytes = data
        self.__pixmap: QPixmap | None = None
        self.__width: int = width
        self.__height: int = height
        self.__radius: int = radius

    def __eq__(self, o: 'CoverProp') -> bool:
        return (
            self.__data == o.__data and
            self.__width == o.__width and
            self.__height == o.__height and
            self.__radius == o.__radius
        )

    def __hash__(self) -> int:
        return hash((Bytes.decode(self.__data), self.__width, self.__height, self.__radius))

    def __set_pixmap(self, pixmap: QPixmap) -> None:
        self.__pixmap = pixmap

    def data(self) -> bytes:
        return self.__data

    def radius(self) -> int:
        return self.__radius

    def content(self) -> QPixmap:
        return self.__pixmap

    @staticmethod
    def from_bytes(
        image_byte: bytes,
        width: int = 0,
        height: int = 0,
        radius: int = 0,
        crop_center: bool = True,
    ) -> Union['CoverProp', None]:
        cover = CoverProp(image_byte, width, height, radius)
        if cover in CoverProp.__created_covers:
            pixmap = CoverProp.__created_covers[cover]
            cover.__set_pixmap(pixmap)
            return cover

        pixmap = Pixmaps.get_pixmap_from_bytes(image_byte)
        if pixmap.isNull():
            return None
        if width > 0 or height > 0:
            pixmap = Pixmaps.scale_pixmap_keeping_ratio(pixmap, max(width, height))
            pixmap = Pixmaps.crop_pixmap(pixmap, width, height, crop_center)
        if radius > 0:
            pixmap = Pixmaps.round_pixmap(pixmap, radius)

        cover.__set_pixmap(pixmap)
        CoverProp.__created_covers[cover] = pixmap
        return cover


class Cover(QLabel):
    __default_cover: CoverProp
    __current_cover: CoverProp
    __value: float = 0
    __start: float = 0
    __end: float = 0
    __radius: int = 0
    __animation: QVariantAnimation

    def __init__(self, parent: Optional["QWidget"] = None):
        QLabel.__init__(self, parent)

    def set_default_cover(self, cover: CoverProp) -> None:
        self.__default_cover = cover
        self.set_cover(cover)

    def current_cover(self) -> CoverProp:
        return self.__current_cover

    def set_radius(self, radius: int) -> None:
        self.__radius = radius

    def set_cover(self, cover: CoverProp) -> None:
        if cover is None:
            cover = self.__default_cover

        self.__current_cover = cover
        self.set_radius(cover.radius())
        super().setPixmap(cover.content())

    def set_animation(self, duration: float, start: float, end: float, on_value_changed: Callable) -> None:
        self.__start = start
        self.__end = end
        self.__animation = QVariantAnimation(self, valueChanged=on_value_changed, duration=duration)
        self.__animation.setEasingCurve(QEasingCurve.OutCubic)

    def zoom(self, value: float) -> None:
        self.__value = value
        if self.__current_cover is None:
            return
        pixmap = self.__current_cover.content().copy()
        pixmap = pixmap.scaledToHeight(int(self.height() * value), Qt.SmoothTransformation)
        pixmap = Pixmaps.crop_pixmap(pixmap, self.width(), self.height())
        pixmap = Pixmaps.round_pixmap(pixmap, radius=self.__radius)
        self.__set_hover_pixmap(pixmap)

    def animation_on_entered_hover(self) -> None:
        if self.__animation is None:
            return
        self.__animation.stop()
        self.__animation.setStartValue(self.__start)
        self.__animation.setEndValue(self.__end)
        self.__animation.start()

    def animation_on_left_hover(self) -> None:
        if self.__animation is None:
            return
        self.__animation.setStartValue(self.__value)
        self.__animation.setEndValue(self.__start)
        self.__animation.start()

    def __set_hover_pixmap(self, pixmap: QPixmap) -> None:
        super().setPixmap(pixmap)
