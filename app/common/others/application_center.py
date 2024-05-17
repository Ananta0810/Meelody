from PyQt5.QtCore import QObject, pyqtSignal, pyqtBoundSignal

from app.common.models import Playlist
from app.common.models.database import Library, Playlists, Settings
from app.common.others.translator import Translator
from app.common.statics.enums import ThemeMode
from app.utils.systems import Systems


class ApplicationCenter(QObject):
    themeChanged: pyqtBoundSignal = pyqtSignal(bool)
    currentPlaylistChanged: pyqtBoundSignal = pyqtSignal(Playlist)
    exited: pyqtBoundSignal = pyqtSignal()
    loaded: pyqtBoundSignal = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.settings: Settings = Settings()
        self.translator: Translator = Translator()
        self.translator.setLanguage(self.settings.language)

        self.isLoaded: bool = False
        self.isLightMode: bool = self.__isLightTheme(self.settings.theme)

        self.library: Library = Library()
        self.playlists: Playlists = Playlists(self.library.getSongs().toList())
        self.currentPlaylist: Playlist = self.library

        self.loaded.connect(lambda: self.__loaded())

    def __loaded(self) -> None:
        self.isLoaded = True

    def setTheme(self, theme: ThemeMode) -> None:
        self.settings.setTheme(theme)

        self.isLightMode = self.__isLightTheme(theme)
        self.themeChanged.emit(self.isLightMode)

    def setActivePlaylist(self, playlist: Playlist) -> None:
        self.currentPlaylist = playlist
        self.currentPlaylistChanged.emit(playlist)

    @staticmethod
    def __isLightTheme(theme: ThemeMode) -> bool:
        if theme == ThemeMode.LIGHT:
            return True
        if theme == ThemeMode.DARK:
            return False
        return Systems.isUsingLightMode()


appCenter = ApplicationCenter()
