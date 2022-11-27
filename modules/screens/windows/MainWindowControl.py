from modules.helpers.types.Decorators import override
from modules.models.Playlist import Playlist
from modules.screens.AbstractScreen import BaseControl
from modules.screens.windows.MainWindowView import MainWindowView


class MainWindowControl(MainWindowView, BaseControl):
    __playlist: Playlist

    def __init__(self) -> None:
        super().__init__()
        self.connect_signals()

    @override
    def connect_signals(self) -> None:
        self._music_player.set_onclick_play(lambda index: self._body.select_song_at(index))
        self._body.set_onclick_play(lambda index: self.play_song_at(index))
        self._body.set_on_keypress(lambda key: self.go_to_song_that_title_start_with(key))

    def load_playlist(self, playlist: Playlist) -> None:
        self.__playlist = playlist
        self._music_player.load_playlist_songs(playlist.get_songs())
        self._body.load_playlist(playlist)

    def play_song_at(self, index: int) -> None:
        self._music_player.play_song_at(index)

    def go_to_song_that_title_start_with(self, title: str) -> int:
        return self.__playlist.get_songs().find_nearest_song_index_by_title(title)