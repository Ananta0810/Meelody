from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from app.common.models import Playlist
from app.components.base import Cover, LabelWithDefaultText, Factory, CoverProps
from app.resource.qt import Images
from app.views.home.songs_table import SongsTable


class Info(QVBoxLayout):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.__initUI()

    def __initUI(self) -> None:
        self.setSpacing(12)

        self._cover = Cover()
        self._cover.setFixedSize(320, 320)

        self._labelsLayout = QVBoxLayout()
        self._labelsLayout.setSpacing(0)

        self._labelTitle = LabelWithDefaultText()
        self._labelTitle.enableEllipsis()
        self._labelTitle.setFixedWidth(320)
        self._labelTitle.setFont(Factory.createFont(size=20, bold=True))

        self._labelTotalSongs = LabelWithDefaultText()
        self._labelTotalSongs.setFixedWidth(320)
        self._labelTotalSongs.setFont(Factory.createFont(size=10))

        self._labelsLayout.addWidget(self._labelTitle)
        self._labelsLayout.addWidget(self._labelTotalSongs)

        self.addWidget(self._cover)
        self.addLayout(self._labelsLayout)
        self.addStretch()

    def setPlaylist(self, playlist: Playlist) -> None:
        self._cover.set_cover(self.__createCover(playlist.getInfo().cover))
        self._labelTitle.setText(playlist.getInfo().name)
        self._labelTotalSongs.setText(f"{playlist.getSongs().size()} TRACKS")

    def setDefaultCover(self, cover: bytes) -> None:
        self._cover.setDefaultCover(self.__createCover(cover))

    @staticmethod
    def __createCover(pixmapByte: bytes) -> Optional[CoverProps]:
        if pixmapByte is None:
            return None
        return CoverProps.fromBytes(pixmapByte, width=320, height=320, radius=24)


class CurrentPlaylist(QWidget):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.__initUI()
        self._info.setDefaultCover(Images.DEFAULT_PLAYLIST_COVER)

    def __initUI(self) -> None:
        self._mainLayout = QHBoxLayout(self)
        self._mainLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self._mainLayout.setSpacing(50)
        self._mainLayout.setContentsMargins(0, 0, 0, 0)

        self._info = Info()
        self._menu = SongsTable()

        self._mainLayout.addLayout(self._info)
        self._mainLayout.addWidget(self._menu, stretch=2)

    def setPlaylist(self, playlist: Playlist) -> None:
        self._info.setPlaylist(playlist)
