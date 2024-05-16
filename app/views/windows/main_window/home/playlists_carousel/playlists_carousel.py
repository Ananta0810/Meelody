from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QWidget

from app.common.models import Playlist
from app.common.others import appCenter, translator
from app.common.statics.qt import Icons
from app.common.statics.styles import Colors
from app.common.statics.styles import Paddings
from app.components.asyncs import ChunksConsumer
from app.components.base import Component
from app.components.buttons import ButtonFactory
from app.components.widgets import StyleWidget, FlexBox
from app.utils.base import Lists
from .new_playlist_dialog import NewPlaylistDialog
from .playlist_cards import LibraryPlaylistCard, FavouritePlaylistCard, UserPlaylistCard


class PlaylistsCarousel(QScrollArea, Component):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._initComponent()

        self.__userPlaylistIds: list[str] = []

    def _createUI(self):
        self.setWidgetResizable(True)
        self.setClassName("bg-none border-none")
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._inner = StyleWidget()
        self._inner.setClassName("bg-none")
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

        self._addPlaylistBtn = ButtonFactory.createIconButton(size=Icons.large, padding=Paddings.relative67, parent=self._newPlaylistCard)
        self._addPlaylistBtn.move(self._newPlaylistCard.rect().center() - self._addPlaylistBtn.rect().center())
        self._addPlaylistBtn.setLightModeIcon(Icons.add.withColor(Colors.primary))
        self._addPlaylistBtn.setDarkModeIcon(Icons.add.withColor(Colors.white))
        self._addPlaylistBtn.setClassName("rounded-full bg-primary-12 hover:bg-primary-25 dark:bg-white-12 dark:hover:bg-white-20")

        self._mainLayout = FlexBox(self._inner)
        self._mainLayout.setSpacing(32)

        self._mainLayout.addWidget(self._playlistLibrary)
        self._mainLayout.addWidget(self._playlistFavourites)
        self._mainLayout.addWidget(self._userPlaylists)
        self._mainLayout.addWidget(self._newPlaylistCard)
        self._mainLayout.addStretch()

    def translateUI(self) -> None:
        self._addPlaylistBtn.setToolTip(translator.translate("PLAYLIST_CAROUSEL.NEW_PLAYLIST_BTN"))

    def _connectSignalSlots(self) -> None:
        appCenter.loaded.connect(lambda: self.setPlaylists(appCenter.playlists.items()))
        appCenter.playlists.changed.connect(lambda playlists: self.setPlaylists(playlists))
        self._addPlaylistBtn.clicked.connect(lambda: self.__openNewPlaylistDialog())

    def wheelEvent(self, event):
        delta = event.angleDelta().y()

        xPosition = self.horizontalScrollBar().value()
        self.horizontalScrollBar().setValue(xPosition - delta)

    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self._mainLayout.setContentsMargins(left, top, right, bottom)

    def setPlaylists(self, playlists: list[Playlist]) -> None:
        if not appCenter.isLoaded:
            appCenter.loaded.connect(lambda: self.setPlaylists(playlists))
            return

        totalPlaylists = len(playlists)
        if totalPlaylists != 0:
            self._userPlaylists.show()

        oldPlaylistIds = self.__userPlaylistIds
        newPlaylistIds = [playlist.getInfo().getId() for playlist in playlists]

        self.__userPlaylistIds = newPlaylistIds

        addedPlaylistIds = Lists.itemsInRightOnly(oldPlaylistIds, newPlaylistIds)
        removedPlaylistIds = Lists.itemsInLeftOnly(oldPlaylistIds, newPlaylistIds)

        if len(addedPlaylistIds) > 0:
            self._userPlaylists.setMinimumWidth(totalPlaylists * 256 + (totalPlaylists - 1) * self._userPlaylistsLayout.spacing())
            newPlaylistDict: dict[str, Playlist] = {playlist.getInfo().getId(): playlist for playlist in playlists}

            chunks = ChunksConsumer(items=addedPlaylistIds, size=3, parent=self)
            chunks.finished.connect(lambda: self.__adaptCovers())
            chunks.forEach(lambda playlistId, index: self.__addPlaylist(newPlaylistDict[playlistId]), delay=10)

        if len(removedPlaylistIds) > 0:
            indexesToRemove = [index for index, playlistId in enumerate(oldPlaylistIds) if playlistId in removedPlaylistIds]
            self._userPlaylistsLayout.removeAtIndexes(indexesToRemove)
            self._userPlaylists.setMinimumWidth(totalPlaylists * 256 + (totalPlaylists - 1) * self._userPlaylistsLayout.spacing())

    def __addPlaylist(self, playlist: Playlist) -> None:
        userPlaylist = UserPlaylistCard(playlist)
        self._userPlaylistsLayout.addWidget(userPlaylist)

    def __adaptCovers(self) -> None:
        chunks = ChunksConsumer(items=self._userPlaylistsLayout.widgets(), size=1, parent=self)
        chunks.forEach(lambda playlist, index: playlist.adaptTitleColorToCover(), delay=10)

    @staticmethod
    def __openNewPlaylistDialog() -> None:
        NewPlaylistDialog().show()
