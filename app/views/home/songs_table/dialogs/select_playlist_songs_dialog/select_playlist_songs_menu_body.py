from typing import Optional

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget

from app.common.models import Song
from app.common.others import appCenter
from app.components.scroll_areas import StyleScrollArea
from app.components.widgets import Box, StyleWidget
from app.views.home.songs_table.dialogs.select_playlist_songs_dialog.select_playlist_song_row import SongRow


class MenuBody(StyleScrollArea):
    songSelected = pyqtSignal(Song)
    songUnSelected = pyqtSignal(Song)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        self.__rowDict: dict[str, SongRow] = {}

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

    def __setSongs(self) -> None:
        for song in appCenter.library.getSongs().getSongs():
            songRow = SongRow(song)
            songRow.applyTheme()
            songRow.checked.connect(lambda _song: self.songSelected.emit(_song))
            songRow.unchecked.connect(lambda _song: self.songUnSelected.emit(_song))
            self._mainLayout.addWidget(songRow)
            self.__rowDict[song.getId()] = songRow

    def setSelectedSongs(self, songs: list[Song]) -> None:
        for song in songs:
            self.__rowDict[song.getId()].select()
