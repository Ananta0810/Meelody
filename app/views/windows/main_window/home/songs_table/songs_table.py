from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from app.common.models import Playlist
from app.common.others import appCenter, translator
from app.common.statics.qt import Cursors, Images
from app.components.base import FontFactory
from app.components.images import Cover
from app.components.labels import Label
from app.components.widgets import ExtendableStyleWidget, Box
from app.utils.qt import Widgets
from app.views.windows.main_window.home.songs_table.songs_menu import SongsMenu
from app.views.windows.main_window.home.songs_table.songs_table_header import SongsTableHeader


class SongsTable(ExtendableStyleWidget):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        self.__currentPlaylist: Optional[Playlist] = None

        super().__init__(parent)
        self._initComponent()

    def _createUI(self) -> None:
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._mainLayout = QVBoxLayout(self)
        self._mainLayout.setAlignment(Qt.AlignTop)
        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainLayout.setSpacing(4)

        self._header = SongsTableHeader()
        self._header.setFixedHeight(48)

        self._menu = SongsMenu()
        self._menu.setClassName("scroll/bg-primary-75 scroll/hover:bg-primary scroll/rounded-2")
        self._menu.setContentsMargins(8, 0, 8, 0)
        self._menu.verticalScrollBar().setCursor(Cursors.pointer)

        self._noSongBox = QWidget()
        self._noSongBox.setFixedHeight(500)

        self._noSongLayout = Box(self._noSongBox)
        self._noSongLayout.setSpacing(12)
        self._noSongLayout.setAlignment(Qt.AlignTop)
        self._noSongLayout.setContentsMargins(0, 160, 0, 0)

        self._noSongImage = Cover()
        self._noSongImage.setAlignment(Qt.AlignCenter)
        self._noSongImage.setCover(Cover.Props.fromBytes(Images.empty, width=128))

        self._noSongMessage = Label()
        self._noSongMessage.setFont(FontFactory.create(size=10))
        self._noSongMessage.setClassName("text-black dark:text-white")
        self._noSongMessage.setAlignment(Qt.AlignCenter)
        self._noSongMessage.setFixedWidth(self._noSongBox.width())

        self._noSongLayout.addWidget(self._noSongImage, alignment=Qt.AlignHCenter)
        self._noSongLayout.addWidget(self._noSongMessage, alignment=Qt.AlignHCenter)

        self._mainLayout.addWidget(self._header)
        self._mainLayout.addWidget(self._noSongBox)
        self._mainLayout.addWidget(self._menu)

    def translateUI(self) -> None:
        self._noSongMessage.setText(translator.translate("SONGS_MENU.MESSAGE_NO_SONG"))

    def _connectSignalSlots(self) -> None:
        appCenter.currentPlaylistChanged.connect(lambda: self.__setCurrentPlaylist(appCenter.currentPlaylist))

    def __setCurrentPlaylist(self, playlist: Playlist) -> None:
        if self.__currentPlaylist is not None:
            Widgets.disconnect(self.__currentPlaylist.getSongs().updated, lambda: self.__updateNoSongMessageVisible())

        self.__currentPlaylist = playlist
        self.__currentPlaylist.getSongs().updated.connect(lambda: self.__updateNoSongMessageVisible())
        self.__updateNoSongMessageVisible()

    def __updateNoSongMessageVisible(self) -> None:
        self._noSongBox.setVisible(not self.__currentPlaylist.getSongs().hasAnySong())
