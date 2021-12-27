from sys import path

from .music_player import MusicPlayer
from .playlist_carousel import PlaylistCarousel
from .playlist_chooser import PlaylistSelector
from .playlist_menu import PlaylistMenu

path.append("./lib")
from constants.application import supportedLanguages
from modules.entities.playlist_info import PlaylistInfo
from modules.models.player import Player
from utils.data.config_utils import getLanguagePackage, retrievePlayerData, retrieveSettingsData, updateSettingsData
from utils.helpers.playlist_song_utils import getPlaylistFromDir
from views.ui_application import ApplicationInterface


class Appication:
    def __init__(self):
        self.ui = ApplicationInterface()
        self.setupControllers()
        self.setupData()

    def setupData(self):
        # =================Settings=================
        settingsData: dict[str, str] = retrieveSettingsData()
        self.displaySettingsDataRetrievedFrom(settingsData)
        # =================Music Player=================
        playlists: list[PlaylistInfo] = [
            PlaylistInfo(0, "ABC", None),
            PlaylistInfo(1, "BCD", None),
            PlaylistInfo(2, "EFG", None),
            PlaylistInfo(3, "HIB", None),
        ]
        self.loadPlaylists(playlists)
        musicPlayerData: dict[str, str] = retrievePlayerData()
        self.musicPlayer.displayDataRetrievedFrom(musicPlayerData)

    def setupControllers(self):
        self.playlistCarousel = PlaylistCarousel(self.ui.playlist_carousel)
        self.musicPlayer = MusicPlayer(self.ui.music_player_inner)
        self.playlistSelector = PlaylistSelector(self.ui)
        self.playlistMenu = PlaylistMenu(self.ui.currentPlaylist.songs.body)
        self.controllers = {
            "application": self,
            "playlistCarousel": self.playlistCarousel,
            "musicPlayer": self.musicPlayer,
            "playlistSelector": self.playlistSelector,
            "playlistMenu": self.playlistMenu,
        }
        self.ui.connectToControllers(self.controllers)
        self.playlistMenu.setControllers(self.controllers)

    def run(self):
        self.ui.MainWindow.show()

    def handleChangedLanguage(self, index: int) -> None:
        supportedLanguagesAsList = [key for key in supportedLanguages.keys()]
        language = supportedLanguagesAsList[index]
        languagePackage = getLanguagePackage(language)
        self.ui.translate(languagePackage)
        updateSettingsData("language", language)

    def handleChangedDarkMode(self) -> None:
        self.ui.switchDarkMode(not self.ui.isDarkMode)
        updateSettingsData("darkMode", self.ui.isDarkMode)

    def handleChangedFolder(self, folderDir: str) -> None:
        if len(folderDir) == 0:
            return
        self.ui.settings_panel.changeCurrentFolder(folderDir)
        updateSettingsData("path", folderDir)
        self.loadPlaylistFromDirForPlayer(folderDir)
        self.musicPlayer.player.setCurrentSongIndex(0)
        self.musicPlayer.player.loadSongToPlay()
        self.musicPlayer.displayCurrentSongInfo()

    def loadPlaylists(self, playlists: list[PlaylistInfo]):
        self.playlistCarousel.setPlaylists(playlists)
        self.playlistCarousel.addPlaylistsToUi()

    def loadPlaylistFromDirForPlayer(self, dir: str) -> None:
        self.musicPlayer.stopPlayingMusic()
        player = Player()
        library = getPlaylistFromDir(dir, withExtension=".mp3")
        player.loadPlaylist(library)
        self.playlistMenu.setPlaylist(library)
        self.playlistMenu.updateUi(self.ui.isDarkMode)
        self.musicPlayer.setPlayer(player)

    def displaySettingsDataRetrievedFrom(self, settingsData: dict[str, str]) -> None:
        isDarkMode: bool = settingsData.get("darkMode")
        language: str = settingsData.get("language")
        languages: list[str] = [key for key in supportedLanguages.keys()]

        self.ui.settings_panel.change_language_dropdown.setCurrentIndex(languages.index(language))
        self.ui.settings_panel.current_folder.setText(settingsData.get("path"))
        self.ui.settings_panel.switch_dark_mode_btn.setChecked(isDarkMode)
        self.ui.translate(getLanguagePackage(language))
        self.ui.switchDarkMode(isDarkMode)
        self.loadPlaylistFromDirForPlayer(settingsData.get("path"))
