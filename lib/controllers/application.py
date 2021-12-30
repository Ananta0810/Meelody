from os import getcwd
from sys import path

path.append(getcwd() + "/lib")
from constants.application import supportedLanguages
from modules.entities.playlist_info import PlaylistInfo
from modules.models.player import Player
from utils.data.config_utils import getLanguagePackage, retrievePlayerData, retrieveSettingsData, updateSettingsData
from utils.helpers.playlist_song_utils import getPlaylistFromDir
from views.application_interface import ApplicationInterface

from .application_controllers.music_player import MusicPlayerController
from .application_controllers.playlist_carousel import PlaylistCarouselController
from .application_controllers.playlist_menu import PlaylistMenuController
from .self_controllers.music_player_controller import MusicPlayer
from .self_controllers.playlist_carousel import PlaylistCarousel
from .self_controllers.playlist_menu import PlaylistMenu


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
            # PlaylistInfo(0, "ABC", None),
            # PlaylistInfo(1, "BCD", None),
            # PlaylistInfo(2, "EFG", None),
            # PlaylistInfo(3, "HIB", None),
        ]
        self.loadPlaylists(playlists)
        musicPlayerData: dict[str, str] = retrievePlayerData()
        self.player.player.displayDataRetrievedFrom(musicPlayerData)

    def setupControllers(self):
        playlistCarousel = PlaylistCarousel(self.ui.body.playlistCarousel)
        musicPlayer = MusicPlayer(self.ui.musicPlayer)
        playlistMenu = PlaylistMenu(self.ui.body.currentPlaylist)

        self.player = MusicPlayerController()
        self.player.setMainController(musicPlayer)
        self.player.setSecondController(playlistMenu)

        self.menu = PlaylistMenuController()
        self.menu.setMainController(playlistMenu)
        self.menu.setSecondController(musicPlayer)

        self.playlistCarousel = PlaylistCarouselController()
        self.playlistCarousel.setMainController(playlistCarousel)
        self.playlistCarousel.setSecondController(self.menu)

    def run(self):
        self.ui.mainWindow.show()

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
        self.ui.menuBar.settingsPanel.changeCurrentFolder(folderDir)
        updateSettingsData("path", folderDir)
        self.loadPlaylistFromDirForPlayer(folderDir)
        self.player.player.player.setCurrentSongIndex(0)
        self.player.player.player.loadSongToPlay()
        self.player.player.displayCurrentSongInfo()

    def loadPlaylists(self, playlists: list[PlaylistInfo]):
        self.playlistCarousel.carousel.setPlaylists(playlists)
        self.playlistCarousel.addPlaylistsToUi()

    def loadPlaylistFromDirForPlayer(self, dir: str) -> None:
        self.player.player.stopPlayingMusic()
        player = Player()
        library = getPlaylistFromDir(dir, withExtension=".mp3")
        player.loadPlaylist(library)
        self.menu.menu.setPlaylist(library)
        self.menu.updateUi(self.ui.isDarkMode)
        self.player.player.setPlayer(player)

    def displaySettingsDataRetrievedFrom(self, settingsData: dict[str, str]) -> None:
        isDarkMode: bool = settingsData.get("darkMode")
        language: str = settingsData.get("language")
        languages: list[str] = [key for key in supportedLanguages.keys()]

        self.ui.menuBar.settingsPanel.changeLanguagueDropdown.setCurrentIndex(languages.index(language))
        self.ui.menuBar.settingsPanel.currentFolder.setText(settingsData.get("path"))
        self.ui.menuBar.settingsPanel.switchDarkModeBtn.setChecked(isDarkMode)
        self.ui.translate(getLanguagePackage(language))
        self.ui.switchDarkMode(isDarkMode)
        self.loadPlaylistFromDirForPlayer(settingsData.get("path"))
