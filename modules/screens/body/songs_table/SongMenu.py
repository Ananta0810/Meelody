from typing import Optional, Callable

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QWidget, QFileDialog

from modules.helpers.types.Decorators import override, connector
from modules.models.Song import Song
from modules.screens.AbstractScreen import BaseView
from modules.screens.body.songs_table.SongTableRowView import SongTableRowView
from modules.statics import Properties
from modules.statics.view.Material import Images, Backgrounds
from modules.widgets import Dialogs
from modules.widgets.MenuLayout import MenuLayout
from modules.widgets.ScrollAreas import SmoothVerticalScrollArea


class SongMenu(SmoothVerticalScrollArea, BaseView):
    __menu: MenuLayout

    __onclick_button_fn: Callable[[int], None] = None
    __onclick_love_fn: Callable[[int], None] = None
    __onclick_add_to_playlist_fn: Callable[[int], None] = None
    __onclick_remove_from_playlist_fn: Callable[[int], None] = None
    __onchange_cover_fn: Callable[[int, str], None] = None
    __onchange_title_fn: Callable[[int, str], bool] = None
    __on_delete_fn: Callable[[int], None] = None
    __on_keypress_fn: Callable[[str], int] = None

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)
        self.start: int = 0
        self.last: int = 6
        self.__song_views: list[SongTableRowView] = []
        self.__is_light_mode = True
        self._current_song_index: list[int] = []
        self.__init_ui()

    def __init_ui(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.set_item_height(104)

        self.__menu = MenuLayout(self)
        self.setWidget(self.__menu)
        self.__menu.setContentsMargins(8, 0, 8, 8)

    @override
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.__menu.setFixedWidth(self.rect().width() - 4)
        super().resizeEvent(a0)

    @override
    def apply_light_mode(self) -> None:
        self.__is_light_mode = True
        self.setStyleSheet(SmoothVerticalScrollArea.build_style(background=Backgrounds.CIRCLE_PRIMARY))
        for song in self.__song_views:
            song.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.__is_light_mode = False
        self.setStyleSheet(SmoothVerticalScrollArea.build_style(background=Backgrounds.CIRCLE_PRIMARY))
        for song in self.__song_views:
            song.apply_dark_mode()

    @connector
    def set_onclick_play(self, fn: Callable[[int], None]) -> None:
        self.__onclick_button_fn = fn
        for index, song in enumerate(self.__song_views):
            song.set_onclick_play(lambda: self.__onclick_play_btn(index))

    @connector
    def set_onclick_love(self, fn: Callable[[int], None]) -> None:
        self.__onclick_love_fn = fn
        for index, song in enumerate(self.__song_views):
            song.set_onclick_love(lambda: self.__onclick_love_btn(index))

    @connector
    def set_onclick_add_to_playlist(self, fn: Callable[[int], None]) -> None:
        self.__onclick_add_to_playlist_fn = fn
        for index, song in enumerate(self.__song_views):
            song.set_onclick_add_to_playlist(lambda: self.__onclick_add_to_playlist_fn(index))

    @connector
    def set_onclick_remove_from_playlist(self, fn: Callable[[int], None]) -> None:
        self.__onclick_remove_from_playlist_fn = fn
        for index, song in enumerate(self.__song_views):
            song.set_onclick_remove_from_playlist(lambda: self.__onclick_remove_from_playlist_fn(index))

    @connector
    def set_onchange_song_cover(self, fn: Callable[[int, str], None]) -> None:
        self.__onchange_cover_fn = fn
        for index, song in enumerate(self.__song_views):
            song.set_on_edit_cover(lambda: self.__choose_cover_for_song_at(index))

    @connector
    def set_on_delete_song(self, fn: Callable[[int], None]) -> None:
        self.__on_delete_fn = fn
        for index, song in enumerate(self.__song_views):
            song.set_on_delete(lambda: self.__confirm_delete_song(index))

    def __confirm_delete_song(self, index: int) -> None:
        return Dialogs.confirm(
            image=Images.DELETE,
            header="Warning",
            message="Are you sure want to delete this song?\n The song will be deleted permanently\n from the storage.",
            acceptText="Delete",
            cancelText="Cancel",
            on_accept=lambda: self.__on_delete_fn(index)
        )

    @connector
    def set_onchange_song_title_and_cover(self, fn: Callable[[int, str, str], bool]) -> None:
        self.__onchange_title_fn = fn
        for index, song in enumerate(self.__song_views):
            song.set_on_update_info(lambda title, artist: fn(index, title, artist))

    def __choose_cover_for_song_at(self, index: int) -> None:
        path = QFileDialog.getOpenFileName(self, filter=Properties.ImportType.IMAGE)[0]
        if path is not None and path != '':
            self.__onchange_cover_fn(index, path)

    def __onclick_play_btn(self, index: int) -> None:
        self.select_song_at(index)
        if self.__onclick_button_fn is not None:
            self.__onclick_button_fn(index)

    def __onclick_love_btn(self, index: int) -> None:
        if self.__onclick_love_fn is not None:
            self.__onclick_love_fn(index)

    @connector
    def set_on_keypress(self, fn: Callable[[str], int]) -> None:
        self.__on_keypress_fn = fn

    @override
    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.__on_keypress(event)
        return super().keyPressEvent(event)

    def __on_keypress(self, event: QKeyEvent) -> None:
        is_holding_alt = int(event.modifiers()) == Qt.AltModifier
        if not is_holding_alt:
            return
        try:
            key = chr(event.key())
            index = self.__on_keypress_fn(key)
            if index == -1:
                return
            self._scroll_to_item_at(index)
        except ValueError:
            pass

    def set_song_cover_at_index(self, index: int, cover: bytes) -> None:
        self.get_song_at(index).set_cover(cover)

    def set_song_title_at_index(self, index: int, title: str) -> None:
        self.get_song_at(index).set_title(title)

    def set_song_artist_at_index(self, index: int, artist: str) -> None:
        self.get_song_at(index).set_artist(artist)

    def set_song_length_at_index(self, index: int, length: float) -> None:
        self.get_song_at(index).set_length(length)

    def set_song_love_state_at_index(self, index: int, state: bool) -> None:
        self.get_song_at(index).set_love_state(state)

    def get_total_songs(self) -> int:
        return self.__menu.getTotalDisplaying()

    def load_songs(self, songs: list[Song]) -> None:
        total_rows = len(self.__song_views)
        total_songs = len(songs)

        is_lacking_rows = total_rows < total_songs
        if is_lacking_rows:
            total_lacking_rows = total_songs - total_rows

            self.__add_rows(total_lacking_rows)
            self.__display_songs(songs)
            return

        self.__display_songs(songs)

    def __add_rows(self, total_lacking_rows) -> None:
        for i in range(0, total_lacking_rows):
            song_view = SongTableRowView()
            self.__song_views.append(song_view)
            self.__menu.addWidget(song_view)
            if self.__is_light_mode:
                song_view.apply_light_mode()
            else:
                song_view.apply_dark_mode()

    def __popular_info(self, song_view: SongTableRowView, song: Song, index: int) -> None:
        song_view.show_less()
        song_view.show()

        song_view.enable_choosing(False)
        song_view.set_default_cover(Images.DEFAULT_SONG_COVER)
        song_view.set_cover(song.get_cover())
        song_view.set_default_artist(song.get_artist())
        song_view.set_artist(song.get_artist())
        song_view.set_title(song.get_title())
        song_view.set_love_state(song.is_loved())
        song_view.set_length(song.get_length())
        song_view.set_onclick_play(lambda: self.__onclick_play_btn(index))
        song_view.set_onclick_love(lambda: self.__onclick_love_btn(index))
        song_view.set_onclick_add_to_playlist(lambda: self.__onclick_add_to_playlist_fn(index))
        song_view.set_onclick_remove_from_playlist(lambda: self.__onclick_remove_from_playlist_fn(index))
        song_view.set_on_edit_cover(lambda: self.__choose_cover_for_song_at(index))
        song_view.set_on_update_info(lambda title, artist: self.__onchange_title_fn(index, title, artist))
        song_view.set_on_delete(lambda: self.__confirm_delete_song(index))

    def __display_songs(self, songs: list[Song]) -> list[SongTableRowView]:
        total_display = len(songs)
        displaying_rows = self.__song_views[0:total_display]
        for i, song_view in enumerate(displaying_rows):
            self.__popular_info(song_view, songs[i], i)
        self.__menu.displayNFirst(total_display)
        return displaying_rows

    def load_choosing_playlist(self, songs: list[Song]) -> None:
        self.load_songs(songs)
        for i, song_view in enumerate(self.__song_views):
            song_view.enable_choosing(True)
            song_view.set_is_chosen(songs[i].is_loved())

    def enable_choosing_song(self, is_choosing: bool) -> None:
        for song in self.__song_views:
            song.enable_choosing(is_choosing)

    def __popular_info_into(self, song_view: SongTableRowView, song: Song, index: int) -> None:
        song_view.set_default_cover(Images.DEFAULT_SONG_COVER)
        song_view.set_cover(song.get_cover())
        song_view.set_default_artist(song.get_artist())
        song_view.set_artist(song.get_artist())
        song_view.set_title(song.get_title())
        song_view.set_love_state(song.is_loved())
        song_view.set_length(song.get_length())

        song_view.set_onclick_play(lambda: self.__onclick_play_btn(index))
        song_view.set_onclick_love(lambda: self.__onclick_love_btn(index))
        song_view.set_onclick_add_to_playlist(lambda: self.__onclick_add_to_playlist_fn(index))
        song_view.set_onclick_remove_from_playlist(lambda: self.__onclick_remove_from_playlist_fn(index))
        song_view.set_on_edit_cover(lambda: self.__choose_cover_for_song_at(index))
        song_view.set_on_update_info(lambda title, artist: self.__onchange_title_fn(index, title, artist))
        song_view.set_on_delete(lambda: self.__confirm_delete_song(index))
        song_view.enable_choosing(False)

    def select_song_at(self, index: int) -> None:
        self._scroll_to_item_at(index)

    def get_scrolling_song_index(self) -> int:
        return self.get_current_item_index()

    def get_song_at(self, index: int) -> SongTableRowView:
        return self.__song_views[index]

    def __remove_songs_in_range(self, start: int, end: int) -> None:
        for index in range(start, end):
            self.__song_views[index].clear_info()
