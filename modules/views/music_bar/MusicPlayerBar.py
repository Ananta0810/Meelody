from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QWidget

from modules.statics.view.Material import Images
from modules.views.music_bar.MusicPlayerLeftSide import MusicPlayerLeftSide
from modules.views.music_bar.MusicPlayerMiddle import MusicPlayerMiddle
from modules.views.music_bar.MusicPlayerRightSide import MusicPlayerRightSide


class MusicPlayerBar(QWidget):
    main_layout: QHBoxLayout
    left: MusicPlayerLeftSide
    middle: MusicPlayerMiddle
    right: MusicPlayerRightSide

    def __init__(self, parent: Optional["QWidget"] = None):
        super(MusicPlayerBar, self).__init__(parent)
        self._totalTime = 0
        self.setup_ui()

        self.left.set_default_title("Song Title")
        self.left.set_default_artist("Song Artist")
        self.left.set_title("Song Title")
        self.left.set_artist("Song Artist")
        self.middle.set_total_time(60)
        self.middle.set_playing_time(0)
        self.right.btn_loop.set_active(False)
        self.right.btn_shuffle.set_active(False)
        self.right.btn_love.set_active(False)

    def setup_ui(self) -> None:
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(20, 0, 20, 0)
        self.main_layout.setSpacing(0)

        self.left = MusicPlayerLeftSide()
        self.left.setContentsMargins(0, 0, 0, 0)
        self.left.setSpacing(12)
        self.left.set_default_cover(Images.DEFAULT_SONG_COVER)

        self.middle = MusicPlayerMiddle()
        self.middle.setContentsMargins(0, 0, 0, 0)
        self.middle.setSpacing(4)

        self.right = MusicPlayerRightSide()
        self.right.setContentsMargins(0, 0, 0, 0)
        self.right.setSpacing(8)

        self.main_layout.addLayout(self.left)
        self.main_layout.addLayout(self.middle)
        self.main_layout.addLayout(self.right)

    def apply_light_mode(self) -> None:
        self.left.apply_light_mode()
        self.middle.apply_light_mode()
        self.right.apply_light_mode()

    def apply_dark_mode(self) -> None:
        self.left.apply_dark_mode()
        self.middle.apply_dark_mode()
        self.right.apply_dark_mode()
