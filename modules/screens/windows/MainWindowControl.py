from modules.helpers.types.Decorators import override
from modules.models.Playlist import Playlist
from modules.screens.AbstractScreen import BaseControl
from modules.screens.windows.MainWindowView import MainWindowView


class MainWindowControl(MainWindowView, BaseControl):

    def __init__(self) -> None:
        super().__init__()
        self.connect_signals()

    @override
    def connect_signals(self) -> None:
        pass

    def load_playlist(self, playlist: Playlist) -> None:
        self._music_player.load_playlist_songs(playlist.get_songs())
        self._body.load_playlist(playlist)