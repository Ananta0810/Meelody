from sys import argv, exit, path
from time import perf_counter

from music_player import MusicPlayer

path.append("./lib")
from constants.application import supportedLanguages
from modules.models.player import Player
from PyQt5.QtWidgets import QApplication
from utils.data.config_utils import getLanguagePack, getLanguagePackFromConfig
from utils.helpers.playlist_song_utils import getPlaylistFromDir
from views.ui_application import ApplicationInterface
from widgets.framless_window import FramelessWindow


class Appication:
    def __init__(self):
        start = perf_counter()
        app = QApplication(argv)
        MainWindow = FramelessWindow()

        # =================Main Part=================

        self.ui = ApplicationInterface()
        self.ui.setupUi(MainWindow)
        self.ui.lightMode()
        self.ui.translate(getLanguagePackFromConfig())

        # =================Controllers=================
        player = Player()
        library = getPlaylistFromDir("Library", withExtension=".mp3")
        player.loadPlaylist(library)
        player.loadSongToPlay()
        self.musicPlayerController = MusicPlayer(player, self.ui.player)

        controllers = {
            "application": self,
            "music_player": self.musicPlayerController,
        }
        self.ui.connectSignals(controllers)
        # =================Show Ui=================
        MainWindow.show()
        end = perf_counter()
        print(f"Time to start application: {end - start}")
        exit(app.exec_())

    def handleChangedLanguage(self, index: int):
        language = getLanguagePack(supportedLanguages[index])
        self.ui.translate(language)


def main():
    Appication()


if __name__ == "__main__":
    main()
