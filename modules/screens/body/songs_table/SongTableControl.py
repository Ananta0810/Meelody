from modules.helpers.types.Decorators import override
from modules.models.AudioPlayer import AudioPlayer
from modules.models.PlaylistSongs import PlaylistSongs
from modules.screens.AbstractScreen import BaseControl
from modules.screens.body.songs_table.SongTableView import SongTableView


class SongTableControl(SongTableView, BaseControl):
    __playlist: PlaylistSongs = None
    __player: AudioPlayer = AudioPlayer()
    __is_choosing_song: bool = False

    def __init__(self) -> None:
        super().__init__()
        self.connect_signals()

    @override
    def connect_signals(self) -> None:
        pass

    def refresh(self) -> None:
        if self.__playlist is None:
            return
        for index, song in enumerate(self.__playlist.get_songs()):
            self.update_song_at(index, song)

    def load_songs(self, playlist: PlaylistSongs) -> None:
        self.__playlist = playlist
        self._load_songs(playlist.get_songs())

    def load_choosing_playlist(self, playlist: PlaylistSongs) -> None:
        self.__is_choosing_song = True
        self.__playlist = playlist
        self._load_choosing_playlist(playlist.get_songs())

    def select_song_at(self, index: int) -> None:
        if not self.__is_choosing_song:
            self._menu.select_song_at(index)

    def love_song(self, is_loved: bool) -> None:
        index = self.__player.get_current_song_index()
        self._menu.set_song_love_state_at_index(index, is_loved)
