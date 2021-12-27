from typing import Optional

from constants.ui.base import ApplicationImage
from PyQt5.QtWidgets import QHBoxLayout, QWidget
from views.view import View

from .playlist_info import PlaylistInfo
from .playlist_songs.song_table import SongTable


class CurrentPlaylist(QHBoxLayout, View):
    def __init__(self, parent: Optional["QWidget"] = None):
        super(CurrentPlaylist, self).__init__(parent)
        self.setupUi()

    def setupUi(self) -> None:
        self.info = PlaylistInfo()
        self.info.setDefaultCover(ApplicationImage.defaultPlaylistCover)
        self.songs = SongTable()
        self.songs.setFixedHeight(600)

        self.addLayout(self.info)
        self.addWidget(self.songs, stretch=2)

    def connectToControllers(self, controllers) -> None:
        self.songs.connectToController(controllers.get("playlistSongs"))

    def lightMode(self) -> None:
        self.info.lightMode()
        self.songs.lightMode()
        super().lightMode()

    def darkMode(self) -> None:
        self.info.darkMode()
        self.songs.darkMode()
        super().darkMode()
