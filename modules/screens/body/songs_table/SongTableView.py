from typing import Optional, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from modules.helpers.types.Decorators import override, connector
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
    def set_on_keypress(self, fn: Callable[[str], int]) -> None:
        self._body.set_on_keypress(fn)

    def _add_song(self, title: str, artist: str, length: int, cover: bytes) -> None:
        new_song: SongTableRowView = self._body.add_new_song(title, artist, length, cover)
        if self.__is_dark_mode:
            new_song.apply_dark_mode()
        else:
            new_song.apply_light_mode()

    def _update_song_at(self, index: int, title: str, artist: str, length: int, cover: bytes) -> None:
        song: SongTableRowView = self._body.get_song_at(index)
        song.set_title(title)
        song.set_artist(artist)
        song.set_length(length)
        song.set_cover(cover)
