from typing import Optional, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from modules.helpers.types.Decorators import override, connector
from modules.models.PlaylistSongs import PlaylistSongs
from modules.screens.AbstractScreen import BaseView
from modules.screens.body.songs_table.SongTableBodyView import SongTableBodyView
from modules.screens.body.songs_table.SongTableHeaderView import SongTableHeaderView
from modules.screens.body.songs_table.SongTableRowView import SongTableRowView


class SongTableView(QWidget, BaseView):
    __main_layout: QVBoxLayout
    __header: SongTableHeaderView
    __body: SongTableBodyView
    __is_dark_mode: bool = False

    def __init__(self, parent: Optional["QWidget"] = None) -> None:
        super().__init__(parent)
        self.__init_ui()
        self.__header.setText()

    def __init_ui(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.__main_layout = QVBoxLayout(self)
        self.__main_layout.setSpacing(4)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.__header = SongTableHeaderView()
        self.__header.setFixedHeight(48)

        self.__body = SongTableBodyView()

        self.__main_layout.addWidget(self.__header)
        self.__main_layout.addWidget(self.__body)

    @override
    def apply_light_mode(self) -> None:
        self.__is_dark_mode = False
        self.__header.apply_light_mode()
        self.__body.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.__is_dark_mode = True
        self.__header.apply_dark_mode()
        self.__body.apply_dark_mode()

    @connector
    def set_onclick_play(self, fn: Callable[[int], None]) -> None:
        self.__body.set_onclick_play(fn)

    @connector
    def set_on_keypress(self, fn: Callable[[str], int]) -> None:
        self.__body.set_on_keypress(fn)

    def select_song_at(self, index: int) -> None:
        self.__body.select_song_at(index)

    def load_songs(self, playlist: PlaylistSongs) -> None:
        for song in playlist.get_songs():
            new_song: SongTableRowView = self.__body.add_new_song(
                song.get_title(), song.get_artist(), song.get_length(), song.get_cover()
            )
            if self.__is_dark_mode:
                new_song.apply_dark_mode()
            else:
                new_song.apply_light_mode()
