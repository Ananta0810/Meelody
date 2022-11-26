from typing import Callable, Optional

from PyQt5.QtCore import QEasingCurve, Qt, QVariantAnimation
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget

from modules.helpers.PixmapHelper import PixmapHelper
from modules.helpers.types.Decorators import override


class ImageViewer(QLabel):
    __default_pixmap: QPixmap
    __current_pixmap: QPixmap
    __value: float = 0
    __start: float = 0
    __end: float = 0
    __radius: int = 0
    __animation: QVariantAnimation

    def __init__(self, parent: Optional["QWidget"] = None):
        QLabel.__init__(self, parent)

    def set_default_pixmap(self, pixmap: QPixmap) -> None:
        self.__default_pixmap = pixmap
        self.setPixmap(pixmap)

    def set_radius(self, radius: int) -> None:
        self.__radius = radius

    @override
    def setPixmap(self, pixmap: QPixmap) -> None:
        if pixmap is None:
            pixmap = self.__default_pixmap
        self.__current_pixmap = pixmap
        super().setPixmap(pixmap)

    def set_animation(self, duration: float, start: float, end: float, on_value_changed: Callable) -> None:
        self.__start = start
        self.__end = end
        self.__animation = QVariantAnimation(self, valueChanged=on_value_changed, duration=duration)
        self.__animation.setEasingCurve(QEasingCurve.OutCubic)

    def zoom(self, value: float) -> None:
        self.__value = value
        if self.__current_pixmap is None:
            return
        pixmap = self.__current_pixmap.copy()
        pixmap = pixmap.scaledToHeight(int(self.height() * value), Qt.SmoothTransformation)
        pixmap = PixmapHelper.crop_pixmap(pixmap, self.width(), self.height())
        pixmap = PixmapHelper.round_pixmap(pixmap, radius=self.__radius)
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
