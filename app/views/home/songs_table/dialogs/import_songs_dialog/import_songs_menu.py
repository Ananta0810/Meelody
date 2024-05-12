from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from app.components.scroll_areas import StyleScrollArea
from app.resource.qt import Cursors
from app.views.home.songs_table.dialogs.import_songs_dialog.import_song_item import ImportSongItem


class ImportSongsMenu(StyleScrollArea):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._widgets: list[ImportSongItem] = []
        self._initComponent()

    def _createUI(self) -> None:
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.verticalScrollBar().setCursor(Cursors.pointer)

        self._menu = QWidget(self)
        self.setWidget(self._menu)

        self._mainLayout = QVBoxLayout(self._menu)
        self._mainLayout.setAlignment(Qt.AlignTop)
        self._mainLayout.setSpacing(12)
        self._mainLayout.setContentsMargins(12, 0, 12, 0)

    def addItem(self, path: str) -> ImportSongItem:
        row = ImportSongItem(path)
        row.applyTheme()

        self._widgets.append(row)
        self._mainLayout.addWidget(row)
        self._updateHeight(row)
        return row

    def _updateHeight(self, row) -> None:
        totalShown = min(len(self._widgets), 6)
        height_ = totalShown * row.height() + (totalShown - 1) * self._mainLayout.spacing()
        self.setFixedHeight(height_)

    def items(self) -> list[ImportSongItem]:
        return self._widgets
