from typing import Optional, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFileDialog

from modules.helpers.types.Decorators import override, connector
from modules.models.Song import Song
from modules.screens.AbstractScreen import BaseView
from modules.screens.body.songs_table.SongTableRowView import SongTableRowView, RenameSongDialog
from modules.statics.view.Material import Images, Backgrounds
from modules.widgets.ScrollAreas import SmoothVerticalScrollArea


class SongTableBodyView(SmoothVerticalScrollArea, BaseView):
    __inner: QWidget
    __menu: QVBoxLayout

    __onclick_button_fn: Callable[[int], None] = None
    __onclick_love_fn: Callable[[int], None] = None
    __onclick_add_to_playlist_fn: Callable[[int], None] = None
    __onclick_remove_from_playlist_fn: Callable[[int], None] = None
    __onchange_cover_fn: Callable[[int, str], None] = None
    __onchange_title_fn: Callable[[int, str], bool] = None
    __on_delete_fn: Callable[[int], None] = None
    __on_keypress_fn: Callable[[str], int] = None

    def __init__(self, parent: Optional["QWidget"] = None):
        super(SongTableBodyView, self).__init__(parent)
        self.start: int = 0
        self.last: int = 6
        self._songs: list[SongTableRowView] = []
        self._current_song_index: list[int] = []
        self.__init_ui()

    def __init_ui(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.set_item_height(104)

        self.__inner = QWidget(self)
        self.setWidget(self.__inner)
        self.__menu = QVBoxLayout(self.__inner)
        self.__menu.setAlignment(Qt.AlignTop)
        self.__menu.setSpacing(0)
        self.__menu.setContentsMargins(8, 0, 8, 8)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    @override
    def apply_light_mode(self) -> None:
        self.setStyleSheet(SmoothVerticalScrollArea.build_style(background=Backgrounds.CIRCLE_PRIMARY))
        for song in self._songs:
            song.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.setStyleSheet(SmoothVerticalScrollArea.build_style(background=Backgrounds.CIRCLE_PRIMARY))
        for song in self._songs:
            song.apply_dark_mode()

    @connector
    def set_onclick_play(self, fn: Callable[[int], None]) -> None:
        self.__onclick_button_fn = fn
        for index, song in enumerate(self._songs):
            song.set_onclick_play(lambda: self.__onclick_play_btn(index))

    @connector
    def set_onclick_love(self, fn: Callable[[int], None]) -> None:
        self.__onclick_love_fn = fn
        for index, song in enumerate(self._songs):
            song.set_onclick_love(lambda: self.__onclick_love_btn(index))

    @connector
    def set_onclick_add_to_playlist(self, fn: Callable[[int], None]) -> None:
        self.__onclick_add_to_playlist_fn = fn
        for index, song in enumerate(self._songs):
            song.set_onclick_add_to_playlist(lambda: self.__onclick_add_to_playlist_fn(index))

    @connector
    def set_onclick_remove_from_playlist(self, fn: Callable[[int], None]) -> None:
        self.__onclick_remove_from_playlist_fn = fn
        for index, song in enumerate(self._songs):
            song.set_onclick_remove_from_playlist(lambda: self.__onclick_remove_from_playlist_fn(index))

    @connector
    def set_onchange_song_cover(self, fn: Callable[[int, str], None]) -> None:
        self.__onchange_cover_fn = fn
        for index, song in enumerate(self._songs):
            song.set_on_edit_cover(lambda: self.__choose_cover_for_song_at(index))

    @connector
    def set_on_delete_song(self, fn: Callable[[int], None]) -> None:
        self.__on_delete_fn = fn
        for index, song in enumerate(self._songs):
            song.set_on_delete(lambda: fn(index))

    @connector
    def set_onchange_song_title(self, fn: Callable[[int, str], bool]) -> None:
        self.__onchange_title_fn = fn
        for index, song in enumerate(self._songs):
            song.set_on_edit_title(lambda: self.__rename_title_for_song_at(index, song.get_title()))

    def __choose_cover_for_song_at(self, index: int) -> None:
        path = QFileDialog.getOpenFileName(self, filter="JPEG, PNG (*.JPEG *.jpeg *.JPG *.jpg *.JPE *.jpe)")[0]
        if path is not None and path != '':
            self.__onchange_cover_fn(index, path)

    def __rename_title_for_song_at(self, index: int, title: str) -> None:
        RenameSongDialog(
            "Rename song",
            onclick_accept_fn=lambda title: self.__onchange_title_fn(index, title)
        ).with_song_title(title).exec()

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
            self._scroll_to_item_at(index)
        except ValueError:
            pass

    def display_song_info_at_index(self, index: int, cover: bytes, title: str, artist: str, length: float) -> None:
        song = self.get_song_at(index)
        song.show()
        song.set_cover(cover)
        song.set_title(title)
        song.set_artist(artist)
        song.set_length(length)

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
        return len(self._songs)

    def load_songs(self, songs: list[Song]) -> list[SongTableRowView]:
        self.clear_table()
        return [self.add_new_song(song) for song in songs]

    def load_choosing_playlist(self, songs: list[Song]) -> list[SongTableRowView]:
        self.clear_table()
        result = []
        for song in songs:
            song_view = self.add_new_song(song)
            song_view.set_is_choosing(song.is_loved())
            song_view.enable_choosing(True)
            result.append(song_view)
        return result

    def enable_choosing_song(self, is_choosing: bool) -> None:
        for song in self._songs:
            song.enable_choosing(is_choosing)

    def clear_table(self):
        self.__remove_songs_in_range(0, self.get_total_songs())
        self._songs.clear()

    def add_new_song(self, song: Song) -> SongTableRowView:
        songView = self.__addSong(song)
        index: int = len(self._songs)
        songView.set_onclick_play(lambda: self.__onclick_play_btn(index))
        songView.set_onclick_love(lambda: self.__onclick_love_btn(index))
        songView.set_onclick_add_to_playlist(lambda: self.__onclick_add_to_playlist_fn(index))
        songView.set_onclick_remove_from_playlist(lambda: self.__onclick_remove_from_playlist_fn(index))
        songView.set_on_edit_cover(lambda: self.__choose_cover_for_song_at(index))
        songView.set_on_edit_title(lambda: self.__rename_title_for_song_at(index, song.get_title()))
        songView.set_on_delete(lambda: self.__on_delete_fn(index))

        songView.enable_choosing(False)

        self._songs.append(songView)
        self.__menu.addWidget(songView)
        return songView

    def select_song_at(self, index: int) -> None:
        self._scroll_to_item_at(index)

    def get_song_at(self, index: int) -> SongTableRowView:
        return self._songs[index]

    def __remove_songs_in_range(self, start: int, end: int) -> None:
        for index in range(start, end):
            self.__menu.itemAt(index).widget().deleteLater()

    def __addSong(self, song: Song) -> SongTableRowView:
        song_view = SongTableRowView()
        song_view.set_default_cover(Images.DEFAULT_SONG_COVER)
        song_view.set_cover(song.get_cover())
        song_view.set_default_artist(song.get_artist())
        song_view.set_artist(song.get_artist())
        song_view.set_title(song.get_title())
        song_view.set_love_state(song.is_loved())
        song_view.set_length(song.get_length())
        self.__menu.addWidget(song_view)
        return song_view
