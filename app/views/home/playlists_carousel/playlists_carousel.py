from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QWidget, QHBoxLayout

from app.common.models import Playlist
from app.common.others import appCenter
from app.components.base import Component, Factory
from app.components.widgets import StyleWidget
from app.helpers.stylesheets import Paddings, Colors
from app.resource.qt import Icons
from .playlist_card import LibraryPlaylistCard, FavouritePlaylistCard, UserPlaylistCard


class PlaylistsCarousel(QScrollArea, Component):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._initComponent()

    def _createUI(self):
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self._inner = QWidget()
        self.setWidget(self._inner)

        # =================Library=================
        self._playlistLibrary = LibraryPlaylistCard()
        self._playlistFavourites = FavouritePlaylistCard()

        self._userPlaylists = QWidget()
        self._userPlaylistsLayout = QHBoxLayout(self._userPlaylists)
        self._userPlaylistsLayout.setAlignment(Qt.AlignLeft)
        self._userPlaylistsLayout.setSpacing(32)
        self._userPlaylistsLayout.setContentsMargins(0, 0, 0, 0)

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

        self._main_layout.addWidget(self._playlistLibrary)
        self._main_layout.addWidget(self._playlistFavourites)
        self._main_layout.addWidget(self._userPlaylists)
        self._main_layout.addWidget(self._newPlaylistCard)
        self._main_layout.addStretch()

    def _connectSignalSlots(self) -> None:
        appCenter.playlistsChanged.connect(lambda playlists: self.setPlaylists(playlists))

    def wheelEvent(self, event):
        delta = event.angleDelta().y()

        xPosition = self.horizontalScrollBar().value()
        self.horizontalScrollBar().setValue(xPosition - delta)

    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self._main_layout.setContentsMargins(left, top, right, bottom)

    def setPlaylists(self, playlists: list[Playlist]) -> None:
        pass
        for playlist in playlists:
            userPlaylist = UserPlaylistCard(playlist)
            self._userPlaylistsLayout.addWidget(userPlaylist)
