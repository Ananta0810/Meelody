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
        self.ui = ApplicationInterface()
        self.ui.setupUi()

        # =================Controllers=================
        player = Player()
        library = getPlaylistFromDir("Library", withExtension=".mp3")
        player.loadPlaylist(library)
        self.musicPlayer = MusicPlayer(self.ui.music_player_inner, player)

        settingsData = retrieveSettingsData()
        musicPlayerData = retrievePlayerData()

        self.ui.displayDataRetrievedFrom(settingsData)
        self.musicPlayer.displayDataRetrievedFrom(musicPlayerData)

        controllers = {
            "application": self,
            "musicPlayer": self.musicPlayer,
        }
        self.ui.connectSignalsToControllers(controllers)

    def run(self):
        self.ui.show()

    def handleChangedLanguage(self, index: int) -> None:
        language = supportedLanguages[index]
        languagePackage = getLanguagePackage(language)
        self.ui.translate(languagePackage)
        updateSettingsData("language", language)

    def handleChangedDarkMode(self) -> None:
        self.ui.switchDarkMode(not self.ui.isDarkMode)
        updateSettingsData("darkMode", self.ui.isDarkMode)

    def handleChangedFolder(self, folderDir: str) -> None:
        if len(folderDir) == 0:
            return
        self.ui.settings_window.changeCurrentFolder(folderDir)
        updateSettingsData("path", folderDir)


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
