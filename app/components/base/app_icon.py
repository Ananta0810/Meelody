from PyQt5.QtGui import QIcon, QPainter, QPixmap

from app.helpers.stylesheets.color import Color


class AppIcon(QIcon):
    __paintedIcons: dict['AppIcon', dict[Color, 'AppIcon']] = {}

    def __or__(self, other: 'AppIcon') -> 'AppIcon':
        return self if self is not None else other

    def withColor(self, color: Color) -> 'AppIcon':
        if self in AppIcon.__paintedIcons:
            colorDict = AppIcon.__paintedIcons[self]
            if color in colorDict:
                return colorDict[color]

        iconPixmap: QPixmap = self.pixmap(self.availableSizes()[0])
        painter = QPainter(iconPixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(iconPixmap.rect(), color.toQColor())
        painter.end()
        newIcon: QIcon = QIcon()
        newIcon.addPixmap(iconPixmap)

        if self not in AppIcon.__paintedIcons:
            AppIcon.__paintedIcons[self] = {}

        colorDict = AppIcon.__paintedIcons[self]
        colorDict[color] = newIcon

        return newIcon
