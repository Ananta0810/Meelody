from threading import Thread
from time import sleep
from typing import Callable

from modules.helpers.types.Decorators import handler, override, connector
from modules.helpers.types.Numbers import Numbers
from modules.models.AudioPlayer import AudioPlayer
from modules.models.PlaylistSongs import PlaylistSongs
from modules.models.Song import Song
from modules.screens.AbstractScreen import BaseControl
from modules.screens.music_bar.MusicPlayerBarView import MusicPlayerBarView


class MusicPlayerControl(MusicPlayerBarView, BaseControl):

    __player: AudioPlayer = AudioPlayer.get_instance()
    __thread_id: int = 0

    __onclick_play_fn: Callable[[int], None]
    __on_shuffle: Callable[[], None]
    __on_love: Callable[[Song], None]

    def __init__(self):
        super().__init__()
        self.connect_signals()

    @override
    def connect_signals(self) -> None:
        self._set_onclick_prev_song(lambda: self.play_previous_song())
        self._set_onclick_play_song(lambda: self.play_current_song())
        self._set_onclick_pause_song(lambda: self.pause_current_song())
        self._set_onclick_next_song(lambda: self.play_next_song())
        self._set_onchange_playing_time(lambda time: self.play_song_at_time(time))
        self._set_onclick_loop(lambda: self.change_loop_state())
        self._set_onclick_shuffle(lambda: self.change_shuffle_state())
        self._set_onclick_love(lambda: self.change_love_state())
        self._set_onchange_volume(lambda volume: self.change_volume(volume))

    @connector
    def set_onclick_play(self, fn: Callable[[int], None]) -> None:
        self.__onclick_play_fn = fn

    @connector
    def set_onclick_shuffle(self, fn: Callable[[], None]) -> None:
        self.__on_shuffle = fn

    @connector
    def set_onclick_love(self, fn: Callable[[Song], None]) -> None:
        self.__on_love = fn

    def load_playlist_songs(self, playlist: PlaylistSongs) -> None:
        self.__player.load_playlist(playlist)

    def load_playing_song(self, song_index: int = 0) -> None:
        self.__player.set_current_song_index(song_index)
        self.__player.load_song_to_play()
        self.__display_current_song_info()
            # self.change_shuffle_state()

    @handler
    def play_previous_song(self) -> None:
        if not self.__player.has_any_song():
            return
        self.__player.stop()
        self.__player.select_previous_song()
        self.__playSong()

    @handler
    def play_current_song(self) -> None:
        self.__playSong()

    @handler
    def pause_current_song(self) -> None:
        self.__player.pause()
        self.set_is_playing(False)

    @handler
    def play_next_song(self) -> None:
        if not self.__player.has_any_song():
            print("No song to play")
            return
        self.__player.stop()
        self.__player.select_next_song()
        self.__playSong()

    @handler
    def play_song_at_time(self, time: float) -> None:
        if not self.__player.has_any_song():
            return
        currentSong = self.__player.get_current_song()
        if currentSong is None:
            return
        self.__player.skip_to_time(time)
        self.__thread_start_player()

    @handler
    def play_song_at(self, index: int) -> None:
        self.pause_current_song()
        self.__player.set_current_song_index(index)
        self.__player.load_song_to_play()
        self.__player.set_time_start(0)
        self.play_current_song()

    @handler
    def change_loop_state(self) -> None:
        pass

    @handler
    def change_shuffle_state(self) -> None:
        if self.is_shuffle():
            self.__player.shuffle()
        else:
            self.__player.unshuffle()

        playlist: PlaylistSongs = self.__player.get_playlist()
        new_index = playlist.find_song_index_by_title(self.__player.get_current_song().get_title())
        if new_index < 0:
            new_index = 0
        self.__player.set_current_song_index(new_index)

        if self.__on_shuffle is not None:
            self.__on_shuffle()

    @handler
    def change_love_state(self) -> None:
        song = self.__player.get_current_song()
        if song is None:
            return
        song.reverse_love_state()
        self.set_love_state(song.is_loved())
        if self.__on_love is not None:
            self.__on_love(song)

    @handler
    def change_volume(self, volume: int) -> None:
        self.__player.set_volume(volume)

    def __playSong(self) -> None:
        if self.__player.get_current_song() is None:
            return
        if self.__onclick_play_fn is not None:
            self.__onclick_play_fn(self.__player.get_current_song_index())
        self.__display_current_song_info()
        self.__thread_start_player()

    def __thread_start_player(self) -> None:
        self.__thread_id += 1
        Thread(target=self.__startPlayer).start()

    def __startPlayer(self) -> None:
        thread_id: int = self.__thread_id
        interval: float = self.__calculate_refresh_ui_interval()
        self.set_is_playing(True)
        self.__player.play()

        while thread_id == self.__thread_id and self.__player.is_playing():
            self.__do_while_playing_music()
            sleep(interval)

        playing_this_song: bool = thread_id == self.__thread_id
        song_is_finished: bool = playing_this_song and self.is_playing()
        if song_is_finished:
            self.__do_after_song_finished()

    def __calculate_refresh_ui_interval(self) -> float:
        TIMES_THAT_UI_HAS_TO_UPDATE_FOR_SLIDER_WHILE_PLAYING: int = 100
        LONGEST_TIME_BREAK_FOR_A_UI_UPDATE_IN_SECONDS: float = 0.25

        return Numbers.clamp_float(
            self.__player.get_current_song().get_length() / TIMES_THAT_UI_HAS_TO_UPDATE_FOR_SLIDER_WHILE_PLAYING,
            min_value=0,
            max_value=LONGEST_TIME_BREAK_FOR_A_UI_UPDATE_IN_SECONDS
        )

    def __do_while_playing_music(self) -> None:
        self.set_playing_time(self.__player.get_playing_time())

    def __do_after_song_finished(self) -> None:
        if self.is_looping():
            self.__player.skip_to_time(0)
            self.__thread_start_player()
            return
        self.play_next_song()

    def __display_current_song_info(self) -> None:
        song: Song = self.__player.get_current_song()
        if song is None:
            self.display_song_info(None, "Artist", None, False)
            self.set_playing_time(0)
            self.set_total_time(0)
            return

        self.display_song_info(song.get_cover(), song.get_title(), song.get_artist(), song.is_loved())
        self.set_playing_time(self.__player.get_playing_time())
        self.set_total_time(song.get_length())
