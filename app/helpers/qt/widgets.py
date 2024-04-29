from typing import final

from PyQt5.QtWidgets import QWidget


@final
class Widgets:

    @staticmethod
    def isInView(widget: QWidget) -> bool:
        return not widget.visibleRegion().isEmpty()
