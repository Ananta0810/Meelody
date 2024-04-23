import os
import random
from time import sleep
from typing import Optional, Callable

from PyQt5.QtCore import QObject, pyqtSignal, QThread
from pygame import mixer

from app.common.models import Song, Playlist
from app.helpers.base import Numbers

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


class MusicPlayer(QObject):
    played = pyqtSignal()
    paused = pyqtSignal()

    songChanged = pyqtSignal(Song)
    loopChanged = pyqtSignal(bool)
    shuffleChanged = pyqtSignal(bool)
    volumeChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        mixer.pre_init()
        mixer.init()

        self.__songs: Optional[Playlist.Songs] = None
        self.__shuffledSongs: Optional[Playlist.Songs] = None
        self.__currentSong: Optional[Song] = None
        self.__currentSongIndex: int = 0
        self.__timeStartInSec: float = 0
        self.__loaded: bool = False
        self.__timeToStopAsSeconds: int | None = None
        self.__elapsedTimeAsSeconds: int = 0
        self.__isLooping = False
        self.__isShuffle = False

        self.__finishTrackerThread = _MusicFinishedTrackThread(self, onSongFinished=self.__onSongFinished)

    def hasAnySong(self):
        return self.__songs is not None and self.__songs.hasAnySong()

    def loadPlaylist(self, songs: Playlist.Songs) -> None:
        self.__songs = songs

    def setStartTime(self, timeStart: float):
        self.__timeStartInSec = timeStart

    def getTimeStart(self):
        return self.__timeStartInSec

    def loadSongToPlay(self):
        if self.__loaded:
            return

        songs = self.__getSongs()
        song = songs.getSongAt(self.__currentSongIndex)
        if song is None:
            return

        self.resetTime()
        self.__currentSong = song
        self.__loaded = True
        mixer.music.unload()
        mixer.music.load(song.getLocation())
        self.songChanged.emit(song)

    def __getSongs(self):
        return self.__shuffledSongs if self.__isShuffle else self.__songs

    def play(self):
        mixer.music.play(start=self.getPlayingTime())
        self.__finishTrackerThread.start()
        self.played.emit()

    def playPreviousSong(self):
        if not self.hasAnySong():
            return
        self.stop()
        self.setCurrentSongIndex((self.__currentSongIndex - 1) % self.__songs.size())
        self.loadSongToPlay()
        self.setStartTime(0)
        self.play()

    def playNextSong(self):
        if not self.hasAnySong():
            return
        self.stop()
        self.setCurrentSongIndex((self.__currentSongIndex + 1) % self.__songs.size())
        self.loadSongToPlay()
        self.setStartTime(0)
        self.play()

    def setCurrentSongIndex(self, index: int) -> None:
        self.__currentSongIndex = index
        self.__loaded = False

    def getCurrentSong(self) -> Song:
        return self.__currentSong

    def getCurrentSongIndex(self) -> int:
        return self.__currentSongIndex

    def skipToTime(self, time: float) -> None:
        self.pause()
        self.setStartTime(time)

    def pause(self, emitSignal: bool = True) -> None:
        if not self.isPlaying():
            return
        self.setStartTime(self.getPlayingTime())
        mixer.music.stop()
        self.__finishTrackerThread.quit()
        if emitSignal:
            self.paused.emit()

    def stop(self) -> None:
        if not self.isPlaying():
            return
        mixer.music.stop()
        mixer.music.unload()
        self.__finishTrackerThread.quit()
        self.__loaded = False
        self.paused.emit()

    def setLooping(self, a0: bool) -> None:
        self.__isLooping = a0
        self.loopChanged.emit(a0)

    def setShuffle(self, a0: bool) -> None:
        self.__isShuffle = a0

        if self.__isShuffle:
            songs = self.__songs.getSongs()
            random.shuffle(songs)
            self.__shuffledSongs = Playlist.Songs(songs, isSorted=False)
            if self.__currentSong is not None:
                currentSongNewIndex = self.__shuffledSongs.indexOf(self.__currentSong)
                self.__currentSongIndex = currentSongNewIndex
        else:
            self.__shuffledSongs = None

        self.shuffleChanged.emit(a0)

    def resetTime(self) -> None:
        self.__timeStartInSec = 0

    def getPlayingTime(self) -> float:
        return self.__timeStartInSec + mixer.music.get_pos() / 1000

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
        self.volumeChanged.emit(volume)

    def refreshRate(self) -> float:
        TIMES_THAT_UI_HAS_TO_UPDATE_FOR_SLIDER_WHILE_PLAYING: int = 100
        LONGEST_TIME_BREAK_FOR_A_UI_UPDATE_IN_SECONDS: float = 0.25

        return Numbers.clamp(
            self.getCurrentSong().getLength() / TIMES_THAT_UI_HAS_TO_UPDATE_FOR_SLIDER_WHILE_PLAYING,
            min_value=0,
            max_value=LONGEST_TIME_BREAK_FOR_A_UI_UPDATE_IN_SECONDS
        )

    def __onSongFinished(self) -> None:
        if self.__isLooping:
            self.pause(emitSignal=False)
            self.setStartTime(0)
            self.play()
            return
        self.playNextSong()


class _MusicFinishedTrackThread(QThread):

    def __init__(self, musicPlayer: MusicPlayer, onSongFinished: Callable) -> None:
        super().__init__()
        self.__musicPlayer = musicPlayer
        self.__onSongFinished = onSongFinished
        self.__thread_id: int = 0

    def run(self) -> None:
        self.__thread_id += 1
        thread_id = self.__thread_id

        refreshRate: float = self.__musicPlayer.refreshRate()

        while self.__musicPlayer.isPlaying():
            sleep(refreshRate)

        if thread_id == self.__thread_id:
            self.__onSongFinished()