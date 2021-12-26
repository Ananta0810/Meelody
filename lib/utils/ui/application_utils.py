from functools import lru_cache
from typing import Any

from modules.screens.qss.qss_elements import Color
from PyQt5.QtGui import QIcon, QPixmap
from widgets.scaleable_qpixmap import ScaleAblePixmap

from .color_utils import ColorUtils
from .icon_utils import IconUtils
from .pixmap_utils import PixmapUtils


class UiUtils:
    @staticmethod
    @lru_cache(maxsize=None)
    def paintIcon(icon: QIcon, color: Color):
        return IconUtils.colorize(icon, ColorUtils.getQColorFromColor(color))

    @staticmethod
    def getSquaredPixmapFromBytes(byteImage: bytes, edge: int, radius: int) -> QPixmap:
        pixmap = PixmapUtils.getPixmapFromBytes(byteImage)
        if pixmap.isNull():
            return None
        pixmap = PixmapUtils.scalePixmapKeepingRatio(pixmap, edge)
        pixmap = PixmapUtils.squarePixmap(pixmap)
        pixmap = PixmapUtils.roundPixmap(pixmap, radius)
        return pixmap

    @staticmethod
    def getEditedPixmapFromBytes(
        byteImage: bytes,
        width: int,
        height,
        cropCenter: bool = True,
        radius: int = 0,
    ) -> ScaleAblePixmap:
        pixmap = PixmapUtils.getPixmapFromBytes(byteImage)
        if pixmap.isNull():
            return None
        pixmap = PixmapUtils.scalePixmapKeepingRatio(pixmap, max(width, height))
        pixmap = PixmapUtils.cropPixmap(pixmap, width, height, cropCenter)
        pixmap = PixmapUtils.roundPixmap(pixmap, radius)
        return pixmap

    @staticmethod
    def setAttribute(parent: Any, object: str, index: int, value: Any) -> None:
        setattr(parent, "_".join([object, str(index)]), value)

    @staticmethod
    def getAttribute(parent: Any, object: str, index: int) -> Any:
        try:
            return getattr(parent, "_".join([object, str(index)]))
        except AttributeError:
            return None
