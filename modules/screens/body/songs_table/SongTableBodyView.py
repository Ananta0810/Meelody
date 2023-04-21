from typing import Optional, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from modules.helpers.types.Decorators import override, connector
from modules.models.Song import Song
from modules.screens.AbstractScreen import BaseView
from modules.screens.body.songs_table.SongTableRowView import SongTableRowView
from modules.statics.view.Material import Images, Backgrounds
from modules.widgets.SmoothVerticalScrollArea import SmoothVerticalScrollArea


class SongTableBodyView(SmoothVerticalScrollArea, BaseView):
    __inner: QWidget
    __menu: QVBoxLayout

    __onclick_button_fn: Callable[[int], None]
    __onclick_love_fn: Callable[[int], None]
    __on_keypress_fn: Callable[[str], int]

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
            song.set_onclick_love(lambda: self._onclick_love_btn(index))

    def __onclick_play_btn(self, index: int) -> None:
        self.select_song_at(index)
        if self.__onclick_button_fn is not None:
            self.__onclick_button_fn(index)

    def _onclick_love_btn(self, index: int) -> None:
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
        song.show_less()
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
        return self.__menu.count()

    def add_new_song(self, song: Song) -> SongTableRowView:
        songView = self.__addSong(song)
        index: int = len(self._songs)
        self._songs.append(songView)
        self.__menu.addWidget(songView)
        songView.set_onclick_play(lambda: self.__onclick_play_btn(index))
        songView.set_onclick_love(lambda: self._onclick_love_btn(index))

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
