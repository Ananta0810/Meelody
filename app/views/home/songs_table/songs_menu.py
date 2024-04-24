from typing import Optional

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from app.components.scroll_areas import SmoothVerticalScrollArea
from app.views.home.songs_table.song_row import SongRow


class SongsMenu(SmoothVerticalScrollArea):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._initComponent()

        for i in range(0, 10):
            song = SongRow()
            self._mainLayout.addWidget(song)
            song.applyLightMode()

    def _createUI(self) -> None:
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setClassName("scroll/bg-primary-50 scroll/hover:bg-primary scroll/rounded-2")

        self._menu = QWidget()
        self._menu.setContentsMargins(8, 0, 8, 8)

        self._mainLayout = QVBoxLayout(self._menu)
        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainLayout.setAlignment(Qt.AlignTop)

        self.setWidget(self._menu)

    def sizeHint(self) -> QtCore.QSize:
        hint = super().sizeHint()
        hint.setHeight(1080)
        return hint
