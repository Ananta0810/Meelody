import typing
from typing import Optional, Union

from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLayout, QHBoxLayout


class Box(QVBoxLayout):

    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

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

    def insertWidget(
        self,
        index: int,
        widget: Optional[QWidget], stretch: int = None,
        alignment: Union[QtCore.Qt.Alignment, QtCore.Qt.AlignmentFlag] = None
    ) -> None:
        if stretch is None:
            if alignment is None:
                super().insertWidget(index, widget)
            else:
                super().insertWidget(index, widget, alignment=alignment)
        else:
            if alignment is None:
                super().insertWidget(index, widget, stretch=stretch)
            else:
                super().insertWidget(index, widget, stretch=stretch, alignment=alignment)

    def addStretch(self, stretch: int = None) -> None:
        if stretch is None:
            super().addStretch()
        else:
            super().addStretch(stretch)

    def addSpacing(self, size: int) -> None:
        super().addSpacing(size)

    def clear(self) -> None:
        for i in reversed(range(self.count())):
            widgetToRemove = self.itemAt(i).widget()
            # remove it from the layout list
            self.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)


class FlexBox(QHBoxLayout):

    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

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

    def insertWidget(
        self,
        index: int,
        widget: Optional[QWidget], stretch: int = None,
        alignment: Union[QtCore.Qt.Alignment, QtCore.Qt.AlignmentFlag] = None
    ) -> None:
        if stretch is None:
            if alignment is None:
                super().insertWidget(index, widget)
            else:
                super().insertWidget(index, widget, alignment=alignment)
        else:
            if alignment is None:
                super().insertWidget(index, widget, stretch=stretch)
            else:
                super().insertWidget(index, widget, stretch=stretch, alignment=alignment)

    def addStretch(self, stretch: int = None) -> None:
        if stretch is None:
            super().addStretch()
        else:
            super().addStretch(stretch)

    def clear(self) -> None:
        for i in reversed(range(self.count())):
            widgetToRemove = self.itemAt(i).widget()
            # remove it from the layout list
            self.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)
