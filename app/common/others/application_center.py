from typing import Optional

from PyQt5.QtCore import QObject, pyqtSignal

from app.common.models import Playlist


class ApplicationCenter(QObject):
    themeChanged = pyqtSignal(bool)
    playlistsChanged = pyqtSignal(list)
    currentPlaylistChanged = pyqtSignal(Playlist)

    def __init__(self) -> None:
        super().__init__()
        self.isLightMode: bool = True
        self.currentPlaylist: Optional[Playlist] = None
        self.playlists: list[Playlist] = []

    def setLightMode(self, a0: bool) -> None:
        self.isLightMode = a0
        self.themeChanged.emit(a0)

    def setActivePlaylist(self, playlist: Playlist) -> None:
        self.currentPlaylist = playlist
        self.currentPlaylistChanged.emit(playlist)

    def setPlaylists(self, playlists: list[Playlist]) -> None:
        self.playlists = playlists
        self.playlistsChanged.emit(playlists)


appCenter = ApplicationCenter()
