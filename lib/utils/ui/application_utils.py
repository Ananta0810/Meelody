from sys import path

from PyQt5.QtGui import QIcon, QPixmap

from .color_utils import ColorUtils
from .icon_utils import IconUtils
from .pixmap_utils import PixmapUtils

path.append("./lib")
from modules.screens.qss.qss_elements import Color


class ApplicationUIUtils:
    @staticmethod
    def paintIcon(icon: QIcon, color: Color):
        return IconUtils.colorize(icon, ColorUtils.getQColorFromColor(color))

    @staticmethod
    def getSquaredPixmapFromBytes(
        byteImage: bytes, edge: int, radius: int
    ) -> QPixmap:
        pixmap = PixmapUtils.getPixmapFromBytes(byteImage)
        pixmap = PixmapUtils.cropPixmap(pixmap, edge)
        pixmap = PixmapUtils.squarePixmap(pixmap)
        pixmap = PixmapUtils.roundPixmap(pixmap, radius=radius)
        return pixmap
