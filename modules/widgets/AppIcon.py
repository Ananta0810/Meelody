from PyQt5.QtGui import QIcon, QPainter, QPixmap

from modules.models.view.Color import Color


class AppIcon(QIcon):

    def __or__(self, other: 'AppIcon') -> 'AppIcon':
        return self if self is not None else other

    def with_color(self, color: Color):
        icon_pixmap: QPixmap = self.pixmap(self.availableSizes()[0])
        painter = QPainter(icon_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon_pixmap.rect(), color.to_QColor())
        painter.end()
        new_icon: QIcon = QIcon()
        new_icon.addPixmap(icon_pixmap)
        return new_icon
