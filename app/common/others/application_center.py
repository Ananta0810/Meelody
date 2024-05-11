from PyQt5.QtCore import QObject, pyqtSignal

from app.common.models import Playlist, ThemeMode
from app.common.others.application_settings import AppSettings
from app.common.others.playlists import Playlists


class ApplicationCenter(QObject):
    themeChanged = pyqtSignal(bool)
    currentPlaylistChanged = pyqtSignal(Playlist)
    exited = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        from app.common.models.playlists import Library
        self.settings: AppSettings = AppSettings()

        self.isLightMode: bool = ThemeMode.systemTheme() if self.settings.theme == ThemeMode.SYSTEM else self.settings.theme == ThemeMode.LIGHT
        self.playlists: Playlists = Playlists()

        self.library: Library = Library(Library.Info(), Library.Songs())
        self.currentPlaylist: Playlist = self.library

    def setTheme(self, theme: ThemeMode) -> None:
        self.isLightMode = ThemeMode.systemTheme() if theme == ThemeMode.SYSTEM else theme == ThemeMode.LIGHT
        self.settings.setTheme(theme)
        self.themeChanged.emit(self.isLightMode)

    def setActivePlaylist(self, playlist: Playlist) -> None:
        self.currentPlaylist = playlist
        self.currentPlaylistChanged.emit(playlist)

    def setPlaylists(self, playlists: list[Playlist]) -> None:
        self.playlists.load(playlists)


appCenter = ApplicationCenter()
