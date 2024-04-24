from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QWidget

from app.components.scroll_areas import SmoothVerticalScrollArea
from app.views.home.songs_table.song_row import SongRow


class MenuLayout(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.__items = []
        self.__nextY = 0
        self.__spacing = 0
        self.__itemWidth = None
        self.__totalDisplaying: int = 0
        self.__yPostToLastItemList = []

    def setSpacing(self, space: int) -> None:
        self.__spacing = space
        self.__nextY = 0
        self.__yPostToLastItemList = []

        for item in self.__items:
            self.__moveWidget(item)

        self.setFixedHeight(self.__nextY)

    def addWidget(self, widget: QWidget) -> None:
        widget.setParent(self)
        self.__moveWidget(widget)
        self.setFixedHeight(self.__nextY)
        self.__items.append(widget)

    def __moveWidget(self, widget):
        margins = self.contentsMargins()

        widget.move(margins.left(), margins.top() + self.__nextY)
        if self.__itemWidth is not None:
            widget.setFixedWidth(self.__itemWidth)

        height = widget.sizeHint().height() + self.__spacing
        self.__yPostToLastItemList.append(height)

        self.__nextY += height

    def displayNFirst(self, totalItems: int) -> None:
        if self.__totalDisplaying == totalItems:
            return
        self.__totalDisplaying = totalItems
        display_items = self.__yPostToLastItemList[0: totalItems]
        self.setFixedHeight(sum(display_items))

    def getTotalDisplaying(self):
        return self.__totalDisplaying

    def setFixedWidth(self, w: int) -> None:
        super().setFixedWidth(w)
        self.__itemWidth = w - self.contentsMargins().left() - self.contentsMargins().right()
        for item in self.__items:
            item.setFixedWidth(self.__itemWidth)


class SongsMenu(SmoothVerticalScrollArea):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.start: int = 0
        self.last: int = 6
        self.__items: list[SongRow] = []
        self._currentSongIndex: list[int] = []
        self._createUI()
        for i in range(0, 10):
            song = SongRow()
            self._menu.addWidget(song)
            song.applyLightMode()

    def _createUI(self) -> None:
        self.setContentsMargins(0, 0, 0, 0)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setItemHeight(104)

        self._menu = MenuLayout(self)
        self._menu.setContentsMargins(8, 0, 8, 8)

        self.setWidget(self._menu)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self._menu.setFixedWidth(self.rect().width() - 4)
        super().resizeEvent(a0)
