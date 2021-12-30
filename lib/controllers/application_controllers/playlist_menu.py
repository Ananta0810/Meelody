from controllers.self_controllers.music_player_controller import MusicPlayer
from controllers.self_controllers.playlist_menu import PlaylistMenu


class PlaylistMenuController:
    def setMainController(self, controller: PlaylistMenu) -> None:
        self.menu = controller
        self.menu.ui.connectToController(self)

    def setSecondController(self, controller: MusicPlayer) -> None:
        self.player = controller

    def updateUi(self, isDarkMode: bool) -> None:
        self.updatePlaylistToScreen()
        if isDarkMode:
            self.menu.ui.darkMode()
        else:
            self.menu.ui.lightMode()

    def updatePlaylistToScreen(self):
        songs = self.menu.playlist.getSongs()
        self.menu.ui.updateLayout(len(songs), controller=self)
        for index, song in enumerate(songs):
            self.menu.ui.displaySongInfoAtIndex(index, song.cover, song.title, song.artist, song.length)

    def handleFindSongInsertIndexWithTitle(self, title: str) -> int:
        return self.menu.handleFindSongInsertIndexWithTitle(title)

    def handleChangedLoveStateOfSongAtIndex(self, index: int, state: bool) -> None:
        self.menu.handleChangedLoveStateOfSongAtIndex(index, state)
        if self.__isPlayingSongAtIndex(index):
            self.player.ui.setLoveState(state)

    def handlePlayedSongAtIndex(self, index: int) -> None:
        self.menu.handlePlayedSongAtIndex(index)
        self.player.handlePlaySongAtIndex(index)

    def handleAddSongToPlaylistAtIndex(self, index: int) -> None:
        self.menu.handleAddSongToPlaylistAtIndex(index)

    def handleEditSongAtIndex(self, index: int) -> None:
        self.menu.handleEditSongAtIndex(index)

    def handleDeleteSongAtIndex(self, index: int) -> None:
        if self.__isPlayingSongAtIndex(index):
            return
        self.menu.handleDeleteSongAtIndex(index)

    def handleChangedSongTitle(self, index: int, newTitle: str) -> None:
        if self.__isPlayingSongAtIndex(index):
            return
        self.menu.handleChangedSongTitle(index, newTitle)

    def handleChangedSongArtist(self, index: int, newArtist: str) -> None:
        if self.__isPlayingSongAtIndex(index):
            return
        self.menu.handleChangedSongArtist(index, newArtist)

    def handleChangedSongCover(self, index: int, coverPath: str) -> None:
        if self.__isPlayingSongAtIndex(index):
            return
        self.menu.handleChangedSongCover(index, coverPath)

    def __isPlayingSongAtIndex(self, index: int) -> bool:
        return self.player.player.getCurrentSongIndex() == index
