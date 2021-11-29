from sys import path

from pygame import mixer

from .playlist_songs import PlaylistSongs

path.append(".lib/modules/")
from entities.song import Song

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
    _volume: int
    _loadedSong: bool
    _currentSong: Song
    _timeStartInSec: float
    _sampleRateOffset: float

    def __init__(self):
        self._playlist = None
        self._currentSongIndex = 0
        self._currentSong = None
        self._volume = 100
        self._loadedSong = False
        self._timeStartInSec = 0
        self._sampleRateOffset = 1
        mixer.pre_init()
        mixer.init()

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
        self._volume = volume
        mixer.music.set_volume(volume / 100)

    def loadSongToPlay(self):
        if self._loadedSong:
            return

        self._loadedSong = True
        self._currentSong = self._playlist.getSong(self._currentSongIndex)
        self._sampleRateOffset = 1

        mixer.music.unload()
        mixer.music.load(self._currentSong.location)

    def play(self):
        TIMES_PLAY_THE_SONG_ALLOWED_TO_PREVENT_THE_BUG_OF_THE_LIBRARY = 1
        mixer.music.play(
            TIMES_PLAY_THE_SONG_ALLOWED_TO_PREVENT_THE_BUG_OF_THE_LIBRARY,
            start=self._timeStartInSec,
        )
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

    def fixSampleRateOffsetWhenSongIsPaused(self):
        STANDARD_AUDIO_SAMPLE_RATE = 48000
        self._sampleRateOffset = (
            STANDARD_AUDIO_SAMPLE_RATE / self._currentSong._audio.getSampleRate()
        )

    def pause(self):
        try:
            self.fixSampleRateOffsetWhenSongIsPaused()
            self._timeStartInSec = self.getPlayingTime()
            mixer.music.stop()
        except:
            pass

    def stop(self):
        try:
            self.fixSampleRateOffsetWhenSongIsPaused()
            mixer.music.stop()
            self.resetTime()
        except:
            pass

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

    def isSongFinished(self):
        OFFSET_FOR_THE_CASE_WHEN_COMPARE_BETWEEN_FLOATING_POINT_IS_INCORRECT = 0.1
        return (
            self.getPlayingTime()
            + OFFSET_FOR_THE_CASE_WHEN_COMPARE_BETWEEN_FLOATING_POINT_IS_INCORRECT
            >= self._currentSong.length
        )

    def isPlaying(self):
        if mixer.get_init() is None:
            return False
        return mixer.music.get_busy()
