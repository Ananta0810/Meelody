from typing import Optional, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from modules.helpers.types.Decorators import override, connector
from modules.models.Playlist import Playlist
from modules.screens.AbstractScreen import BaseView
from modules.screens.body.PlaylistInfoView import PlaylistInfoView
from modules.screens.body.songs_table.SongTableControl import SongTableControl
from modules.statics.view.Material import Images


class CurrentPlaylistView(QWidget, BaseView):
    __main_layout: QHBoxLayout
    __info: PlaylistInfoView
    __menu: SongTableControl

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

        self.__menu = SongTableControl()

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

    @connector
    def set_onclick_love(self, fn: Callable[[int], None]) -> None:
        self.__menu.set_onclick_love(fn)

    @connector
    def set_onclick_add_to_playlist_on_menu(self, fn: Callable[[int], None]) -> None:
        self.__menu.set_onclick_add_to_playlist(fn)

    @connector
    def set_onclick_remove_from_playlist_on_menu(self, fn: Callable[[int], None]) -> None:
        self.__menu.set_onclick_remove_from_playlist(fn)

    @connector
    def set_onchange_song_title_and_artist_on_menu(self, fn: Callable[[int, str, str], bool]) -> None:
        self.__menu.set_onchange_song_title_and_artist_on_menu(fn)

    @connector
    def set_onchange_song_cover_on_menu(self, fn: Callable[[int, str], None]) -> None:
        self.__menu.set_onchange_song_cover_on_menu(fn)

    @connector
    def set_on_delete_song_on_menu(self, fn: Callable[[int], None]) -> None:
        self.__menu.set_on_delete_song_on_menu(fn)

    @connector
    def set_on_keypress(self, fn: Callable[[str], int]) -> None:
        self.__menu.set_on_keypress(fn)

    @connector
    def set_onclick_download_songs_to_library_fn(self, fn: Callable[[str], None]) -> None:
        self.__menu.set_onclick_download_songs_to_library_fn(fn)

    @connector
    def set_onclick_add_songs_to_library_fn(self, fn: Callable[[list[str]], None]) -> None:
        self.__menu.set_onclick_add_songs_to_library_fn(fn)

    @connector
    def set_onclick_select_songs_to_playlist_fn(self, fn: Callable[[], None]) -> None:
        self.__menu.set_onclick_select_songs_to_playlist_fn(fn)

    @connector
    def set_onclick_apply_select_songs_to_playlist_fn(self, fn: Callable[[], None]) -> None:
        self.__menu.set_onclick_apply_select_songs_to_playlist_fn(fn)

    def enable_choosing_song(self, is_choosing: bool) -> None:
        self.__menu.enable_choosing_song(is_choosing)

    def enable_add_songs_to_library(self, visible: bool) -> None:
        self.__menu.enable_add_songs_to_library(visible)

    def enable_select_songs_to_playlist(self, visible: bool) -> None:
        self.__menu.enable_select_songs_to_playlist(visible)

    def refresh_menu(self) -> None:
        self.__menu.refresh()

    def love_song(self, is_loved: bool) -> None:
        self.__menu.love_song(is_loved)

    def select_song_at(self, index: int) -> None:
        self.__menu.select_song_at(index)

    def enable_edit_songs(self, enabled: bool) -> None:
        self.__menu.enable_edit_songs(enabled)

    def enable_delete_songs(self, enabled: bool) -> None:
        self.__menu.enable_delete_songs(enabled)

    def enable_edit_of_song_at(self, index: int, enabled: bool) -> None:
        self.__menu.enable_edit_of_song_at(index, enabled)

    def enable_delete_song_at(self, index: int, enabled: bool) -> None:
        self.__menu.enable_delete_song_at(index, enabled)

    def load_playlist(self, playlist: Playlist) -> None:
        self.set_current_playlist_info(playlist)
        self.__menu.load_songs(playlist.get_songs())

    def load_choosing_playlist(self, playlist: Playlist) -> None:
        self.__menu.load_choosing_playlist(playlist.get_songs())

    def set_current_playlist_info(self, playlist: Playlist) -> None:
        self.__info.set_cover(playlist.get_info().cover)
        self.__info.set_title(playlist.get_info().name)
        self.__info.set_total_song(playlist.size())
