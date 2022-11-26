from typing import Optional

from PyQt5.QtGui import QShowEvent
from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout

from modules.helpers.types.Decorators import override
from modules.statics.view.Material import Backgrounds
from modules.views.ViewComponent import ViewComponent
from modules.views.body.CurrentPlaylistView import CurrentPlaylistView
from modules.views.body.PlaylistCarousel import PlaylistCarousel


class HomeBodyView(QScrollArea, ViewComponent):
    __inner: QWidget
    __main_layout: QVBoxLayout
    __playlist_carousel: PlaylistCarousel
    __current_playlist: CurrentPlaylistView

    def __init__(self, parent: Optional["QWidget"] = None):
        super(HomeBodyView, self).__init__(parent)
        self.__init_ui()

    def __init_ui(self) -> None:
        self.setStyleSheet(Backgrounds.TRANSPARENT.to_stylesheet())
        self.__inner = QWidget()
        self.setWidget(self.__inner)

        self.__main_layout = QVBoxLayout(self.__inner)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)
        self.__main_layout.setSpacing(50)

        self.__playlist_carousel = PlaylistCarousel()
        self.__playlist_carousel.setFixedHeight(360)
        self.__playlist_carousel.setStyleSheet(Backgrounds.TRANSPARENT.to_stylesheet())

        self.__current_playlist = CurrentPlaylistView()

        self.__main_layout.addWidget(self.__playlist_carousel)
        self.__main_layout.addWidget(self.__current_playlist)

    @override
    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self.__playlist_carousel.setContentsMargins(left, top, right, bottom)
        self.__current_playlist.setContentsMargins(left, top, right, bottom)

    @override
    def showEvent(self, a0: QShowEvent) -> None:
        self.__current_playlist.setFixedHeight(self.height())
        return super().showEvent(a0)

    @override
    def apply_light_mode(self) -> None:
        self.__playlist_carousel.apply_light_mode()
        self.__current_playlist.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.__playlist_carousel.apply_dark_mode()
        self.__current_playlist.apply_dark_mode()