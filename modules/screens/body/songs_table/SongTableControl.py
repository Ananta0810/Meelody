from modules.helpers.types.Decorators import override, connector
from modules.models.AudioPlayer import AudioPlayer
from modules.models.PlaylistSongs import PlaylistSongs
from modules.screens.AbstractScreen import BaseControl
from modules.screens.body.songs_table.SongTableView import SongTableView


class SongTableControl(SongTableView, BaseControl):
    __playlist: PlaylistSongs = None
    __player: AudioPlayer = AudioPlayer()

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
            self._update_song_at(index, song)

    def load_songs(self, playlist: PlaylistSongs) -> None:
        self.__playlist = playlist
        for song in playlist.get_songs():
            self._add_song(song)

    def select_song_at(self, index: int) -> None:
        self._body.select_song_at(index)

    def love_song(self, is_loved: bool) -> None:
        index = self.__player.get_current_song_index()
        self._body.set_song_love_state_at_index(index, is_loved)
