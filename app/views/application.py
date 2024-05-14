from app.common.others import appCenter, database, musicPlayer, translator
from app.views.windows.main_window import MainWindow


class Application:
    def __init__(self):
        self.__createUI()
        self.__configureInternational()
        self.__configureDatabase()
        self.__configureMusicPlayer()
        self.__configureApplication()

    def __createUI(self):
        self._mainWindow = MainWindow()

    def __configureApplication(self) -> None:
        appCenter.exited.connect(lambda: musicPlayer.stop())
        appCenter.exited.connect(lambda: self._mainWindow.close())
        appCenter.setTheme(appCenter.settings.theme)

    @staticmethod
    def __configureInternational() -> None:
        translator.setLanguage(appCenter.settings.language)

    @staticmethod
    def __configureDatabase() -> None:
        playlists = database.playlists.load(appCenter.library.getSongs().toList())

        appCenter.setPlaylists(playlists)
        appCenter.setActivePlaylist(appCenter.library)

    @staticmethod
    def __configureMusicPlayer() -> None:
        settings = appCenter.settings

        musicPlayer.songChanged.connect(lambda song: settings.setPlayingSongId(song.getId()))
        musicPlayer.loopChanged.connect(lambda loop: settings.setIsLooping(loop))
        musicPlayer.shuffleChanged.connect(lambda shuffle: settings.setIsShuffle(shuffle))
        musicPlayer.volumeChanged.connect(lambda shuffle: settings.setVolume(shuffle))

        musicPlayer.loadPlaylist(appCenter.library.getSongs())
        musicPlayer.setLooping(settings.isLooping)
        musicPlayer.setShuffle(settings.isShuffle)
        musicPlayer.setVolume(settings.volume)
        musicPlayer.setCurrentSongIndex(appCenter.library.getSongs().getSongIndexWithId(appCenter.settings.playingSongId))
        musicPlayer.loadSongToPlay()

    def run(self) -> 'Application':
        self._mainWindow.show()
        return self

    def receiveMessage(self, msg: str) -> None:
        self._mainWindow.receiveMessage(msg)
