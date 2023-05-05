import sys
from threading import Thread
from time import sleep
from typing import Callable

from modules.helpers import Times, Printers
from modules.helpers.types import Numbers
from modules.helpers.types.Decorators import handler, override, connector
from modules.models.AudioPlayer import AudioPlayer
from modules.models.PlaylistSongs import PlaylistSongs
from modules.models.Song import Song
from modules.screens.AbstractScreen import BaseControl
from modules.screens.music_bar.MusicPlayerBar import MusicPlayerBar


class MusicPlayerControl(MusicPlayerBar, BaseControl):
    __player: AudioPlayer = AudioPlayer.get_instance()
    __thread_id: int = 0

    __onclick_play_fn: Callable[[int], None] = None
    __onclick_next_fn: Callable[[int], None] = None
    __onclick_prev_fn: Callable[[int], None] = None
    __onclick_pause_fn: Callable[[int], None] = None
    __on_shuffle: Callable[[bool], None] = None
    __on_loop: Callable[[bool], None] = None
    __on_love: Callable[[Song], None] = None

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
        self._set_onclick_shuffle(lambda shuffle: self.change_shuffle_state(shuffle))
        self._set_onclick_love(lambda: self.change_love_state())
        self._set_on_set_timer(self.set_timer)
        self._set_onchange_volume(lambda volume: self.change_volume(volume))

    @connector
    def set_onclick_play(self, fn: Callable[[int], None]) -> None:
        self.__onclick_play_fn = fn

    @connector
    def set_onclick_pause(self, fn: Callable[[int], None]) -> None:
        self.__onclick_pause_fn = fn

    @connector
    def set_onclick_prev(self, fn: Callable[[int], None]) -> None:
        self.__onclick_prev_fn = fn

    @connector
    def set_onclick_next(self, fn: Callable[[int], None]) -> None:
        self.__onclick_next_fn = fn

    @connector
    def set_onclick_shuffle(self, fn: Callable[[bool], None]) -> None:
        self.__on_shuffle = fn

    @connector
    def set_onclick_loop(self, fn: Callable[[bool], None]) -> None:
        self.__on_loop = fn

    @connector
    def set_onclick_love(self, fn: Callable[[Song], None]) -> None:
        self.__on_love = fn

    def load_playlist_songs(self, playlist: PlaylistSongs) -> None:
        self.__player.load_playlist(playlist)

    def load_playing_song(self, song_index: int = 0) -> None:
        if self.__player.has_any_song():
            self.__player.set_current_song_index(song_index)
            self.__player.load_song_to_play()

        self.__display_current_song_info()

    @handler
    def play_previous_song(self) -> None:
        if not self.__player.has_any_song():
            Printers.error("No song to play.")
            return
        self.__player.stop()
        self.__player.select_previous_song()
        print(f"Play previous song {self.__player.get_current_song().get_title()}.")
        self.__playSong()
        self.__onclick_prev_fn(self.__player.get_current_song_index())

    @handler
    def play_next_song(self) -> None:
        if not self.__player.has_any_song():
            Printers.error("No song to play.")
            return
        self.__player.stop()
        self.__player.select_next_song()
        print(f"Play next song {self.__player.get_current_song().get_title()}.")
        self.__playSong()
        self.__onclick_next_fn(self.__player.get_current_song_index())

    @handler
    def play_current_song(self) -> None:
        song = self.__player.get_current_song()
        if song is None:
            self.set_is_playing(False)
            Printers.error('No song to play.')
            return
        playing_time = Times.string_of(self.__player.get_playing_time())
        print(f"Playing {song.get_title()} at {playing_time}.")
        self.__playSong()

    @handler
    def pause_current_song(self) -> None:
        song = self.__player.get_current_song()
        if song is not None:
            playing_time = Times.string_of(self.__player.get_playing_time())
            print(f"Paused {song.get_title()} at {playing_time}")
        self.__player.pause()
        self.set_is_playing(False)
        if self.__onclick_pause_fn is not None:
            self.__onclick_pause_fn(self.__player.get_current_song_index())

    @handler
    def stop_current_song(self) -> None:
        self.__player.stop()
        self.set_playing_time(0)
        self.set_is_playing(False)

    @handler
    def play_song_at_time(self, time: float) -> None:
        if not self.__player.has_any_song():
            Printers.error("No song to play.")
            return
        currentSong = self.__player.get_current_song()
        if currentSong is None:
            Printers.error("No song to play.")
            return

        self.__player.skip_to_time(time)
        playing_time = Times.string_of(self.__player.get_playing_time())
        print(f"Skip song {self.__player.get_current_song().get_title()} at {playing_time}.")
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
        if self.__on_loop is not None:
            self.__on_loop(self.is_looping())

    @handler
    def change_shuffle_state(self, shuffle: bool) -> None:
        if shuffle:
            self.__player.shuffle()
        else:
            self.__player.unshuffle()

        playlist: PlaylistSongs = self.__player.get_playlist()
        if not playlist.has_any_song():
            return
        new_index = playlist.index_of(self.__player.get_current_song())
        if new_index < 0:
            new_index = 0
        self.__player.set_current_song_index(new_index)

        if self.__on_shuffle is not None:
            self.__on_shuffle(self.is_shuffle())

    @handler
    def change_love_state(self) -> None:
        song = self.__player.get_current_song()
        if song is None:
            Printers.error("No song to love.")
            return
        song.reverse_love_state()
        self.set_love_state(song.is_loved())
        print(f"{'Loved' if song.is_loved() else 'Unloved'} song {song.get_title()}")
        if self.__on_love is not None:
            self.__on_love(song)

    @handler
    def change_volume(self, volume: int) -> None:
        self.__player.set_volume(volume)

    @handler
    def set_timer(self, minutes: int | None) -> bool:
        if minutes is None:
            self.__player.reset_timer()
            print(f"Reset timer.")
            return True
        self.__player.set_timer(minutes)
        return True

    @override
    def set_loop(self, enable: bool) -> None:
        super().set_loop(enable)

    @override
    def set_shuffle(self, enable: bool) -> None:
        if self.__player.get_playlist() is None:
            super().set_shuffle(enable)
            return

        if enable:
            self.__player.shuffle()
        else:
            self.__player.unshuffle()

        playlist: PlaylistSongs = self.__player.get_playlist()
        if not playlist.has_any_song():
            return
        new_index = playlist.index_of(self.__player.get_current_song().get_title())
        if new_index < 0:
            new_index = 0
        self.__player.set_current_song_index(new_index)
        super().set_shuffle(enable)

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
        if not self.is_playing():
            self.set_is_playing(True)
        self.__player.play()

        while thread_id == self.__thread_id and self.__player.is_playing():
            self.__update_ui()
            self.__countdown_timer(interval)
            sys.stdout.flush()
            sleep(interval)

        playing_this_song: bool = thread_id == self.__thread_id
        song_is_finished: bool = playing_this_song and self.is_playing()
        if song_is_finished:
            self.__do_after_song_finished()

    def __countdown_timer(self, interval_in_sec: float) -> None:
        if not self.__player.is_countdown_timer():
            return
        self.__player.tick(interval_in_sec)
        if self.__player.is_reached_timer():
            self.pause_current_song()
            self.__player.reset_timer()
            print("Paused song because timer is up.")

    def do_after_played(self, interval, thread_id):
        while thread_id == self.__thread_id and self.__player.is_playing():
            self.__update_ui()
            sleep(interval)

        playing_this_song: bool = thread_id == self.__thread_id
        song_is_finished: bool = playing_this_song and self.is_playing()
        if song_is_finished:
            self.__do_after_song_finished()

    def __calculate_refresh_ui_interval(self) -> float:
        TIMES_THAT_UI_HAS_TO_UPDATE_FOR_SLIDER_WHILE_PLAYING: int = 100
        LONGEST_TIME_BREAK_FOR_A_UI_UPDATE_IN_SECONDS: float = 0.25

        return Numbers.clamp(
            self.__player.get_current_song().get_length() / TIMES_THAT_UI_HAS_TO_UPDATE_FOR_SLIDER_WHILE_PLAYING,
            min_value=0,
            max_value=LONGEST_TIME_BREAK_FOR_A_UI_UPDATE_IN_SECONDS
        )

    def __update_ui(self) -> None:
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
            self.display_song_info(None, "Song Title", "Song Artist", False)
            self.set_playing_time(0)
            self.set_total_time(0)
            return

        self.display_song_info(song.get_cover(), song.get_title(), song.get_artist(), song.is_loved())
        self.set_playing_time(self.__player.get_playing_time())
        self.set_total_time(song.get_length())
