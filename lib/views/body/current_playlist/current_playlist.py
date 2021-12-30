from typing import Optional

from constants.ui.base import ApplicationImage
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QWidget
from views.view import View

from .playlist_info import PlaylistInfo
from .playlist_songs.song_table import SongTable


class CurrentPlaylist(QWidget, View):
    def __init__(self, parent: Optional["QWidget"] = None):
        super(CurrentPlaylist, self).__init__(parent)
        self.setupUi()

    def setupUi(self) -> None:
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignLeft)
        self.mainLayout.setSpacing(50)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.info = PlaylistInfo()
        self.info.setDefaultCover(ApplicationImage.defaultPlaylistCover)
        self.songs = SongTable()

        self.mainLayout.addLayout(self.info)
        self.mainLayout.addWidget(self.songs, stretch=2)

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

    def setCurrentPlaylistInfo(self, name: str, length: int, cover: bytes = None) -> None:
        if cover is None:
            cover = (
                ApplicationImage.favouritesCover
                if name.lower() == "favourites"
                else ApplicationImage.defaultPlaylistCover
            )

        self.info.setCover(cover)
        self.info.setLabel(name)
        self.info.setTotalSong(length)

    def connectToController(self, controller) -> None:
        self.songs.body.connectToController(controller)

    def selectItem(self, index: int) -> None:
        self.songs.body.scrollToItem(index)

    def setSongCoverAtIndex(self, index: int, cover: bytes) -> None:
        self.songs.body.__getSongByIndex(index).setCover(cover)

    def setSongTitleAtIndex(self, index: int, title: str) -> None:
        self.songs.body.__getSongByIndex(index).setTitle(title)

    def setSongArtistAtIndex(self, index: int, artist: str) -> None:
        self.songs.body.__getSongByIndex(index).setArtist(artist)

    def setSongLengthAtIndex(self, index: int, length: float) -> None:
        self.songs.body.__getSongByIndex(index).setLength(length)

    def setSongLoveStateAtIndex(self, index: int, state: bool) -> None:
        self.songs.body.__getSongByIndex(index).setLoveState(state)

    def updateLayout(self, totalItem: int, controller) -> None:
        self.songs.body.updateLayout(totalItem, controller)

    def displaySongInfoAtIndex(self, index: int, cover: bytes, title: str, artist: str, length: float) -> None:
        self.songs.body.displaySongInfoAtIndex(index, cover, title, artist, length)
