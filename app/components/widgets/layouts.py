import typing
from typing import Optional, Union

from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLayout, QHBoxLayout


class Box(QVBoxLayout):

    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

    def addLayout(self, layout: Optional[QLayout], stretch: int = None) -> None:
        if stretch is None:
            super().addLayout(layout)
            return
        super().addLayout(layout, stretch)

    def addWidget(self, widget: QWidget, stretch: int = None, alignment: Union[QtCore.Qt.Alignment, QtCore.Qt.AlignmentFlag] = None) -> None:
        if stretch is None:
            if alignment is None:
                super().addWidget(widget)
            else:
                super().addWidget(widget, alignment=alignment)
        else:
            if alignment is None:
                super().addWidget(widget, stretch=stretch)
            else:
                super().addWidget(widget, stretch=stretch, alignment=alignment)

    def addStretch(self, stretch: int = None) -> None:
        if stretch is None:
            super().addStretch()
        else:
            super().addStretch(stretch)


class FlexBox(QHBoxLayout):

    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

    def addLayout(self, layout: Optional[QLayout], stretch: int = None) -> None:
        if stretch is None:
            super().addLayout(layout)
            return
        super().addLayout(layout, stretch)

    def addWidget(self, widget: QWidget, stretch: int = None, alignment: Union[QtCore.Qt.Alignment, QtCore.Qt.AlignmentFlag] = None) -> None:
        if stretch is None:
            if alignment is None:
                super().addWidget(widget)
            else:
                super().addWidget(widget, alignment=alignment)
        else:
            if alignment is None:
                super().addWidget(widget, stretch=stretch)
            else:
                super().addWidget(widget, stretch=stretch, alignment=alignment)

    def addStretch(self, stretch: int = None) -> None:
        if stretch is None:
            super().addStretch()
        else:
            super().addStretch(stretch)
