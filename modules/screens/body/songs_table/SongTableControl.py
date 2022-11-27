from modules.helpers.types.Decorators import override
from modules.models.PlaylistSongs import PlaylistSongs
from modules.screens.AbstractScreen import BaseControl
from modules.screens.body.songs_table.SongTableView import SongTableView


class SongTableControl(SongTableView, BaseControl):
    __playlist: PlaylistSongs = None

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
            self._update_song_at(
                index, song.get_title(), song.get_artist(), song.get_length(), song.get_cover()
            )

    def load_songs(self, playlist: PlaylistSongs) -> None:
        self.__playlist = playlist
        for song in playlist.get_songs():
            self._add_song(song.get_title(), song.get_artist(), song.get_length(), song.get_cover())

    def select_song_at(self, index: int) -> None:
        self._body.select_song_at(index)
