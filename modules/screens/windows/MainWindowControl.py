from modules.helpers.types.Decorators import override
from modules.models.AudioPlayer import AudioPlayer
from modules.models.Playlist import Playlist
from modules.screens.AbstractScreen import BaseControl
from modules.screens.windows.MainWindowView import MainWindowView


class MainWindowControl(MainWindowView, BaseControl):
    __playlist: Playlist
    __player: AudioPlayer = AudioPlayer()

    def __init__(self) -> None:
        super().__init__()
        self.connect_signals()

    @override
    def connect_signals(self) -> None:
        self._music_player.set_onclick_play(lambda index: self._body.select_song_at(index))
        self._music_player.set_onclick_shuffle(lambda: self._body.refresh_menu())
        self._music_player.set_onclick_love(lambda is_loved: self._body.love_song(is_loved))
        self._body.set_onclick_play(lambda index: self.play_song_at(index))
        self._body.set_onclick_love(lambda index: self.love_song_at(index))
        self._body.set_on_keypress(lambda key: self.go_to_song_that_title_start_with(key))
        self.set_onclick_close(lambda: self._music_player.pause_current_song())

    def love_song_at(self, index: int) -> None:
        if self.__player.get_current_song_index() == index:
            self._music_player.change_love_state()
            return
        song = self.__playlist.get_songs().get_song_at(index)
        song.reverse_love_state()

    def load_playlist(self, playlist: Playlist) -> None:
        self.__playlist = playlist
        self._music_player.load_playlist_songs(playlist.get_songs())
        self._body.load_playlist(playlist)

    def play_song_at(self, index: int) -> None:
        self._music_player.play_song_at(index)

    def go_to_song_that_title_start_with(self, title: str) -> int:
        return self.__playlist.get_songs().find_nearest_song_index_by_title(title)
