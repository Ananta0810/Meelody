from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from modules.helpers.types.Decorators import override
from modules.models.view.Background import Background
from modules.screens.AbstractScreen import BaseView
from modules.screens.body.HomeBodyView import HomeBodyView
from modules.screens.music_bar.MusicPlayerControl import MusicPlayerControl
from modules.statics.view.Material import ColorBoxes
from modules.widgets import Dialogs
from modules.widgets.Windows import FramelessWindow


class MainWindowView(FramelessWindow, BaseView):
    _body: HomeBodyView
    _music_player: MusicPlayerControl

    def __init__(self, parent: Optional["QWidget"] = None, width: int = 1280, height: int = 720):
        super(MainWindowView, self).__init__(parent)
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.__init_ui()
        Dialogs.Dialogs.get_instance().set_window(self)

    def __init_ui(self) -> None:
        self._body = HomeBodyView()
        self._body.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._body.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._body.setWidgetResizable(True)
        self._body.setContentsMargins(72, 0, 50, 0)

        self._music_player = MusicPlayerControl()
        self._music_player.setFixedHeight(96)
        self._music_player.setObjectName("musicPlayer")

        self.addWidget(self._body)
        self.addWidget(self._music_player, alignment=Qt.AlignBottom)

    @override
    def apply_light_mode(self) -> None:
        super().apply_light_mode()
        self.setStyleSheet(Background(border_radius=32, color=ColorBoxes.WHITE).to_stylesheet())
        self._body.apply_light_mode()
        self._music_player.setStyleSheet("QWidget#musicPlayer{border-top: 1px solid #eaeaea};border-radius:0px")
        self._music_player.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        super().apply_dark_mode()
        self.setStyleSheet(Background(border_radius=32, color=ColorBoxes.BLACK).to_stylesheet())
        self._body.apply_dark_mode()
        self._music_player.setStyleSheet("QWidget#musicPlayer{border-top: 1px solid #202020};border-radius:0px")
        self._music_player.apply_dark_mode()

    def _set_default_playlist_cover(self, cover: bytes):
        self._body.set_default_playlist_cover(cover)
