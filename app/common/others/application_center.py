from typing import Optional

from PyQt5.QtCore import QObject, pyqtSignal

from app.common.models import Playlist


class ApplicationCenter(QObject):
    themeChanged = pyqtSignal(bool)
    playlistChanged = pyqtSignal(Playlist)

    def __init__(self) -> None:
        super().__init__()
        self.isLightMode: bool = True
        self.playlist: Optional[Playlist] = None

    def setLightMode(self, a0: bool) -> None:
        self.isLightMode = a0
        self.themeChanged.emit(a0)

    def setActivePlaylist(self, playlist: Playlist) -> None:
        self.playlist = playlist
        self.playlistChanged.emit(playlist)


appCenter = ApplicationCenter()
