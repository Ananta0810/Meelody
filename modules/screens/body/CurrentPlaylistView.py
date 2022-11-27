from typing import Optional, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from modules.helpers.types.Decorators import override, connector
from modules.models.Playlist import Playlist
from modules.statics.view.Material import Images
from modules.screens.AbstractScreen import BaseView
from modules.screens.body.PlaylistInfoView import PlaylistInfoView
from modules.screens.body.songs_table.SongTableView import SongTableView


class CurrentPlaylistView(QWidget, BaseView):
    __main_layout: QHBoxLayout
    __info: PlaylistInfoView
    __menu: SongTableView

    def __init__(self, parent: Optional["QWidget"] = None):
        super(CurrentPlaylistView, self).__init__(parent)
        self.__init_ui()

    def __init_ui(self) -> None:
        self.__main_layout = QHBoxLayout(self)
        self.__main_layout.setAlignment(Qt.AlignLeft)
        self.__main_layout.setSpacing(50)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.__info = PlaylistInfoView()
        self.__info.set_default_cover(Images.DEFAULT_PLAYLIST_COVER)

        self.__menu = SongTableView()

        self.__main_layout.addLayout(self.__info)
        self.__main_layout.addWidget(self.__menu, stretch=2)

    @override
    def apply_light_mode(self) -> None:
        self.__info.apply_light_mode()
        self.__menu.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.__info.apply_dark_mode()
        self.__menu.apply_dark_mode()

    @connector
    def set_onclick_play(self, fn: Callable[[int], None]) -> None:
        self.__menu.set_onclick_play(fn)

    def load_playlist(self, playlist: Playlist) -> None:
        self.set_current_playlist_info(
            playlist.get_info().name, playlist.get_info().cover, playlist.size()
        )
        self.__menu.load_songs(playlist.get_songs())

    def set_current_playlist_info(self, name: str, cover: bytes = None, total_song: int = 0) -> None:
        if cover is None:
            cover = (
                Images.FAVOURITES_PLAYLIST_COVER
                if name.lower() == "favourites"
                else Images.DEFAULT_PLAYLIST_COVER
            )

        self.__info.set_cover(cover)
        self.__info.set_title(name)
        self.__info.set_total_song(total_song)
