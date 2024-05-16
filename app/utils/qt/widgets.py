from contextlib import suppress
from typing import final

from PyQt5.QtCore import QObject, pyqtBoundSignal
from PyQt5.QtWidgets import QWidget
from PyQt5.sip import isdeleted


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

    @staticmethod
    def isDeleted(widget: QWidget) -> bool:
        return isdeleted(widget)

    @staticmethod
    def disconnect(signal: pyqtBoundSignal, fn: callable) -> None:
        with suppress(TypeError):
            signal.disconnect(fn)
