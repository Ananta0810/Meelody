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

    def __configureDatabase(self):
        library = Playlist(Playlist.Info(id="library", name="Library"), Playlist.Songs(database.songs.load("library", withExtension="mp3")))
        playlists = database.playlists.load(library.getSongs().getSongs())

        appCenter.setPlaylists(playlists)
        appCenter.setLibrary(library)
        appCenter.setActivePlaylist(library)

        musicPlayer.loadPlaylist(library.getSongs())
        musicPlayer.songChanged.connect(lambda song: appCenter.settings.setPlayingSongId(song.getId()))
        musicPlayer.loopChanged.connect(lambda loop: appCenter.settings.setIsLooping(loop))
        musicPlayer.shuffleChanged.connect(lambda shuffle: appCenter.settings.setIsShuffle(shuffle))

        self.__setPlayingSong(library)

    @staticmethod
    def __setPlayingSong(library: Playlist) -> None:
        if appCenter.settings.playingSongId is not None:
            lastPlayingSongIndex = library.getSongs().getSongIndexWithId(appCenter.settings.playingSongId)
            if lastPlayingSongIndex >= 0:
                musicPlayer.setCurrentSongIndex(lastPlayingSongIndex)
                musicPlayer.loadSongToPlay()
                return

        musicPlayer.setCurrentSongIndex(0)
        musicPlayer.loadSongToPlay()

    def run(self) -> 'Application':
        self._mainWindow.show()
        return self

    def receiveMessage(self, msg: str) -> None:
        self._mainWindow.receiveMessage(msg)
