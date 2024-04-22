import os

from PyQt5.QtCore import QObject, pyqtSignal

from .song import Song

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from pygame import mixer


class MusicPlayer(QObject):
    __currentSong: Song = None
    __currentSongIndex: int = 0
    __timeStartInSec: float = 0
    __loaded: bool = False
    __timeToStopAsSeconds: int | None = None
    __elapsedTimeAsSeconds: int = 0

    played = pyqtSignal()
    paused = pyqtSignal()

    def __init__(self):
        super().__init__()
        mixer.pre_init()
        mixer.init()

    def setStartTime(self, timeStart: float):
        self.__timeStartInSec = timeStart

    def getTimeStart(self):
        return self.__timeStartInSec

    def loadSongToPlay(self):
        if self.__loaded:
            return
        self.resetTime()
        self.__loaded = True
        mixer.music.unload()
        mixer.music.load(self.__currentSong.getLocation())

    def play(self):
        mixer.music.play(start=self.__getPlayingTime())
        self.played.emit()

    def setCurrentSongIndex(self, index: int) -> None:
        self.__currentSongIndex = index
        self.__loaded = False

    def setCurrentSong(self, song: Song) -> None:
        self.__currentSong = song

    def getCurrentSong(self) -> Song:
        return self.__currentSong

    def getCurrentSongIndex(self) -> int:
        return self.__currentSongIndex

    def skipToTime(self, time: float) -> None:
        self.pause()
        self.setStartTime(time)

    def pause(self) -> None:
        if not self.isPlaying():
            return
        self.setStartTime(self.__getPlayingTime())
        mixer.music.stop()
        self.paused.emit()

    def stop(self) -> None:
        if not self.isPlaying():
            return
        mixer.music.stop()
        mixer.music.unload()
        self.__loaded = False
        self.paused.emit()

    def resetTime(self) -> None:
        self.__timeStartInSec = 0

    def __getPlayingTime(self) -> float:
        return self.__timeStartInSec + mixer.music.get_pos() / 1000

    def getPlayingTime(self) -> float:
        return self.__getPlayingTime()

    def isPlaying(self) -> bool:
        if mixer.get_init() is None:
            return False
        return mixer.music.get_busy()

    def setVolume(self, volume: int):
        """
        set volume of the song, volume from 0 to 100
        """
        MAX_VOLUME = 100
        mixer.music.set_volume(volume / MAX_VOLUME)
