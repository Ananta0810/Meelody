from app.common.models import Playlist
from app.common.others import appCenter, database, musicPlayer
from app.views.windows import MainWindow


class Application:
    def __init__(self):
        self.__createUI()
        self.__configureApplication()
        self.__configureDatabase()

    def __createUI(self):
        self._mainWindow = MainWindow()

    def __configureApplication(self):
        appCenter.exited.connect(lambda: musicPlayer.stop())
        appCenter.exited.connect(lambda: self._mainWindow.close())

    @staticmethod
    def __configureDatabase():
        library = Playlist(Playlist.Info("Library"), Playlist.Songs(database.Songs.load("library", withExtension="mp3")))

        appCenter.setLibrary(library)
        appCenter.setActivePlaylist(library)
        appCenter.setPlaylists(
            [
                Playlist(Playlist.Info("Summer"), library.getSongs()),
                Playlist(Playlist.Info("Chill"), library.getSongs()),
                Playlist(Playlist.Info("Morning"), library.getSongs()),
            ]
        )

        musicPlayer.loadPlaylist(library.getSongs())
        musicPlayer.setCurrentSongIndex(0)
        musicPlayer.loadSongToPlay()

        appCenter.setLightMode(True)

    def run(self) -> 'Application':
        self._mainWindow.show()
        return self

    def receiveMessage(self, msg: str) -> None:
        self._mainWindow.receiveMessage(msg)
