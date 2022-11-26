from typing import Optional

from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from modules.models.view.Background import Background
from modules.statics.view.Material import ColorBoxes
from modules.views.body.HomeBodyView import HomeBodyView
from modules.views.music_bar.MusicPlayerBar import MusicPlayerBar
from modules.widgets.IconButton import IconButton
from modules.widgets.windows.FramelessWindow import FramelessWindow


class MainWindowView(FramelessWindow):
    music_player: MusicPlayerBar
    main_layout: QVBoxLayout
    home_screen: QWidget
    title_bar: QHBoxLayout
    background: QWidget
    close_btn: IconButton
    minimize_btn: IconButton
    body: HomeBodyView

    def __init__(self, parent: Optional["QWidget"] = None, width: int = 1280, height: int = 720):
        super(MainWindowView, self).__init__(parent)
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.__init_ui()

    def __init_ui(self) -> None:
        self.body = HomeBodyView()
        self.body.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.body.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.body.setWidgetResizable(True)
        self.body.setContentsMargins(72, 0, 50, 0)

        self.music_player = MusicPlayerBar()
        self.music_player.setFixedHeight(96)
        self.music_player.setObjectName("musicPlayer")

        self.addWidget(self.body)
        self.addWidget(self.music_player, alignment=Qt.AlignBottom)
        QMetaObject.connectSlotsByName(self)

    def apply_light_mode(self) -> None:
        super().apply_light_mode()
        self.setStyleSheet(Background(border_radius=24, color=ColorBoxes.WHITE).to_stylesheet())
        self.body.apply_light_mode()
        self.music_player.setStyleSheet("QWidget#musicPlayer{border-top: 1px solid #eaeaea};border-radius:0px")
        self.music_player.apply_light_mode()

    def apply_dark_mode(self) -> None:
        super().apply_dark_mode()
        self.setStyleSheet(Background(border_radius=24, color=ColorBoxes.BLACK).to_stylesheet())
        self.body.apply_dark_mode()
        self.music_player.setStyleSheet("QWidget#musicPlayer{border-top: 1px solid #202020};border-radius:0px")
        self.music_player.apply_dark_mode()
