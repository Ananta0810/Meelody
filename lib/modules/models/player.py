from sys import path

path.append(".lib/modules/")
from modules.entities.song import Song
from modules.models.timer import Timer
from pygame import mixer

from .playlist_songs import PlaylistSongs

#! Known issues from the library:
# * 1: The function that calculates the playing time of the song will return the time since you start the song.
# * Which means if you play the song more than once, you will not get the desired playing time of the song
# * ==> Solution: play the song once, after it ended, restart it.

# * 2: When you pause the song, if you play it again, the speed of the song will be changed if the song has
# * frequency (sample rate) unequaled to 48000 hz.
# * ==> Solution: When unpause the song, change the speed of the song


class Player:
    _playlist: PlaylistSongs
    _currentSongIndex: int
    _currentSong: Song
    _timeStartInSec: float
    _sampleRateOffset: float
    _loadedSong: bool
    timer: Timer

    def __init__(self):
        self._playlist = None
        self._currentSongIndex = 0
        self._currentSong = None
        self._timeStartInSec = 0
        self._sampleRateOffset = 1
        self._loadedSong = False
        self.timer = Timer()
        # mixer.pre_init()
        mixer.init()

    def hasSong(self):
        return self._playlist is not None and self._playlist.hasSong()

    def loadPlaylist(self, playlist: PlaylistSongs):
        self._playlist = playlist

    def setTimeStart(self, timeStart: float):
        self._timeStartInSec = timeStart / self._sampleRateOffset

    def getTimeStart(self):
        return self._timeStartInSec

    def setVolume(self, volume: int):
        """
        set volume of the song, volume from 0 to 100
        """
        MAX_VOLUME = 100
        volumeAsFloat = volume / MAX_VOLUME
        mixer.music.set_volume(volumeAsFloat)

    def loadSongToPlay(self):
        if self._loadedSong:
            return

        self._loadedSong = True
        self._currentSong = self._playlist.getSong(self._currentSongIndex)
        self._sampleRateOffset = 1

        mixer.music.unload()
        if self._currentSong is None:
            return
        mixer.music.load(self._currentSong.location)

    def play(self):
        mixer.music.play(start=self._timeStartInSec)

    def next(self):
        self.resetTime()
        self._loadedSong = False
        self._currentSongIndex = (
            self._currentSongIndex + 1
        ) % self._playlist.size()

    def getPlaylist(self) -> list[Song]:
        return self._playlist

    def setCurrentSongIndex(self, index: int) -> None:
        self._currentSongIndex = index

    def setCurrentSong(self, title: str) -> None:
        songIndex = self._playlist.findSongByTitle(title)
        if songIndex < 0 or songIndex >= len(self._playlist._songs):
            songIndex = 0
        self._currentSongIndex = songIndex

    def getCurrentSong(self):
        return self._currentSong

    def previous(self):
        self.resetTime()
        self._loadedSong = False
        self._currentSongIndex = (
            self._currentSongIndex - 1
        ) % self._playlist.size()

    def fixSampleRateOffsetWhenSongIsPaused(self):
        if self._currentSong is None:
            return
        STANDARD_AUDIO_SAMPLE_RATE = 48000
        self._sampleRateOffset = (
            STANDARD_AUDIO_SAMPLE_RATE
            / self._currentSong._audio.getSampleRate()
        )

    def pause(self):
        if not self.isPlaying():
            return
        self.fixSampleRateOffsetWhenSongIsPaused()
        self.setTimeStart(self.getPlayingTime())
        mixer.music.stop()

    def stop(self):
        if not self.isPlaying():
            return
        self.fixSampleRateOffsetWhenSongIsPaused()
        self.resetTime()
        mixer.music.stop()

    def resetTime(self):
        self._timeStartInSec = 0

    def shuffle(self):
        self._playlist.shuffle()

    def unshuffle(self):
        self._playlist.unshuffle()

    def getPlayingTime(self) -> float:
        return (
            self._timeStartInSec + mixer.music.get_pos() / 1000
        ) * self._sampleRateOffset

    def isPlaying(self):
        if mixer.get_init() is None:
            return False
        return mixer.music.get_busy()
