from typing import final

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget


@final
class Widgets:

    @staticmethod
    def isInView(widget: QWidget) -> bool:
        return not widget.visibleRegion().isEmpty()

    @staticmethod
    def isDescendantOf(ancestorWidget: QObject, widget: QObject) -> bool:
        ancestor = widget.parent()
        while ancestor is not None:
            if ancestor == ancestorWidget:
                return True
            ancestor = ancestor.parent()
        return False
