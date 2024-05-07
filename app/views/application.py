from app.common.models import Playlist
from app.common.others import appCenter, database, musicPlayer
from app.views.windows import MainWindow


class Application:
    def __init__(self):
        self.__createUI()
        self.__configureDatabase()
        self.__configureMusicPlayer()
        self.__configureApplication()

    def __createUI(self):
        self._mainWindow = MainWindow()

    def __configureApplication(self):
        appCenter.exited.connect(lambda: musicPlayer.stop())
        appCenter.exited.connect(lambda: self._mainWindow.close())
        appCenter.setLightMode(True)

    @staticmethod
    def __configureDatabase():
        librarySongs = database.songs.load("library", withExtension="mp3")
        playlists = database.playlists.load(librarySongs)

        appCenter.library.getSongs().setSongs(librarySongs)
        appCenter.setPlaylists(playlists)

    def __configureMusicPlayer(self):
        settings = appCenter.settings

        musicPlayer.songChanged.connect(lambda song: settings.setPlayingSongId(song.getId()))
        musicPlayer.loopChanged.connect(lambda loop: settings.setIsLooping(loop))
        musicPlayer.shuffleChanged.connect(lambda shuffle: settings.setIsShuffle(shuffle))

        library = appCenter.library.getSongs()

        musicPlayer.loadPlaylist(library)
        musicPlayer.setLooping(settings.isLooping)
        musicPlayer.setShuffle(settings.isShuffle)
        musicPlayer.setCurrentSongIndex(self.__getLastPlayingSongIndex(library))
        musicPlayer.loadSongToPlay()

    @staticmethod
    def __getLastPlayingSongIndex(library: Playlist.Songs) -> int:
        try:
            return 0 if appCenter.settings.playingSongId is None else max(0, library.getSongIndexWithId(appCenter.settings.playingSongId))
        except:
            return 0

    def run(self) -> 'Application':
        self._mainWindow.show()
        return self

    def receiveMessage(self, msg: str) -> None:
        self._mainWindow.receiveMessage(msg)
