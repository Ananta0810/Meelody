from sys import path

path.append("./lib")
from threading import Thread
from time import sleep

from modules.models.player import Player
from utils.data.config_utils import updatePlayerData


class MusicPlayer:
    def __init__(self, ui, player: Player):
        self.ui = ui
        self.player = player
        self.currentThreadNumber: int = 0
        self.canRunTimeSlider: bool = True

    def displayDataRetrievedFrom(self, data: dict) -> None:
        self.player.setCurrentSong(data.get("currentSong"))
        self.player.loadSongToPlay()
        self.displayCurrentSongInfo()
        self.ui.setLoopState(data.get("isLooping"))
        self.ui.setShuffleState(data.get("isShuffling"))
        self.ui.setVolume(data.get("volume"))

    def handleEnteredTimer(self):
        SECONDS_PER_MINUTE = 60
        timeToActiveTimerInMinute: int = self.ui.getTimerValue()
        timeToActiveTimerInSeconds: int = (
            timeToActiveTimerInMinute * SECONDS_PER_MINUTE
        )
        self.player.timer.setTime(timeToActiveTimerInSeconds)
        self.ui.closeTimerBox()

    def handleClickedLoop(self):
        isLooping = self.ui.isLooping()
        updatePlayerData("isLooping", isLooping)

    def handleClickedShuffle(self):
        isShuffling = self.ui.isShuffling()
        updatePlayerData("isShuffling", isShuffling)
        if isShuffling:
            self.player.shuffle()
        else:
            self.player.unshuffle()

    def handlePausedTimeSlider(self):
        self.canRunTimeSlider = False

    def handleUnpausedTimeSlider(self):
        self.canRunTimeSlider = True
        if not self.player.hasSong():
            return
        timeStart: float = (
            self.ui.getCurrentTimeSliderPosition()
            / 100
            * self.player.getCurrentSong().length
        )
        self.player.stop()
        self.player.setTimeStart(timeStart)
        self.ui.displayPlayingTime(timeStart)
        self.handlePlaySong()

    def handleChangVolume(self):
        volume: int = self.ui.getCurrentVolumeValue()
        self.player.setVolume(volume)
        updatePlayerData("volume", volume)

    def handlePlaySong(self):
        if self.player.getCurrentSong() is None:
            return
        if not self.ui.isPlaying():
            self.pauseMusic()
            return
        self.player.loadSongToPlay()
        updatePlayerData("currentSong", self.player.getCurrentSong().title)
        self.__threadPlaySong()

    def handleLoveSong(self):
        if not self.player.hasSong():
            return
        self.player.getCurrentSong().reverseLoveState()

    def handleNextSong(self):
        if not self.player.hasSong():
            return
        self.player.next()
        self.player.loadSongToPlay()
        self.displayCurrentSongInfo()
        updatePlayerData("currentSong", self.player.getCurrentSong().title)
        self.__threadPlaySong()

    def handlePreviousSong(self):
        if not self.player.hasSong():
            return
        self.player.previous()
        self.player.loadSongToPlay()
        self.displayCurrentSongInfo()
        updatePlayerData("currentSong", self.player.getCurrentSong().title)
        self.__threadPlaySong()

    def displayCurrentSongInfo(self):
        if self.player is None:
            return
        cover = None
        title = None
        artist = ""
        length = 0
        song = None
        if self.player.hasSong():
            song = self.player.getCurrentSong()
        if song is not None:
            cover = song.cover
            title = song.title
            artist = song.artist
            length = song.length
        self.ui.displaySongInfo(cover, title, artist)
        self.ui.displayPlayingTime(0)
        self.ui.displayTotalTime(length)

    def pauseMusic(self):
        self.player.pause()
        self.ui.setPlayingState(False)

    def playMusic(self):
        self.ui.setPlayingState(True)
        player = self.player
        player.play()

        threadNumber: int = self.currentThreadNumber
        TIMES_THAT_UI_HAS_TO_UPDATE_FOR_SLIDER_WHILE_PLAYING: int = 100
        LONGEST_TIME_BREAK_FOR_A_UI_UPDATE_IN_SECONDS: float = 0.25

        interval: float = (
            player.getCurrentSong().length
            / TIMES_THAT_UI_HAS_TO_UPDATE_FOR_SLIDER_WHILE_PLAYING
        )
        if interval > LONGEST_TIME_BREAK_FOR_A_UI_UPDATE_IN_SECONDS:
            interval = LONGEST_TIME_BREAK_FOR_A_UI_UPDATE_IN_SECONDS
        player.timer.setInterval(interval)

        while threadNumber == self.currentThreadNumber and player.isPlaying():
            self.__doWhilePlayingMusic(player)
            sleep(interval)

        playingThisSong: bool = threadNumber == self.currentThreadNumber
        songIsFinished: bool = self.ui.isPlaying() and playingThisSong

        if songIsFinished:
            self.__doAfterSongFinished()

    def __threadPlaySong(self):
        thread: Thread = Thread(target=self.playMusic)
        self.currentThreadNumber += 1
        thread.start()

    def __doWhilePlayingMusic(self, player: Player):
        playingTime = player.getPlayingTime()
        self.ui.displayPlayingTime(playingTime)

        if self.canRunTimeSlider:
            self.ui.runTimeSlider(playingTime, player.getCurrentSong().length)
        if player.timer.isEnabled():
            self.__runTimer()

    def __doAfterSongFinished(self):
        self.player.resetTime()
        self.ui.setPlayingState(False)
        if self.ui.isLooping():
            self.__threadPlaySong()
        else:
            self.handleNextSong()

    def __runTimer(self):
        timer = self.player.timer
        timer.count()
        if not timer.isActive():
            return
        timer.reset()
        self.pauseMusic()


# def main():
#     start = perf_counter()
#     app = QApplication(argv)
#     form = QWidget()
#     form.setGeometry(276, 490, 1368, 100)
#     form.setStyleSheet("background: white")
#     player = Player()
#     library = getPlaylistFromDir("Library", withExtension=".mp3")
#     player.loadPlaylist(library)
#     player.loadSongToPlay()
#     form.setStyleSheet("background: black")
#     appController = MusicPlayer(form, player)
#     appController.ui.setFixedSize(1368, 100)
#     appController.ui.darkMode()
#     form.show()

#     end = perf_counter()
#     print(f"Time to start application: {end - start}")
#     exit(app.exec_())


# if __name__ == "__main__":
#     main()
