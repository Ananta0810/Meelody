from typing import Optional

from PyQt5.QtGui import QPixmap


class MeelodyPixmap(QPixmap):

    def __init__(self, pixmap: QPixmap, radius: int, parent: Optional["QWidget"] = None):
        QPixmap.__init__(self, parent)
        self.__pixmap: QPixmap = pixmap
        self.__radius: int = radius

    def radius(self) -> int:
        return self.__radius

    def pixmap(self) -> QPixmap:
        return self.__pixmap

    def __getattr__(self, item):
        try:
            return getattr(self, item)
        except AttributeError:
            return getattr(self.__pixmap, item)
