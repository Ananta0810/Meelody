from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QWidget

from modules.helpers.types.Decorators import override
from modules.statics.view.Material import Images
from modules.views.ViewComponent import ViewComponent
from modules.views.music_bar.MusicPlayerLeftSide import MusicPlayerLeftSide
from modules.views.music_bar.MusicPlayerMiddle import MusicPlayerMiddle
from modules.views.music_bar.MusicPlayerRightSide import MusicPlayerRightSide


class MusicPlayerBar(QWidget, ViewComponent):
    __main_layout: QHBoxLayout
    __left: MusicPlayerLeftSide
    __middle: MusicPlayerMiddle
    __right: MusicPlayerRightSide

    def __init__(self, parent: Optional["QWidget"] = None):
        super(MusicPlayerBar, self).__init__(parent)
        self._totalTime = 0
        self.__init_ui()

        self.__left.set_default_title("Song Title")
        self.__left.set_default_artist("Song Artist")
        self.__left.set_title("Song Title")
        self.__left.set_artist("Song Artist")
        self.__middle.set_total_time(60)
        self.__middle.set_playing_time(0)

    def __init_ui(self) -> None:
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.__main_layout = QHBoxLayout(self)
        self.__main_layout.setContentsMargins(20, 0, 20, 0)
        self.__main_layout.setSpacing(0)

        self.__left = MusicPlayerLeftSide()
        self.__left.setContentsMargins(0, 0, 0, 0)
        self.__left.setSpacing(12)
        self.__left.set_default_cover(Images.DEFAULT_SONG_COVER)

        self.__middle = MusicPlayerMiddle()
        self.__middle.setContentsMargins(0, 0, 0, 0)
        self.__middle.setSpacing(4)

        self.__right = MusicPlayerRightSide()
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
