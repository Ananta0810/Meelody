from typing import Optional, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from modules.helpers.types.Decorators import override, connector
from modules.models.Song import Song
from modules.screens.AbstractScreen import BaseView
from modules.screens.body.songs_table.SongTableBodyView import SongTableBodyView
from modules.screens.body.songs_table.SongTableHeaderView import SongTableHeaderView
from modules.screens.body.songs_table.SongTableRowView import SongTableRowView


class SongTableView(QWidget, BaseView):
    _main_layout: QVBoxLayout
    _header: SongTableHeaderView
    _body: SongTableBodyView
    __is_dark_mode: bool = False

    def __init__(self, parent: Optional["QWidget"] = None) -> None:
        super().__init__(parent)
        self.__init_ui()
        self._header.setText()

    def __init_ui(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setSpacing(4)
        self._main_layout.setContentsMargins(0, 0, 0, 0)

        self._header = SongTableHeaderView()
        self._header.setFixedHeight(48)

        self._body = SongTableBodyView()

        self._main_layout.addWidget(self._header)
        self._main_layout.addWidget(self._body)

    @override
    def apply_light_mode(self) -> None:
        self.__is_dark_mode = False
        self._header.apply_light_mode()
        self._body.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.__is_dark_mode = True
        self._header.apply_dark_mode()
        self._body.apply_dark_mode()

    @connector
    def set_onclick_play(self, fn: Callable[[int], None]) -> None:
        self._body.set_onclick_play(fn)

    @connector
    def set_onclick_love(self, fn: Callable[[int], None]) -> None:
        self._body.set_onclick_love(fn)

    @connector
    def set_onclick_add_to_playlist(self, fn: Callable[[int], None]) -> None:
        self._body.set_onclick_add_to_playlist(fn)

    @connector
    def set_onclick_remove_from_playlist(self, fn: Callable[[int], None]) -> None:
        self._body.set_onclick_remove_from_playlist(fn)

    @connector
    def set_onchange_song_title_and_artist_on_menu(self, fn: Callable[[int, str, str], bool]) -> None:
        self._body.set_onchange_song_title_and_cover(fn)

    @connector
    def set_onchange_song_cover_on_menu(self, fn: Callable[[int, str], None]) -> None:
        self._body.set_onchange_song_cover(fn)

    @connector
    def set_on_delete_song_on_menu(self, fn: Callable[[int], None]) -> None:
        self._body.set_on_delete_song(fn)

    @connector
    def set_on_keypress(self, fn: Callable[[str], int]) -> None:
        self._body.set_on_keypress(fn)

    @connector
    def set_onclose_download_dialog(self, fn: callable) -> None:
        self._header.set_onclose_download_dialog(fn)

    @connector
    def set_onclick_download_songs_to_library_fn(self, fn: Callable[[str], None]) -> None:
        self._header.set_onclick_download_songs_to_library_fn(fn)

    @connector
    def set_onclick_add_songs_to_library_fn(self, fn: Callable[[list[str]], None]) -> None:
        self._header.set_onclick_add_songs_to_library_fn(fn)

    @connector
    def set_onclick_select_songs_to_playlist_fn(self, fn: Callable[[], None]) -> None:
        self._header.set_onclick_select_songs_to_playlist_fn(fn)

    @connector
    def set_onclick_apply_select_songs_to_playlist_fn(self, fn: Callable[[], None]) -> None:
        self._header.set_onclick_apply_select_songs_to_playlist_fn(fn)

    def add_item(self, label: str) -> None:
        self._header.add_item(label)

    def mark_succeed_download_at(self, index: int) -> None:
        self._header.mark_succeed_at(index)

    def mark_processing_download_at(self, index: int) -> None:
        self._header.mark_processing_at(index)

    def mark_failed_download_at(self, index: int) -> None:
        self._header.mark_failed_at(index)

    def set_description_at(self, index: int, value: str) -> None:
        self._header.set_description_at(index, value)

    def set_progress_at(self, index: int, value: float) -> None:
        self._header.set_progress_at(index, value)

    def is_opening_download_dialog(self) -> bool:
        return self._header.is_opening_download_dialog()

    def enable_choosing_song(self, is_choosing: bool) -> None:
        self._body.enable_choosing_song(is_choosing)

    def enable_add_songs_to_library(self, visible: bool) -> None:
        self._header.enable_add_songs_to_library(visible)

    def enable_download_songs_to_library(self, visible: bool) -> None:
        self._header.enable_download_songs_to_library(visible)

    def enable_select_songs_to_playlist(self, visible: bool) -> None:
        self._header.enable_select_songs_to_playlist(visible)

    def _load_songs(self, songs: list[Song]) -> None:
        song_views: list[SongTableRowView] = self._body.load_songs(songs)
        if self.__is_dark_mode:
            for song_view in song_views:
                song_view.apply_dark_mode()
        else:
            for song_view in song_views:
                song_view.apply_light_mode()

    def _load_choosing_playlist(self, songs: list[Song]) -> None:
        song_views: list[SongTableRowView] = self._body.load_choosing_playlist(songs)
        if self.__is_dark_mode:
            for song_view in song_views:
                song_view.apply_dark_mode()
        else:
            for song_view in song_views:
                song_view.apply_light_mode()

    def update_song_at(self, index: int, song: Song) -> None:
        song_view: SongTableRowView = self._body.get_song_at(index)
        song_view.set_title(song.get_title())
        song_view.set_artist(song.get_artist())
        song_view.set_length(song.get_length())
        song_view.set_cover(song.get_cover())

    def enable_edit_songs(self, enabled: bool) -> None:
        songs = self._body.get_total_songs()
        for index in range(0, songs):
            self.enable_edit_of_song_at(index, enabled)

    def enable_delete_songs(self, enabled: bool) -> None:
        songs = self._body.get_total_songs()
        for index in range(0, songs):
            self.enable_delete_song_at(index, enabled)

    def enable_edit_of_song_at(self, index: int, enabled: bool) -> None:
        song_view: SongTableRowView = self._body.get_song_at(index)
        song_view.enable_edit(enabled)

    def enable_delete_song_at(self, index: int, enabled: bool) -> None:
        song_view: SongTableRowView = self._body.get_song_at(index)
        song_view.enable_delete(enabled)
