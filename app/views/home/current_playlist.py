from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from app.common.models import Playlist
from app.common.others import appCenter, translator
from app.components.base import LabelWithDefaultText, Factory, CoverProps, Component, CoverWithPlaceHolder
from app.resource.qt import Images
from app.views.home.songs_table import SongsTable


class _Info(QVBoxLayout, Component):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._initComponent()

    def _createUI(self) -> None:
        self.setSpacing(12)
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self._cover = CoverWithPlaceHolder()
        self._cover.setFixedSize(320, 320)
        self._cover.setPlaceHolderCover(self.__createCover(Images.defaultPlaylistCover))

        self._titleLabel = LabelWithDefaultText()
        self._titleLabel.enableEllipsis()
        self._titleLabel.setFixedWidth(320)
        self._titleLabel.setFont(Factory.createFont(size=20, bold=True))
        self._titleLabel.setClassName("text-black dark:text-white")

        self._totalSongsLabel = LabelWithDefaultText()
        self._totalSongsLabel.setFixedWidth(320)
        self._totalSongsLabel.setFont(Factory.createFont(size=10))
        self._totalSongsLabel.setClassName("text-black dark:text-white")

        self._labelsLayout = QVBoxLayout()
        self._labelsLayout.setSpacing(0)
        self._labelsLayout.addWidget(self._titleLabel)
        self._labelsLayout.addWidget(self._totalSongsLabel)

        self.addWidget(self._cover)
        self.addLayout(self._labelsLayout)

    def _translateUI(self) -> None:
        playlist = appCenter.currentPlaylist
        self._titleLabel.setText(playlist.getInfo().getName())
        self._totalSongsLabel.setText(f"{playlist.getSongs().size()} {translator.translate('CURRENT_PLAYLIST.TRACKS')}")

    def _connectSignalSlots(self) -> None:
        appCenter.currentPlaylistChanged.connect(lambda playlist: self.__setPlaylist(playlist))

    def __setPlaylist(self, playlist: Playlist) -> None:
        self._cover.setCover(self.__createCover(playlist.getInfo().getCover()))
        self._titleLabel.setText(playlist.getInfo().getName())
        self._totalSongsLabel.setText(f"{playlist.getSongs().size()} {translator.translate('CURRENT_PLAYLIST.TRACKS')}")

    @staticmethod
    def __createCover(data: bytes) -> Optional[CoverProps]:
        return CoverProps.fromBytes(data, width=320, height=320, radius=24)


class CurrentPlaylist(QWidget):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.__initUI()

    def __initUI(self) -> None:
        self._mainLayout = QHBoxLayout(self)
        self._mainLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self._mainLayout.setSpacing(50)
        self._mainLayout.setContentsMargins(0, 0, 0, 0)

        self._info = _Info()
        self._menu = SongsTable()

        self._mainLayout.addLayout(self._info)
        self._mainLayout.addWidget(self._menu, stretch=2)

    def setPlaylist(self, playlist: Playlist) -> None:
        self._info.setPlaylist(playlist)
