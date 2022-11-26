from typing import Optional

from PyQt5.QtGui import QShowEvent
from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout

from modules.helpers.types.Decorators import override
from modules.statics.view.Material import Backgrounds
from modules.views.body.CurrentPlaylistView import CurrentPlaylistView
from modules.views.body.PlaylistCarousel import PlaylistCarousel


class HomeBodyView(QScrollArea):
    inner: QWidget
    main_layout: QVBoxLayout
    playlist_carousel: PlaylistCarousel
    current_playlist: CurrentPlaylistView

    def __init__(self, parent: Optional["QWidget"] = None):
        super(HomeBodyView, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.setStyleSheet(Backgrounds.TRANSPARENT.to_stylesheet())
        self.inner = QWidget()
        self.setWidget(self.inner)

        self.main_layout = QVBoxLayout(self.inner)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(50)

        self.playlist_carousel = PlaylistCarousel()
        self.playlist_carousel.setFixedHeight(360)
        self.playlist_carousel.setStyleSheet(Backgrounds.TRANSPARENT.to_stylesheet())

        self.current_playlist = CurrentPlaylistView()

        self.main_layout.addWidget(self.playlist_carousel)
        self.main_layout.addWidget(self.current_playlist)

    @override
    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self.playlist_carousel.setContentsMargins(left, top, right, bottom)
        self.current_playlist.setContentsMargins(left, top, right, bottom)

    @override
    def showEvent(self, a0: QShowEvent) -> None:
        self.current_playlist.setFixedHeight(self.height())
        return super().showEvent(a0)

    def apply_light_mode(self) -> None:
        self.playlist_carousel.apply_light_mode()
        self.current_playlist.apply_light_mode()

    def apply_dark_mode(self) -> None:
        self.playlist_carousel.apply_dark_mode()
        self.current_playlist.apply_dark_mode()