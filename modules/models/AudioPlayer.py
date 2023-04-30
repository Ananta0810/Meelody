from modules.helpers.types.Metas import SingletonMeta
from modules.models.PlaylistSongs import PlaylistSongs
from modules.models.Song import Song

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from pygame import mixer


class AudioPlayer(metaclass=SingletonMeta):
    __playlist: PlaylistSongs = None
    __current_song: Song = None
    __current_song_index: int = 0
    __time_start_in_sec: float = 0
    __loaded: bool = False
    __offset_rate: float = 1

    def __init__(self):
        mixer.pre_init()
        mixer.init()

    @staticmethod
    def get_instance() -> 'AudioPlayer':
        return AudioPlayer()

    def has_any_song(self):
        return self.__playlist is not None and self.__playlist.has_any_song()

    def load_playlist(self, playlist: PlaylistSongs) -> None:
        self.__playlist = playlist

    def set_time_start(self, time_start: float):
        self.__time_start_in_sec = time_start

    def get_time_start(self):
        return self.__time_start_in_sec

    @staticmethod
    def set_volume(volume: int):
        """
        set volume of the song, volume from 0 to 100
        """
        MAX_VOLUME = 100
        volume_as_float = volume / MAX_VOLUME
        mixer.music.set_volume(volume_as_float)

    def load_song_to_play(self):
        if self.__loaded:
            return
        song = self.__playlist.get_song_at(self.__current_song_index)
        if song is None:
            return
        self.reset_time()
        self.__current_song = song
        self.__offset_rate = 48000 / song.get_sample_rate()
        self.__loaded = True
        mixer.music.unload()
        mixer.music.load(song.get_location())

    def play(self):
        mixer.music.play(start=self.__get_playing_time())

    def select_previous_song(self):
        self.set_current_song_index((self.__current_song_index - 1) % self.__playlist.size())
        self.load_song_to_play()

    def select_next_song(self):
        self.set_current_song_index((self.__current_song_index + 1) % self.__playlist.size())
        self.load_song_to_play()

    def get_playlist(self) -> PlaylistSongs:
        return self.__playlist

    def get_songs(self) -> list[Song]:
        return self.__playlist.get_songs()

    def set_current_song_index(self, index: int) -> None:
        self.__current_song_index = index
        self.__loaded = False

    def set_current_song(self, title: str) -> None:
        song_index = self.__playlist.find_song_index_by_title(title)
        if song_index < 0 or song_index >= self.__playlist.size():
            song_index = 0
        self.__current_song_index = song_index
        self.__loaded = False

    def get_current_song(self) -> Song:
        return self.__current_song

    def get_current_song_index(self) -> int:
        return self.__current_song_index

    def skip_to_time(self, time: float) -> None:
        self.pause()
        self.set_time_start(time / self.__offset_rate)

    def pause(self) -> None:
        if not self.is_playing():
            return
        self.set_time_start(self.__get_playing_time())
        mixer.music.stop()

    def stop(self) -> None:
        if not self.is_playing():
            return
        mixer.music.stop()
        mixer.music.unload()
        self.__loaded = False

    def reset_time(self) -> None:
        self.__time_start_in_sec = 0

    def shuffle(self) -> None:
        self.__playlist.shuffle()

    def unshuffle(self) -> None:
        self.__playlist.unshuffle()

    def __get_playing_time(self) -> float:
        return self.__time_start_in_sec + mixer.music.get_pos() / 1000

    def get_playing_time(self) -> float:
        return self.__get_playing_time() * self.__offset_rate

    @staticmethod
    def is_playing() -> bool:
        if mixer.get_init() is None:
            return False
        return mixer.music.get_busy()
