from typing import Optional

from PyQt5.QtWidgets import QWidget

from modules.helpers.types.Decorators import override


class HideableLayout(QWidget):
    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)
        self.__items = []
        self.__next_y = 0
        self.__spacing = 0
        self.__item_width = None

    def setSpacing(self, space: int) -> None:
        self.__spacing = space

    def addWidget(self, widget: QWidget) -> None:
        widget.setParent(self)
        widget.move(self.contentsMargins().left(), self.contentsMargins().top() + self.__next_y)
        if self.__item_width is not None:
            widget.setFixedWidth(self.__item_width)

        self.__next_y += widget.sizeHint().height() + self.__spacing
        self.setFixedHeight(self.__next_y)

        self.__items.append(widget)

    @override
    def setFixedWidth(self, w: int) -> None:
        super().setFixedWidth(w)
        self.__item_width = w - self.contentsMargins().left() - self.contentsMargins().right()
        for item in self.__items:
            item.setFixedWidth(self.__item_width)
