from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from modules.helpers.types.Decorators import override
from modules.models.view.Background import Background
from modules.screens.music_bar.MusicPlayerControl import MusicPlayerControl
from modules.statics.view.Material import ColorBoxes
from modules.screens.AbstractScreen import BaseView
from modules.screens.body.HomeBodyView import HomeBodyView
from modules.screens.music_bar.MusicPlayerBarView import MusicPlayerBarView
from modules.widgets.FramelessWindow import FramelessWindow


class MainWindowView(FramelessWindow, BaseView):
    __body: HomeBodyView
    __music_player: MusicPlayerControl

    def __init__(self, parent: Optional["QWidget"] = None, width: int = 1280, height: int = 720):
        super(MainWindowView, self).__init__(parent)
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.__init_ui()

    def __init_ui(self) -> None:
        self.__body = HomeBodyView()
        self.__body.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__body.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__body.setWidgetResizable(True)
        self.__body.setContentsMargins(72, 0, 50, 0)

        self.__music_player = MusicPlayerControl()
        self.__music_player.setFixedHeight(96)
        self.__music_player.setObjectName("musicPlayer")

        self.addWidget(self.__body)
        self.addWidget(self.__music_player, alignment=Qt.AlignBottom)

    @override
    def apply_light_mode(self) -> None:
        super().apply_light_mode()
        self.setStyleSheet(Background(border_radius=24, color=ColorBoxes.WHITE).to_stylesheet())
        self.__body.apply_light_mode()
        self.__music_player.setStyleSheet("QWidget#musicPlayer{border-top: 1px solid #eaeaea};border-radius:0px")
        self.__music_player.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        super().apply_dark_mode()
        self.setStyleSheet(Background(border_radius=24, color=ColorBoxes.BLACK).to_stylesheet())
        self.__body.apply_dark_mode()
        self.__music_player.setStyleSheet("QWidget#musicPlayer{border-top: 1px solid #202020};border-radius:0px")
        self.__music_player.apply_dark_mode()
