from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QWidget, QHBoxLayout

from app.components.base import Component, Factory
from app.components.widgets import StyleWidget
from app.helpers.stylesheets import Paddings, Colors
from app.resource.qt import Icons
from .playlist_card import LibraryPlaylistCard


class PlaylistsCarousel(QScrollArea, Component):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._initComponent()
        # self._playlistFavourites.setTitle("Favourites")

    def _createUI(self):
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self._inner = QWidget()
        self.setWidget(self._inner)

        # =================Library=================
        self._playlistLibrary = LibraryPlaylistCard()
        # self._playlistFavourites = self.__create_favourite_playlist()

        self._defaultPlaylists = QHBoxLayout()
        self._defaultPlaylists.setAlignment(Qt.AlignLeft)
        self._defaultPlaylists.addWidget(self._playlistLibrary)
        # self._defaultPlaylists.addWidget(self._playlistFavourites)

        self._userPlaylists = QHBoxLayout()
        self._userPlaylists.setAlignment(Qt.AlignLeft)

        # =================New playlist=================
        self._newPlaylistCard = StyleWidget()
        self._newPlaylistCard.setFixedSize(256, 320)
        self._newPlaylistCard.setClassName("rounded-24 bg-primary-12")

        self._btnAddPlaylist = Factory.createIconButton(size=Icons.LARGE, padding=Paddings.RELATIVE_67, parent=self._newPlaylistCard)
        self._btnAddPlaylist.move(self._newPlaylistCard.rect().center() - self._btnAddPlaylist.rect().center())
        self._btnAddPlaylist.setLightModeIcon(Icons.ADD.withColor(Colors.PRIMARY))
        self._btnAddPlaylist.setClassName("hover:bg-primary-25 rounded-full")

        self._main_layout = QHBoxLayout(self._inner)
        self._main_layout.setAlignment(Qt.AlignLeft)
        self._main_layout.setSpacing(32)
        self._main_layout.setContentsMargins(0, 0, 0, 0)

        self._main_layout.addLayout(self._defaultPlaylists)
        self._main_layout.addLayout(self._userPlaylists)
        self._main_layout.addWidget(self._newPlaylistCard)
        self._main_layout.addStretch()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()

        xPosition = self.horizontalScrollBar().value()
        self.horizontalScrollBar().setValue(xPosition - delta)

    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self._main_layout.setContentsMargins(left, top, right, bottom)
