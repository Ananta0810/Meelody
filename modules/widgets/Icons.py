from PyQt5.QtGui import QIcon, QPainter, QPixmap

from modules.models.view.Color import Color


class AppIcon(QIcon):
    __painted_covers: dict['AppIcon', dict[Color, 'AppIcon']] = {}

    def __or__(self, other: 'AppIcon') -> 'AppIcon':
        return self if self is not None else other

    def with_color(self, color: Color) -> 'AppIcon':
        if self in AppIcon.__painted_covers:
            color_dict = AppIcon.__painted_covers[self]
            if color in color_dict:
                return color_dict[color]

        icon_pixmap: QPixmap = self.pixmap(self.availableSizes()[0])
        painter = QPainter(icon_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon_pixmap.rect(), color.to_QColor())
        painter.end()
        new_icon: QIcon = QIcon()
        new_icon.addPixmap(icon_pixmap)

        if self not in AppIcon.__painted_covers:
            AppIcon.__painted_covers[self] = {}

        color_dict = AppIcon.__painted_covers[self]
        color_dict[color] = new_icon

        return new_icon
