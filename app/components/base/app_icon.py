from PyQt5.QtGui import QIcon, QPainter, QPixmap

from app.helpers.stylesheets import Color


class AppIcon(QIcon):
    __paintedCovers: dict['AppIcon', dict[Color, 'AppIcon']] = {}

    def __or__(self, other: 'AppIcon') -> 'AppIcon':
        return self if self is not None else other

    def withColor(self, color: Color) -> 'AppIcon':
        if self in AppIcon.__paintedCovers:
            colorDict = AppIcon.__paintedCovers[self]
            if color in colorDict:
                return colorDict[color]

        icon_pixmap: QPixmap = self.pixmap(self.availableSizes()[0])
        painter = QPainter(icon_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon_pixmap.rect(), color.toQColor())
        painter.end()
        new_icon: QIcon = QIcon()
        new_icon.addPixmap(icon_pixmap)

        if self not in AppIcon.__paintedCovers:
            AppIcon.__paintedCovers[self] = {}

        colorDict = AppIcon.__paintedCovers[self]
        colorDict[color] = new_icon

        return new_icon
