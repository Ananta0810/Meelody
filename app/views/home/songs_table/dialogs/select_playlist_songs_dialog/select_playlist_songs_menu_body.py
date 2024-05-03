from typing import Optional, Union

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from app.common.others import appCenter
from app.components.scroll_areas import StyleScrollArea
from app.components.widgets import Box, StyleWidget
from app.views.home.songs_table.dialogs.select_playlist_songs_dialog.select_playlist_song_row import SongRow


class MenuBody(StyleScrollArea):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self._initComponent()
        self.__setSongs()

    def _createUI(self) -> None:
        super()._createUI()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self._menu = StyleWidget()
        self._menu.setClassName("bg-none")
        self._menu.setContentsMargins(0, 0, 0, 0)

        self._mainLayout = Box(self._menu)
        self._mainLayout.setAlignment(Qt.AlignTop)

        self.setWidget(self._menu)

    def addWidget(self, widget: QWidget, stretch: int = None, alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = None) -> None:
        self._mainLayout.addWidget(widget, stretch, alignment)

    def removeWidget(self, widget: QWidget) -> None:
        self._mainLayout.removeWidget(widget)

    def __setSongs(self) -> None:
        for song in appCenter.library.getSongs().getSongs():
            songRow = SongRow(song)
            songRow.applyTheme()
            self.addWidget(songRow)
