from sys import path

from pygame import mixer

from .playlist_songs import PlaylistSongs

path.append(".")
from lib.modules.entities.song import Song


class Player:
    _playlist: PlaylistSongs
    _currentSongIndex: int
    _volume: int
    _loadedSong: bool
    _currentSong: Song
    _timeStartInSec: float

    def __init__(self):
        self._playlist = None
        self._currentSongIndex = 0
        self._currentSong = None
        self._volume = 100
        self._loadedSong = False
        self._timeStartInSec = 0
        mixer.pre_init()
        mixer.init()

    def loadPlaylist(self, playlist: PlaylistSongs):
        self._playlist = playlist

    def setTimeStart(self, timeStart: float):
        self._timeStartInSec = timeStart

    def getTimeStart(self):
        return self._timeStartInSec

    def setVolume(self, volume: int):
        """
        set volume of the song, volume from 0 to 100
        """
        self._volume = volume
        mixer.music.set_volume(volume / 100)

    def loadSongToPlay(self):
        if self._loadedSong:
            return
        mixer.music.unload()

        self._loadedSong = True
        self._currentSong = self._playlist.getSong(self._currentSongIndex)
        mixer.music.load(self._currentSong.location)

    def play(self):
        mixer.music.play(2, start=self._timeStartInSec)
        self.setVolume(self._volume)

    def next(self):
        self.resetTime()
        self._loadedSong = False
        self._currentSongIndex = (self._currentSongIndex + 1) % self._playlist.size()

    def getCurrentSong(self):
        return self._currentSong

    def previous(self):
        self.resetTime()
        self._loadedSong = False
        self._currentSongIndex = (self._currentSongIndex - 1) % self._playlist.size()

    def pause(self):
        try:
            self._timeStartInSec = self.getPlayingTime()
            mixer.music.stop()
        except:
            pass

    def stop(self):
        try:
            self.resetTime()
            mixer.music.stop()
        except:
            pass

    def resetTime(self):
        self._timeStartInSec = 0

    def shuffle(self):
        self._playlist.shuffle()

    def unshuffle(self):
        self._playlist.unshuffle()

    def getPlayingTime(self) -> float:
        return self._timeStartInSec + mixer.music.get_pos() / 1000

    def isSongFinished(self):
        return self.getPlayingTime() >= self._currentSong.length

    def isPlaying(self):
        try:
            return mixer.music.get_busy()
        except:
            return False
