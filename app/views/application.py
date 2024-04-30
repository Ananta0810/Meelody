from app.common.models import Playlist
from app.common.others import appCenter, database, musicPlayer
from app.views.windows import MainWindow


class Application:
    def __init__(self):
        self.__createUI()
        self.__configureDatabase()
        self.__configureApplication()

    def __createUI(self):
        self._mainWindow = MainWindow()

    def __configureApplication(self):
        appCenter.exited.connect(lambda: musicPlayer.stop())
        appCenter.exited.connect(lambda: self._mainWindow.close())
        appCenter.setLightMode(True)

    @staticmethod
    def __configureDatabase():
        library = Playlist(Playlist.Info("Library"), Playlist.Songs(database.songs.load("library", withExtension="mp3")))
        playlists = database.playlists.load(library.getSongs().getSongs())

        appCenter.setPlaylists(playlists)
        appCenter.setLibrary(library)
        appCenter.setActivePlaylist(library)

        musicPlayer.loadPlaylist(library.getSongs())
        musicPlayer.setCurrentSongIndex(0)
        musicPlayer.loadSongToPlay()

        appCenter.playlists.changed.connect(lambda _: database.playlists.save(appCenter.playlists.validItems()))

    def run(self) -> 'Application':
        self._mainWindow.show()
        return self

    def receiveMessage(self, msg: str) -> None:
        self._mainWindow.receiveMessage(msg)
