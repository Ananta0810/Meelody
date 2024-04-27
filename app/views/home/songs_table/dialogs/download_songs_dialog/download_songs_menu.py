from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout

from app.views.home.songs_table.dialogs.download_songs_dialog.download_song_item import DownloadSongItem


class DownloadSongsMenu(QScrollArea):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._createUI()

    def _createUI(self) -> None:
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self._inner = QWidget(self)
        self.setWidget(self._inner)

        self._menu = QVBoxLayout(self._inner)
        self._menu.setAlignment(Qt.AlignTop)
        self._menu.setSpacing(0)
        self._menu.setContentsMargins(0, 0, 0, 0)

    def addItem(self) -> DownloadSongItem:
        row = DownloadSongItem()
        row.setFixedHeight(64)
        row.applyTheme()
        self._menu.addWidget(row)
        return row
