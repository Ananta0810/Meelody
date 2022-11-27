from typing import Optional, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QWidget

from modules.helpers.types.Decorators import override, connector
from modules.statics.view.Material import Images
from modules.screens.AbstractScreen import BaseView
from modules.screens.music_bar.MusicPlayerLeftSideView import MusicPlayerLeftSideView
from modules.screens.music_bar.MusicPlayerMiddleView import MusicPlayerMiddleView
from modules.screens.music_bar.MusicPlayerRightSideView import MusicPlayerRightSideView


class MusicPlayerBarView(QWidget, BaseView):
    __main_layout: QHBoxLayout
    __left: MusicPlayerLeftSideView
    __middle: MusicPlayerMiddleView
    __right: MusicPlayerRightSideView

    def __init__(self, parent: Optional["QWidget"] = None):
        super(MusicPlayerBarView, self).__init__(parent)
        self._totalTime = 0
        self.__init_ui()

    def __init_ui(self) -> None:
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.__main_layout = QHBoxLayout(self)
        self.__main_layout.setContentsMargins(20, 0, 20, 0)
        self.__main_layout.setSpacing(0)

        self.__left = MusicPlayerLeftSideView()
        self.__left.setContentsMargins(0, 0, 0, 0)
        self.__left.setSpacing(12)
        self.__left.set_default_cover(Images.DEFAULT_SONG_COVER)

        self.__middle = MusicPlayerMiddleView()
        self.__middle.setContentsMargins(0, 0, 0, 0)
        self.__middle.setSpacing(4)

        self.__right = MusicPlayerRightSideView()
        self.__right.setContentsMargins(0, 0, 0, 0)
        self.__right.setSpacing(8)

        self.__main_layout.addLayout(self.__left)
        self.__main_layout.addLayout(self.__middle)
        self.__main_layout.addLayout(self.__right)

    @override
    def apply_light_mode(self) -> None:
        self.__left.apply_light_mode()
        self.__middle.apply_light_mode()
        self.__right.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.__left.apply_dark_mode()
        self.__middle.apply_dark_mode()
        self.__right.apply_dark_mode()

    @connector
    def _set_onclick_prev_song(self, fn: callable) -> None:
        self.__left.set_onclick_prev_song(fn)

    @connector
    def _set_onclick_play_song(self, fn: callable) -> None:
        self.__left.set_onclick_play_song(fn)

    @connector
    def _set_onclick_pause_song(self, fn: callable) -> None:
        self.__left.set_onclick_pause_song(fn)

    @connector
    def _set_onclick_next_song(self, fn: callable) -> None:
        self.__left.set_onclick_next_song(fn)

    @connector
    def _set_onchange_playing_time(self, fn: Callable[[float], None]):
        self.__middle.set_onchange_playing_time(fn)

    @connector
    def _set_onclick_loop(self, fn: callable) -> None:
        self.__right.set_onclick_loop(fn)

    @connector
    def _set_onclick_shuffle(self, fn: callable) -> None:
        self.__right.set_onclick_shuffle(fn)

    @connector
    def _set_onclick_love(self, fn: callable) -> None:
        self.__right.set_onclick_love(fn)

    @connector
    def _set_onchange_volume(self, fn: Callable[[int], None]) -> None:
        self.__right.set_onchange_volume(fn)

    def set_playing_time(self, time: float) -> None:
        self.__middle.set_playing_time(time)

    def set_total_time(self, time: float) -> None:
        self.__middle.set_total_time(time)

    def set_is_playing(self, enable: bool) -> None:
        return self.__left.set_is_playing(enable)

    def set_loop(self, enable: bool) -> None:
        return self.__right.set_loop(enable)

    def set_shuffle(self, enable: bool) -> None:
        return self.__right.set_shuffle(enable)

    def set_love_state(self, enable: bool) -> None:
        return self.__right.set_love_state(enable)

    def is_playing(self) -> bool:
        return self.__left.is_playing()

    def is_looping(self) -> bool:
        return self.__right.is_looping()

    def is_shuffle(self) -> bool:
        return self.__right.is_shuffle()

    def display_song_info(
        self, cover: bytes = None, title: str = None, artist: str = None, love_state: bool = False
    ) -> None:
        self.__left.set_cover(cover)
        self.__left.set_title(title)
        self.__left.set_artist(artist)
        self.__right.set_love_state(love_state)
