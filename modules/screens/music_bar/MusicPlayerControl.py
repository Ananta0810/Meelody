from threading import Thread
from time import sleep

from modules.helpers.types.Numbers import Numbers
from modules.models.AudioPlayer import AudioPlayer
from modules.models.PlaylistSongs import PlaylistSongs
from modules.models.Song import Song
from modules.screens.AbstractScreen import BaseControl
from modules.screens.music_bar.MusicPlayerBarView import MusicPlayerBarView


class MusicPlayerControl(MusicPlayerBarView, BaseControl):

    __player: AudioPlayer = AudioPlayer.get_instance()
    __thread_id: int = 0

    def __init__(self) -> None:
        super(MusicPlayerControl, self).__init__()
        playlist = PlaylistSongs()

        playlist.insert(Song.from_file("library/Abandoned Temple.mp3"))
        playlist.insert(Song.from_file("library/Graze The Roof.mp3"))
        playlist.insert(Song.from_file("library/Ship Battle.mp3"))
        playlist.insert(Song.from_file("library/Tom Tom.mp3"))

        self.__player.load_playlist(playlist)
        self.__player.set_current_song_index(0)
        self.__player.load_song_to_play()
        self.connect_signals()

    def connect_signals(self) -> None:
        self.set_onclick_prev_song(lambda: self.play_previous_song())
        self.set_onclick_play_song(lambda: self.play_current_song())
        self.set_onclick_pause_song(lambda: self.pause_current_song())
        self.set_onclick_next_song(lambda: self.play_next_song())

    def play_previous_song(self) -> None:
        if not self.__player.has_any_song():
            return
        self.__player.stop()
        self.__player.select_previous_song()
        self.__playSong()

    def play_current_song(self) -> None:
        self.__playSong()

    def pause_current_song(self) -> None:
        self.__player.pause()
        self.set_is_playing(False)

    def play_next_song(self) -> None:
        if not self.__player.has_any_song():
            return
        self.__player.stop()
        self.__player.select_next_song()
        self.__playSong()

    def __playSong(self) -> None:
        if self.__player.get_current_song() is None:
            return
        self.__display_current_song_info()
        self.__thread_start_player()

    def __thread_start_player(self) -> None:
        self.__thread_id += 1
        Thread(target=self.__startPlayer).start()

    def __startPlayer(self) -> None:
        thread_id: int = self.__thread_id
        interval: float = self.__get_interval_update_to_ui()
        self.set_is_playing(True)
        self.__player.play()

        while thread_id == self.__thread_id and self.__player.is_playing():
            self.__do_while_playing_music()
            sleep(interval)

        playing_this_song: bool = thread_id == self.__thread_id
        songIsFinished: bool = playing_this_song and self.is_playing()
        if songIsFinished:
            self.__do_after_song_finished()

    def __get_interval_update_to_ui(self) -> float:
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
            self.__thread_start_player()
            return
        self.play_next_song()

    def __display_current_song_info(self) -> None:
        song = self.__player.get_current_song()
        if song is None:
            self.display_song_info(None, "Artist", None, False)
            self.set_playing_time(0)
            self.set_total_time(0)
            return

        self.display_song_info(song.get_cover(), song.get_title(), song.get_artist(), song.is_loved())
        self.set_playing_time(self.__player.get_playing_time())
        self.set_total_time(song.get_length())
