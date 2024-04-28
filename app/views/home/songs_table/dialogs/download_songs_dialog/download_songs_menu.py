from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from app.components.scroll_areas import StyleScrollArea
from app.views.home.songs_table.dialogs.download_songs_dialog.download_song_item import DownloadSongItem


class DownloadSongsMenu(StyleScrollArea):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._widgets: list[QWidget] = []
        self._initComponent()
        self.setFixedHeight(0)

    def _createUI(self) -> None:
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._menu = QWidget(self)
        self.setWidget(self._menu)

        self._mainLayout = QVBoxLayout(self._menu)
        self._mainLayout.setAlignment(Qt.AlignTop)
        self._mainLayout.setSpacing(0)
        self._mainLayout.setContentsMargins(0, 0, 0, 0)

    def addItem(self) -> DownloadSongItem:
        row = DownloadSongItem()
        row.setFixedHeight(64)
        row.applyTheme()
        self._widgets.append(row)
        self._mainLayout.addWidget(row)
        self._updateHeight(row)
        return row

    def _updateHeight(self, row):
        height_ = min(len(self._widgets), 3) * row.height()
        self.setFixedHeight(height_)
