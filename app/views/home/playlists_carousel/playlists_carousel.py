from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QWidget, QHBoxLayout

from app.common.models import Playlist
from app.common.others import appCenter
from app.components.base import Component, Factory
from app.components.widgets import StyleWidget, FlexBox
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
        self._userPlaylistsLayout = FlexBox(self._userPlaylists)
        self._userPlaylistsLayout.setAlignment(Qt.AlignLeft)
        self._userPlaylistsLayout.setSpacing(32)
        self._userPlaylists.hide()

        # =================New playlist=================
        self._newPlaylistCard = StyleWidget()
        self._newPlaylistCard.setFixedSize(256, 320)
        self._newPlaylistCard.setClassName("rounded-24 bg-primary-12 dark:bg-white-12")

        self._addPlaylistBtn = Factory.createIconButton(size=Icons.LARGE, padding=Paddings.RELATIVE_67, parent=self._newPlaylistCard)
        self._addPlaylistBtn.move(self._newPlaylistCard.rect().center() - self._addPlaylistBtn.rect().center())
        self._addPlaylistBtn.setLightModeIcon(Icons.ADD.withColor(Colors.PRIMARY))
        self._addPlaylistBtn.setDarkModeIcon(Icons.ADD.withColor(Colors.WHITE))
        self._addPlaylistBtn.setClassName("rounded-full bg-primary-12 hover:bg-primary-25 dark:bg-white-12 dark:hover:bg-white-20")

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
        appCenter.playlists.changed.connect(self.setPlaylists)
        self._addPlaylistBtn.clicked.connect(self.__createEmptyPlaylist)

    def wheelEvent(self, event):
        delta = event.angleDelta().y()

        xPosition = self.horizontalScrollBar().value()
        self.horizontalScrollBar().setValue(xPosition - delta)

    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self._main_layout.setContentsMargins(left, top, right, bottom)

    def setPlaylists(self, playlists: list[Playlist]) -> None:
        if len(playlists) != 0:
            self._userPlaylists.show()

        self._userPlaylistsLayout.clear()
        for playlist in playlists:
            userPlaylist = UserPlaylistCard(playlist)
            self._userPlaylistsLayout.addWidget(userPlaylist)

    def __createEmptyPlaylist(self) -> None:
        playlist = Playlist(Playlist.Info(), Playlist.Songs())
        appCenter.playlists.append(playlist)
