from sys import path

path.append("./lib")
from threading import Thread
from time import sleep

from modules.models.player import Player
from utils.data.config_utils import updatePlayerData
from views.music_player.music_player import UIPlayerMusic


class MusicPlayer:
    def __init__(self, ui: UIPlayerMusic):
        self.ui = ui
        self.player: Player = None
        self.currentThreadNumber: int = 0

    def setPlayer(self, player: Player) -> None:
        self.player = player

    def displayDataRetrievedFrom(self, data: dict) -> None:
        self.player.setCurrentSong(data.get("currentSong"))
        self.ui.setLoopState(data.get("isLooping"))
        self.ui.setShuffleState(data.get("isShuffling"))
        self.ui.setVolume(data.get("volume"))
        # self.handleClickedShuffle()
        self.__prepareBeforePlaying()

    def handlePlaySongAtIndex(self, index: int) -> None:
        if not self.player.hasSong():
            return
        self.player.stop()
        self.player.setCurrentSongIndex(index)
        self.__playSong()

    def handlePlaySongAtCertainTime(self, time: float) -> None:
        if not self.player.hasSong():
            return
        currentSong = self.player.getCurrentSong()
        if currentSong is None:
            return
        self.player.skipToTime(time)
        self.__threadStartPlayer()

    def handlePlayCurrrentSong(self) -> None:
        needToPause = not self.ui.isPlaying()
        if needToPause:
            self.pauseMusic()
            return
        self.__playSong()

    def handlePlayNextSong(self) -> None:
        if not self.player.hasSong():
            return
        self.player.stop()
        self.player.next()
        self.__playSong()

    def handlePlayPreviousSong(self) -> None:
        if not self.player.hasSong():
            return
        self.player.stop()
        self.player.previous()
        self.__playSong()

    def handleEnteredTimer(self) -> None:
        SECONDS_PER_MINUTE = 60
        timeToActiveTimerInMinute: int = self.ui.getTimerValue()
        timeToActiveTimerInSeconds: int = timeToActiveTimerInMinute * SECONDS_PER_MINUTE
        self.player.timer.setTime(timeToActiveTimerInSeconds)
        self.ui.closeTimerBox()

    def handleClickedLoop(self) -> None:
        isLooping = self.ui.isLooping()
        updatePlayerData("isLooping", isLooping)

    def handleClickedShuffle(self) -> None:
        needToShuffle = self.ui.isShuffling()
        updatePlayerData("isShuffling", needToShuffle)
        if not needToShuffle:
            self.player.unshuffle()
            return
        self.player.shuffle()

    def handleClickedLoveSong(self) -> None:
        if not self.player.hasSong():
            return
        self.player.getCurrentSong().reverseLoveState()

    def handleChangVolume(self) -> None:
        volume: int = self.ui.getCurrentVolumeValue()
        self.player.setVolume(volume)
        updatePlayerData("volume", volume)

    def pauseMusic(self) -> None:
        if self.player is None:
            return
        self.player.pause()
        self.ui.setPlayingState(False)

    def stopPlayingMusic(self) -> None:
        if self.player is None:
            return
        self.player.stop()
        self.ui.setPlayingState(False)

    def __displayCurrentSongInfo(self) -> None:
        if self.player is None:
            return

        song = None
        if self.player.hasSong():
            song = self.player.getCurrentSong()
        if song is None:
            self.ui.displaySongInfo()
            self.ui.setPlayingTime(0)
            self.ui.setTotalTime(0)
            return

        self.ui.displaySongInfo(song.cover, song.title, song.artist, song.loved)
        self.ui.setTotalTime(song.length)
        self.ui.setPlayingTime(self.player.getPlayingTime())

    def __startPlayer(self) -> None:
        if self.player is None:
            return
        self.ui.setPlayingState(True)

        threadNumber: int = self.currentThreadNumber
        interval: float = self.__getIntervalUpdateToUi()
        self.player.timer.setInterval(interval)
        self.player.play()
        while threadNumber == self.currentThreadNumber and self.player.isPlaying():
            self.__doWhilePlayingMusic()
            sleep(interval)

        playingThisSong: bool = threadNumber == self.currentThreadNumber
        songIsFinished: bool = playingThisSong and self.ui.isPlaying()
        if songIsFinished:
            self.__doAfterSongFinished()

    def __prepareBeforePlaying(self):
        self.player.loadSongToPlay()
        self.ui.setTotalTime(self.player.getCurrentSong().length)
        self.__displayCurrentSongInfo()
        updatePlayerData("currentSong", self.player.getCurrentSong().title)

    def __playSong(self) -> None:
        if self.player.getCurrentSong() is None:
            return
        self.__prepareBeforePlaying()
        self.__threadStartPlayer()

    def __threadStartPlayer(self) -> None:
        self.currentThreadNumber += 1
        Thread(target=self.__startPlayer).start()

    def __getIntervalUpdateToUi(self) -> float:
        TIMES_THAT_UI_HAS_TO_UPDATE_FOR_SLIDER_WHILE_PLAYING: int = 100
        LONGEST_TIME_BREAK_FOR_A_UI_UPDATE_IN_SECONDS: float = 0.25

        interval: float = self.player.getCurrentSong().length / TIMES_THAT_UI_HAS_TO_UPDATE_FOR_SLIDER_WHILE_PLAYING
        if interval > LONGEST_TIME_BREAK_FOR_A_UI_UPDATE_IN_SECONDS:
            interval = LONGEST_TIME_BREAK_FOR_A_UI_UPDATE_IN_SECONDS
        return interval

    def __doWhilePlayingMusic(self) -> None:
        self.__realTimeUiUpdate()
        if self.player.timer.isEnabled():
            self.__runTimer()

    def __doAfterSongFinished(self) -> None:
        self.player.resetTime()
        if self.ui.isLooping():
            self.__threadStartPlayer()
            return
        self.handlePlayNextSong()

    def __realTimeUiUpdate(self):
        self.ui.setPlayingTime(self.player.getPlayingTime())

    def __runTimer(self) -> None:
        if self.player is None:
            return
        timer = self.player.timer
        timer.count()
        if not timer.isActive():
            return
        timer.reset()
        self.pauseMusic()
