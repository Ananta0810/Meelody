from sys import argv, exit, path
from time import perf_counter

from music_player import MusicPlayer
from playlist_carousel import PlaylistCarousel

path.append("./lib")
from constants.application import supportedLanguages
from modules.entities.playlist_info import PlaylistInfo
from modules.models.player import Player
from PyQt5.QtWidgets import QApplication
from utils.data.config_utils import getLanguagePackage, retrievePlayerData, retrieveSettingsData, updateSettingsData
from utils.helpers.playlist_song_utils import getPlaylistFromDir
from views.ui_application import ApplicationInterface


class Appication:
    def __init__(self):
        # =================UI=================
        self.ui = ApplicationInterface()

        # =================Controllers=================
        self.playlistCarousel = PlaylistCarousel(self.ui.playlist_carousel)
        self.musicPlayer = MusicPlayer(self.ui.music_player_inner)
        self.controllers = {
            "application": self,
            "playlistCarousel": self.playlistCarousel,
            "musicPlayer": self.musicPlayer,
        }

        settingsData: dict[str, str] = retrieveSettingsData()
        musicPlayerData: dict[str, str] = retrievePlayerData()

        playlists: list[PlaylistInfo] = [
            PlaylistInfo(0, "ABC", None),
            PlaylistInfo(1, "BCD", None),
            PlaylistInfo(2, "EFG", None),
            PlaylistInfo(3, "HIB", None),
        ]

        self.displaySettingsDataRetrievedFrom(settingsData)
        self.loadPlaylistFromDirForPlayer(settingsData.get("path"))
        self.loadPlaylists(playlists)
        self.musicPlayer.displayDataRetrievedFrom(musicPlayerData)

        self.ui.connectSignalsToControllers(self.controllers)

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
        self.ui.settings_panel_inner.changeCurrentFolder(folderDir)
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
        self.musicPlayer.setPlayer(player)

    def displaySettingsDataRetrievedFrom(self, settingsData: dict[str, str]) -> None:
        isDarkMode: bool = settingsData.get("darkMode")
        language: str = settingsData.get("language")
        languages: list[str] = [key for key in supportedLanguages.keys()]

        self.ui.settings_panel_inner.change_language_dropdown.setCurrentIndex(languages.index(language))
        self.ui.settings_panel_inner.current_folder.setText(settingsData.get("path"))
        self.ui.settings_panel_inner.switch_dark_mode_btn.setChecked(isDarkMode)
        self.ui.translate(getLanguagePackage(language))
        self.ui.switchDarkMode(isDarkMode)


def main():
    start = perf_counter()
    app = QApplication(argv)
    application = Appication()
    application.run()
    end = perf_counter()
    print(f"Time to start application: {end - start}")
    exit(app.exec_())


if __name__ == "__main__":
    main()
