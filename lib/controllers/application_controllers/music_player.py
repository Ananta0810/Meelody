from ..self_controllers.music_player_controller import MusicPlayer
from ..self_controllers.playlist_menu import PlaylistMenu


class MusicPlayerController:
    def __init__(self) -> None:
        pass

    def setMainController(self, controller: MusicPlayer):
        self.player = controller
        self.player.ui.connectToController(self)

    def setSecondController(self, controller: PlaylistMenu):
        self.menu = controller

    def handlePlaySongAtIndex(self, index: int) -> None:
        self.handlePlaySongAtIndex(index)
        self.menu.ui.selectItem(index)

    def handlePlaySongAtCertainTime(self, time: float) -> None:
        self.player.handlePlaySongAtCertainTime(time)

    def handlePlayCurrrentSong(self) -> None:
        self.player.handlePlayCurrrentSong()
        self.menu.ui.selectItem(self.player.player.getCurrentSongIndex())

    def handlePlayNextSong(self) -> None:
        self.player.handlePlayNextSong()
        self.menu.ui.selectItem(self.player.player.getCurrentSongIndex())

    def handlePlayPreviousSong(self) -> None:
        self.player.handlePlayPreviousSong()
        self.menu.ui.selectItem(self.player.player.getCurrentSongIndex())

    def handleEnteredTimer(self) -> None:
        self.player.handleEnteredTimer()

    def handleClickedLoop(self) -> None:
        self.player.handleClickedLoop()

    def handleClickedShuffle(self) -> None:
        self.player.handleClickedShuffle()

    def handleClickedLoveSong(self) -> None:
        self.player.handleClickedLoveSong()
        player = self.player.player
        self.menu.ui.setSongLoveStateAtIndex(player.getCurrentSongIndex(), player.getCurrentSong().loved)

    def handleChangVolume(self) -> None:
        self.player.handleChangVolume()
