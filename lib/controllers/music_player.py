from sys import path

path.append("./lib")
from threading import Thread
from time import sleep

from modules.models.player import Player
from utils.data.config_utils import updatePlayerData
from views.ui_player_music import UIPlayerMusic


class MusicPlayer:
    def __init__(self, ui: UIPlayerMusic):
        self.ui = ui
        self.player: Player = None
        self.currentThreadNumber: int = 0
        self.canRunTimeSlider: bool = True

    def setPlayer(self, player: Player) -> None:
        self.player = player

    def displayDataRetrievedFrom(self, data: dict) -> None:

        self.ui.setLoopState(data.get("isLooping"))
        self.ui.setShuffleState(data.get("isShuffling"))
        self.handleClickedShuffle()
        self.ui.setVolume(data.get("volume"))

        self.player.setCurrentSong(data.get("currentSong"))
        self.player.loadSongToPlay()
        self.displayCurrentSongInfo()

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
        isShuffling = self.ui.isShuffling()
        updatePlayerData("isShuffling", isShuffling)
        if isShuffling:
            self.player.shuffle()
        else:
            self.player.unshuffle()

    def handlePausedTimeSlider(self) -> None:
        self.canRunTimeSlider = False

    def handleUnpausedTimeSlider(self) -> None:
        self.canRunTimeSlider = True
        if not self.player.hasSong():
            return
        currentSong = self.player.getCurrentSong()
        if currentSong is None:
            return
        timeStart: float = self.ui.getCurrentTimeSliderPosition() / 100 * currentSong.length
        self.player.stop()
        self.player.setTimeStart(timeStart)
        self.ui.displayPlayingTime(timeStart)
        self.handlePlaySong()

    def handleChangVolume(self) -> None:
        volume: int = self.ui.getCurrentVolumeValue()
        self.player.setVolume(volume)
        updatePlayerData("volume", volume)

    def handlePlaySong(self) -> None:
        song = self.player.getCurrentSong()
        if song is None:
            return
        if not self.ui.isPlaying():
            self.pauseMusic()
            return
        self.player.loadSongToPlay()
        self.displayCurrentSongInfo()
        updatePlayerData("currentSong", song.title)
        self.__threadPlaySong()

    def handleLoveSong(self) -> None:
        if not self.player.hasSong():
            return
        self.player.getCurrentSong().reverseLoveState()

    def handleNextSong(self) -> None:
        if not self.player.hasSong():
            return
        self.player.next()
        self.playSong()

    def handlePreviousSong(self) -> None:
        if not self.player.hasSong():
            return
        self.player.previous()
        self.playSong()

    # !==========================Fix this later==========================
    def playSong(self) -> None:
        self.player.loadSongToPlay()
        self.displayCurrentSongInfo()
        updatePlayerData("currentSong", self.player.getCurrentSong().title)
        self.__threadPlaySong()

    def displayCurrentSongInfo(self) -> None:
        if self.player is None:
            return

        song = None
        if self.player.hasSong():
            song = self.player.getCurrentSong()

        if song is None:
            self.ui.displaySongInfo()
            self.ui.displayPlayingTime(0)
            self.ui.displayTotalTime(0)
            self.ui.runTimeSlider(0, 1)
            return

        self.ui.displaySongInfo(song.cover, song.title, song.artist, song.loved)
        self.ui.displayPlayingTime(0)
        self.ui.runTimeSlider(0, song.length)
        self.ui.displayTotalTime(song.length)

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

    def playMusic(self) -> None:
        player = self.player
        if player is None:
            return
        self.ui.setPlayingState(True)
        player.play()

        threadNumber: int = self.currentThreadNumber
        TIMES_THAT_UI_HAS_TO_UPDATE_FOR_SLIDER_WHILE_PLAYING: int = 100
        LONGEST_TIME_BREAK_FOR_A_UI_UPDATE_IN_SECONDS: float = 0.25

        interval: float = player.getCurrentSong().length / TIMES_THAT_UI_HAS_TO_UPDATE_FOR_SLIDER_WHILE_PLAYING
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

    def __threadPlaySong(self) -> None:
        thread: Thread = Thread(target=self.playMusic)
        self.currentThreadNumber += 1
        thread.start()

    def __doWhilePlayingMusic(self, player: Player) -> None:
        if player is None:
            return
        playingTime = player.getPlayingTime()
        self.ui.displayPlayingTime(playingTime)

        if self.canRunTimeSlider:
            self.ui.runTimeSlider(playingTime, player.getCurrentSong().length)
        if player.timer.isEnabled():
            self.__runTimer()

    def __doAfterSongFinished(self) -> None:
        if self.player is None:
            return
        self.player.resetTime()
        self.ui.setPlayingState(False)
        if self.ui.isLooping():
            self.__threadPlaySong()
        else:
            self.handleNextSong()

    def __runTimer(self) -> None:
        if self.player is None:
            return
        timer = self.player.timer
        timer.count()
        if not timer.isActive():
            return
        timer.reset()
        self.pauseMusic()
