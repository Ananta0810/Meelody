from PyQt5.QtGui import QColor, QIcon, QPainter


class ColorChangalbeButton(QIcon):
    def __init__(self, parent=None):
        super().__init__(parent)

    def setIconColor(self, color: QColor):
        iconAsPixmap = self.pixmap(self.size())
        painter = QPainter(iconAsPixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(iconAsPixmap.rect(), color)
        painter.end()
        self.addPixmap(iconAsPixmap)
        return self
