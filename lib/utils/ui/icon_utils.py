
from PyQt5.QtGui import QColor, QIcon, QPainter


class IconUtils:
    @staticmethod
    def colorize(icon: QIcon, color: QColor):
        iconAsPixmap = icon.pixmap(icon.availableSizes()[0])
        painter = QPainter(iconAsPixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(iconAsPixmap.rect(), color)
        painter.end()
        newIcon: QIcon = QIcon()
        newIcon.addPixmap(iconAsPixmap)
        return newIcon
