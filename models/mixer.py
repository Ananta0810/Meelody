from sys import path

import mutagen.mp3
from pygame import mixer

from .playlist_songs import PlaylistSongs

path.append(".")
from entities.song import Song


class Mixer:
    _songs: PlaylistSongs
    _currentSongIndex: int
    _volume: int
    _loadedSong: bool
    _currentSong: Song
    _timeStartInSec: float
    _sampleOffset: int

    def __init__(self):
        self._songs = None
        self._currentSongIndex = 0
        self._currentSong = None
        self._volume = 100
        self._loadedSong = False
        self._timeStartInSec = 0
        self._sampleOffset = 1
        mixer.pre_init(48000, -16, 2, 2048)
        mixer.init()

    def loadPlaylist(self, playlist: PlaylistSongs):
        self._songs = playlist

    def setTimeStart(self, timeStart: float):
        # self._timeStartInSec = timeStart / self._sampleOffset
        self._timeStartInSec = timeStart

    def getTimeStart(self):
        return self._timeStartInSec

    def setVolume(self, volume: int):
        """
        set volume of the song, volume from 0 to 100
        """
        self._volume = volume
        mixer.music.set_volume(volume / 100)

    def load(self):
        if self._loadedSong:
            return
        mixer.music.unload()

        self._currentSong = self._songs.getSong(self._currentSongIndex)
        mixer.music.load(self._currentSong.location)
        print(f"Playing {self._currentSong.title}")

        mp3 = mutagen.mp3.MP3(self._currentSong.location)
        self._sampleOffset = 48000 / mp3.info.sample_rate

        self._loadedSong = True

    def playSongAt(self, index: int):
        pass

    def play(self):
        mixer.music.play(2, start=self._timeStartInSec)
        self.setVolume(self._volume)

    def next(self):
        self.resetTime()
        self._loadedSong = False
        self._currentSongIndex = (self._currentSongIndex + 1) % self._songs.size()

    def getCurrentSong(self):
        return self._currentSong

    def previous(self):
        self.resetTime()
        self._loadedSong = False
        self._currentSongIndex = (self._currentSongIndex - 1) % self._songs.size()

    def pause(self):
        try:
            # self._timeStartInSec = self.getPlayingTime() / self._sampleOffset
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
        self._songs.shuffle()

    def unshuffle(self):
        self._songs.unshuffle()

    def getPlayingTime(self) -> float:
        return self._timeStartInSec + mixer.music.get_pos() / 1000
        # ) * self._sampleOffset

    def isSongFinished(self):
        # return self.getPlayingTime() / self._sampleOffset >= self._currentSong.length
        return self.getPlayingTime() >= self._currentSong.length

    def isPlaying(self):
        try:
            return mixer.music.get_busy()
        except Mixer.BusyError:
            return False
