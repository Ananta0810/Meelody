from app.common.models import Playlist
from app.common.others import appCenter, database, musicPlayer
from app.resource.qt import Icons, Cursors
from app.views.windows import MainWindow


class Application:
    def __init__(self):
        self.__createUI()
        self.__configureApplication()
        self.__configureDatabase()

    def __createUI(self):
        Icons.init()
        Cursors.init()
        self._mainWindow = MainWindow()

    def __configureApplication(self):
        appCenter.exited.connect(lambda: musicPlayer.stop())
        appCenter.exited.connect(lambda: self._mainWindow.close())

    def __configureDatabase(self):
        songs = Playlist.Songs(database.Songs.load("library", withExtension="mp3"))
        library = Playlist(Playlist.Info("Library"), songs)

        musicPlayer.loadPlaylist(library.getSongs())
        musicPlayer.setCurrentSongIndex(0)
        musicPlayer.loadSongToPlay()

        appCenter.setActivePlaylist(library)
        appCenter.setPlaylists(
            [
                Playlist(Playlist.Info("Summer"), songs),
                Playlist(Playlist.Info("Chill"), songs),
                Playlist(Playlist.Info("Morning"), songs),
            ]
        )

        appCenter.setLightMode(False)

    def run(self) -> 'Application':
        self._mainWindow.show()
        return self

    def receiveMessage(self, msg: str) -> None:
        self._mainWindow.receiveMessage(msg)
