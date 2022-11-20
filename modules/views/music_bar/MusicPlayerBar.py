from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QWidget

from modules.statics.view.Material import Images
from modules.views.music_bar.LeftSide import MusicPlayerLeftSide


class MusicPlayerBar(QWidget):
    main_layout: QHBoxLayout
    left: MusicPlayerLeftSide

    def __init__(self, parent: Optional["QWidget"] = None):
        super(MusicPlayerBar, self).__init__(parent)
        self._totalTime = 0
        self.setup_ui()

    def setup_ui(self) -> None:
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(40, 0, 40, 0)
        self.main_layout.setSpacing(0)

        self.left = MusicPlayerLeftSide()
        self.left.setContentsMargins(0, 0, 0, 0)
        self.left.setSpacing(12)
        self.left.set_default_cover(Images.DEFAULT_SONG_COVER)
        self.left.set_default_title("Song Title")
        self.left.set_default_artist("Song Artist")

        self.left.set_title("Song Title")
        self.left.set_artist("Song Artist")

        self.main_layout.addLayout(self.left)
        self.main_layout.addStretch(1)

    def apply_light_mode(self) -> None:
        self.left.apply_light_mode()

    def apply_dark_mode(self) -> None:
        self.left.apply_dark_mode()
