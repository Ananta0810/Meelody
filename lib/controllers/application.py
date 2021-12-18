from sys import argv, exit, path
from time import perf_counter

from music_player import MusicPlayer

path.append("./lib")
from constants.application import supportedLanguages
from modules.models.player import Player
from PyQt5.QtWidgets import QApplication
from utils.data.config_utils import (
    getLanguagePackage,
    retrievePlayerData,
    retrieveSettingsData,
    updateSettingsData,
)
from utils.helpers.playlist_song_utils import getPlaylistFromDir
from views.ui_application import ApplicationInterface


class Appication:
    def __init__(self):
        # =================UI=================
        self.ui = ApplicationInterface()

        # =================Controllers=================
        self.musicPlayer = MusicPlayer(self.ui.music_player_inner)

        settingsData = retrieveSettingsData()
        musicPlayerData = retrievePlayerData()

        self.ui.displayDataRetrievedFrom(settingsData)
        self.loadPlaylistFromDirForPlayer(settingsData.get("path"))
        self.musicPlayer.displayDataRetrievedFrom(musicPlayerData)

        controllers = {
            "application": self,
            "musicPlayer": self.musicPlayer,
        }
        self.ui.connectSignalsToControllers(controllers)

    def run(self):
        self.ui.show()

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

    def loadPlaylistFromDirForPlayer(self, dir: str) -> None:
        self.musicPlayer.stopPlayingMusic()

        player = Player()
        self.musicPlayer.setPlayer(player)
        library = getPlaylistFromDir(dir, withExtension=".mp3")
        player.loadPlaylist(library)
        player.loadSongToPlay()
        self.musicPlayer.displayCurrentSongInfo()


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
