from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from app.common.statics.qt import Cursors
from app.views.home.songs_table.songs_menu import SongsMenu
from app.views.home.songs_table.songs_table_header import SongsTableHeader


class SongsTable(QWidget):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.__initUI()

    def __initUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._mainLayout = QVBoxLayout(self)
        self._mainLayout.setAlignment(Qt.AlignTop)
        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainLayout.setSpacing(4)

        self._header = SongsTableHeader()
        self._header.setFixedHeight(48)

        self._menu = SongsMenu()
        self._menu.setClassName("scroll/bg-primary-75 scroll/hover:bg-primary scroll/rounded-2")
        self._menu.setContentsMargins(8, 0, 8, 0)
        self._menu.verticalScrollBar().setCursor(Cursors.pointer)

        self._mainLayout.addWidget(self._header)
        self._mainLayout.addWidget(self._menu)
