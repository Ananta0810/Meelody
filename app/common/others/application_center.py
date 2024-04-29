from PyQt5.QtCore import QObject, pyqtSignal

from app.common.models import Playlist
from app.common.others.playlists import Playlists


class ApplicationCenter(QObject):
    themeChanged = pyqtSignal(bool)
    currentPlaylistChanged = pyqtSignal(Playlist)
    exited = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.isLightMode: bool = True
        self.playlists: Playlists = Playlists()

        self.library: Playlist = None
        self.currentPlaylist: Playlist = None

    def setLightMode(self, a0: bool) -> None:
        self.isLightMode = a0
        self.themeChanged.emit(a0)

    def setLibrary(self, playlist: Playlist) -> None:
        self.library = playlist

    def setActivePlaylist(self, playlist: Playlist) -> None:
        self.currentPlaylist = playlist
        self.currentPlaylistChanged.emit(playlist)

    def setPlaylists(self, playlists: list[Playlist]) -> None:
        self.playlists.appendAll(playlists)


appCenter = ApplicationCenter()
