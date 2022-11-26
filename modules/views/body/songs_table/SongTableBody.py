from typing import Optional

from PyQt5.QtCore import pyqtSignal, QEvent, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from modules.helpers.types.Decorators import override
from modules.statics.view.Material import Images, Backgrounds
from modules.views.ViewComponent import ViewComponent
from modules.views.body.songs_table.SongTableRow import SongTableRow
from modules.widgets.SmoothVerticalScrollArea import SmoothVerticalScrollArea


class SongTableBody(SmoothVerticalScrollArea, ViewComponent):
    keyPressed = pyqtSignal(QEvent)

    __inner: QWidget
    __menu: QVBoxLayout

    def __init__(self, parent: Optional["QWidget"] = None):
        super(SongTableBody, self).__init__(parent)
        self.start: int = 0
        self.last: int = 6
        self._songs: list[SongTableRow] = []
        self._current_song_index: list[int] = []
        self.setup_ui()

    def setup_ui(self):
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

    def display_song_info_at_index(self, index: int, cover: bytes, title: str, artist: str, length: float) -> None:
        song = self.__get_song_at(index)
        song.show()
        song.show_less()
        song.set_cover(cover)
        song.set_title(title)
        song.set_artist(artist)
        song.set_length(length)

    def set_song_cover_at_index(self, index: int, cover: bytes) -> None:
        self.__get_song_at(index).set_cover(cover)

    def set_song_title_at_index(self, index: int, title: str) -> None:
        self.__get_song_at(index).set_title(title)

    def set_song_artist_at_index(self, index: int, artist: str) -> None:
        self.__get_song_at(index).set_artist(artist)

    def set_song_length_at_index(self, index: int, length: float) -> None:
        self.__get_song_at(index).set_length(length)

    def set_song_love_state_at_index(self, index: int, state: bool) -> None:
        self.__get_song_at(index).set_love_state(state)

    def get_total_songs(self) -> int:
        return self.__menu.count()

    def __get_song_at(self, index: int) -> SongTableRow:
        return self._songs[index]

    def add_new_song(self, title: str = "Title", artist: str = "Artist", length: int = 0) -> None:
        index = self.get_total_songs()
        song = self.__addSong(title, artist, length)
        self._songs.append(song)
        self.__menu.addWidget(song)

    def __remove_songs_in_range(self, start: int, end: int) -> None:
        for index in range(start, end):
            self.__menu.itemAt(index).widget().deleteLater()

    def __addSong(self, title: str, artist: str, length: int) -> SongTableRow:
        song = SongTableRow()
        song.set_default_cover(Images.DEFAULT_SONG_COVER)
        song.set_default_artist(artist)
        song.set_artist(artist)
        song.set_title(title)
        song.set_length(length)
        self.__menu.addWidget(song)
        return song
