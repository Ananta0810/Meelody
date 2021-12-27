from PyQt5.QtWidgets import *
from typing import Optional


class MinimizedWindow(QHBoxLayout):
    def __init__(self, parent: Optional["QWidget"] = None):
        super(MinimizedWindow, self).__init__(parent)

    def addWidget(
        self,
        a0: QWidget,
        stretch: int = ...,
        alignment: typing.Union[QtCore.Qt.Alignment, QtCore.Qt.AlignmentFlag] = ...,
    ) -> None:
        return super().addWidget(a0, stretch=stretch, alignment=alignment)

    def addLayout(self, layout: QLayout, stretch: int = ...) -> None:
        return super().addLayout(layout, stretch=stretch)
