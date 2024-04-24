from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from app.common.models import Song
from app.common.others import signalBus
from app.components.scroll_areas import SmoothVerticalScrollArea
from app.views.home.songs_table.song_row import SongRow


class SongsMenu(SmoothVerticalScrollArea):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.__lightMode = True
        self._initComponent()

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

    def _connectSignalSlots(self) -> None:
        signalBus.playlistChanged.connect(lambda playlist: self.__setSongs(playlist.getSongs().getSongs()))

    def __setSongs(self, songs: list[Song]) -> None:
        for song in songs:
            songRow = SongRow(song)
            if self.__lightMode:
                songRow.applyLightMode()
            else:
                songRow.applyDarkMode()
            self._mainLayout.addWidget(songRow)

    def applyLightMode(self) -> None:
        super().applyLightMode()
        self.__lightMode = True

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        self.__lightMode = False
