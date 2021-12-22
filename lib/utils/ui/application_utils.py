from sys import path

from PyQt5.QtGui import QIcon, QPixmap

from .color_utils import ColorUtils
from .icon_utils import IconUtils
from .pixmap_utils import PixmapUtils

path.append("./lib")
from modules.screens.qss.qss_elements import Color
from widgets.scaleable_qpixmap import ScaleAblePixmap


class ApplicationUIUtils:
    @staticmethod
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
