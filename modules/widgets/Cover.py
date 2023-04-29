from typing import Callable, Optional, Union

from PyQt5.QtCore import QEasingCurve, Qt, QVariantAnimation
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget

from modules.helpers import Pixmaps


class CoverProp:

    def __init__(self,
                 pixmap: QPixmap,
                 width: int,
                 height: int,
                 radius: int,
                 ):
        self.__pixmap: QPixmap = pixmap
        self.__width: int = width
        self.__height: int = height
        self.__radius: int = radius

    def radius(self) -> int:
        return self.__radius

    def content(self) -> QPixmap:
        return self.__pixmap

    @staticmethod
    def from_bytes(
        image_byte: bytes,
        width: int,
        height: int,
        radius: int = 0,
        crop_center: bool = True,
    ) -> Union['CoverProp', None]:
        pixmap = Pixmaps.get_pixmap_from_bytes(image_byte)
        if pixmap.isNull():
            return None
        pixmap = Pixmaps.scale_pixmap_keeping_ratio(pixmap, max(width, height))
        pixmap = Pixmaps.crop_pixmap(pixmap, width, height, crop_center)
        pixmap = Pixmaps.round_pixmap(pixmap, radius)
        return CoverProp(pixmap, width, height, radius)


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

    def current_cover(self) -> QPixmap:
        return self.__current_cover.content()

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
