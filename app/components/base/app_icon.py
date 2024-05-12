from PyQt5.QtGui import QIcon, QPainter, QPixmap

from app.helpers.stylesheets import Color
from app.utils.base import memoizeResult


class AppIcon(QIcon):

    def __init__(self, path: str):
        super().__init__(path)
        self.__path = path

    def __str__(self) -> str:
        return self.__path

    @memoizeResult
    def withColor(self, color: Color) -> 'AppIcon':
        iconPixmap: QPixmap = self.pixmap(self.availableSizes()[0])

        painter = QPainter(iconPixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(iconPixmap.rect(), color.toQColor())
        painter.end()
        newIcon: QIcon = QIcon()
        newIcon.addPixmap(iconPixmap)

        return newIcon
