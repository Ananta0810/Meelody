from app.common.models import Playlist
from app.common.others import appCenter, database, musicPlayer
from app.resource.qt import Icons, Cursors
from app.views.windows import MainWindow


class Application:
    def __init__(self):
        self.__createUI()
        self.__configureDatabase()

    def __createUI(self):
        Icons.init()
        Cursors.init()
        self.window = MainWindow()

    def __configureDatabase(self):
        playlist = Playlist(Playlist.Info("Library"), Playlist.Songs(database.Songs.load("library", withExtension="mp3")))

        musicPlayer.loadPlaylist(playlist.getSongs())
        musicPlayer.setCurrentSongIndex(0)
        musicPlayer.loadSongToPlay()

        appCenter.setActivePlaylist(playlist)
        appCenter.setLightMode(True)

    def run(self) -> 'Application':
        self.window.show()
        return self

    def receiveMessage(self, msg: str) -> None:
        self.window.receiveMessage(msg)
