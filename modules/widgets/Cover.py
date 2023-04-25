from typing import Union

from PyQt5.QtGui import QPixmap

from modules.helpers.PixmapHelper import PixmapHelper


class Cover:

    def __init__(self, pixmap: QPixmap, radius: int):
        self.__pixmap: QPixmap = pixmap
        self.__radius: int = radius

    def radius(self) -> int:
        return self.__radius

    def content(self) -> QPixmap:
        return self.__pixmap

    __covers: dict[str, 'Cover'] = {}

    @staticmethod
    def from_bytes(
        image_byte: bytes,
        width: int,
        height: int,
        radius: int = 0,
        crop_center: bool = True,
    ) -> Union['Cover', None]:
        key = str(image_byte)
        if key in Cover.__covers:
            return Cover.__covers[key]
        pixmap = PixmapHelper.get_pixmap_from_bytes(image_byte)
        if pixmap.isNull():
            return None
        pixmap = PixmapHelper.scale_pixmap_keeping_ratio(pixmap, max(width, height))
        pixmap = PixmapHelper.crop_pixmap(pixmap, width, height, crop_center)
        pixmap = PixmapHelper.round_pixmap(pixmap, radius)
        cover = Cover(pixmap, radius)
        Cover.__covers[key] = cover
        return cover
