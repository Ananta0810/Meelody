from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget
from views.view import View

from .current_playlist.current_playlist import CurrentPlaylist
from .playlist_carousel.carousel import PlaylistCarousel


class HomeScreen(QScrollArea, View):
    def __init__(self, parent: Optional["QWidget"] = None):
        super(HomeScreen, self).__init__(parent)
        self.setupUi()

    def setupUi(self) -> None:
        self.setStyleSheet("background:transparent;border:none")
        self.inner = QWidget()
        self.setWidget(self.inner)
        self.mainLayout = QVBoxLayout(self.inner)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.playlistCarousel = PlaylistCarousel()
        self.playlistCarousel.setFixedHeight(360)
        self.playlistCarousel.setStyleSheet("background:transparent;border:none")
        self.playlistCarousel.main_layout.setContentsMargins(84, 0, 50, 0)

        self.currentPlaylist = CurrentPlaylist()
        self.currentPlaylist.setAlignment(Qt.AlignLeft)
        self.currentPlaylist.setContentsMargins(84, 50, 50, 0)
        self.currentPlaylist.setSpacing(50)

        self.mainLayout.addWidget(self.playlistCarousel)
        self.mainLayout.addLayout(self.currentPlaylist)

    def connectToControllers(self, controllers) -> None:
        self.playlistCarousel.connectToController(controllers.get("playlistCarousel"))
        self.currentPlaylist.songs.connectToController(controllers.get("playlistMenu"))

    def lightMode(self) -> None:
        self.playlistCarousel.lightMode()
        self.currentPlaylist.lightMode()
        return super().lightMode()

    def darkMode(self) -> None:
        self.playlistCarousel.darkMode()
        self.currentPlaylist.darkMode()
        return super().darkMode()
