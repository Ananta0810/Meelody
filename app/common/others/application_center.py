from PyQt5.QtCore import QObject, pyqtSignal

from app.common.models import Playlist
from app.common.others.application_settings import AppSettings
from app.common.others.playlists import Playlists
from app.common.statics.enums import ThemeMode
from app.helpers.systems import Systems


class ApplicationCenter(QObject):
    themeChanged = pyqtSignal(bool)
    currentPlaylistChanged = pyqtSignal(Playlist)
    exited = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        from app.common.models.playlists import Library
        self.settings: AppSettings = AppSettings()

        self.isLightMode: bool = self.__isLightTheme(self.settings.theme)
        self.playlists: Playlists = Playlists()

        self.library: Library = Library(Library.Info(), Library.Songs())
        self.currentPlaylist: Playlist = self.library

    def setTheme(self, theme: ThemeMode) -> None:
        self.settings.setTheme(theme)

        self.isLightMode = self.__isLightTheme(theme)
        self.themeChanged.emit(self.isLightMode)

    def setActivePlaylist(self, playlist: Playlist) -> None:
        self.currentPlaylist = playlist
        self.currentPlaylistChanged.emit(playlist)

    def setPlaylists(self, playlists: list[Playlist]) -> None:
        self.playlists.load(playlists)

    @staticmethod
    def __isLightTheme(theme: ThemeMode) -> bool:
        if theme == ThemeMode.LIGHT:
            return True
        if theme == ThemeMode.DARK:
            return False
        return Systems.isUsingLightMode()


appCenter = ApplicationCenter()
