from typing import Optional

from PyQt5.QtWidgets import QWidget

from modules.helpers.types.Decorators import override


class MenuLayout(QWidget):
    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)
        self.__items = []
        self.__next_y = 0
        self.__spacing = 0
        self.__item_width = None
        self.__total_displaying: int = 0
        self.__y_post_to_last_item_list = []

    def setSpacing(self, space: int) -> None:
        self.__spacing = space
        self.__next_y = 0
        self.__y_post_to_last_item_list = []

        for item in self.__items:
            self.__move_widget(item)

        self.setFixedHeight(self.__next_y)

    def addWidget(self, widget: QWidget) -> None:
        widget.setParent(self)
        self.__move_widget(widget)
        self.setFixedHeight(self.__next_y)
        self.__items.append(widget)

    def __move_widget(self, widget):
        margins = self.contentsMargins()

        widget.move(margins.left(), margins.top() + self.__next_y)
        if self.__item_width is not None:
            widget.setFixedWidth(self.__item_width)

        height = widget.sizeHint().height() + self.__spacing
        self.__y_post_to_last_item_list.append(height)

        self.__next_y += height

    def displayNFirst(self, total_items: int) -> None:
        if self.__total_displaying == total_items:
            return
        self.__total_displaying = total_items
        display_items = self.__y_post_to_last_item_list[0: total_items]
        self.setFixedHeight(sum(display_items))

    def getTotalDisplaying(self):
        return self.__total_displaying

    @override
    def setFixedWidth(self, w: int) -> None:
        super().setFixedWidth(w)
        self.__item_width = w - self.contentsMargins().left() - self.contentsMargins().right()
        for item in self.__items:
            item.setFixedWidth(self.__item_width)
