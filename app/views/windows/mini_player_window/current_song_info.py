import typing
from typing import Optional

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from app.common.models import Song
from app.common.others import musicPlayer
from app.common.statics.qt import Images
from app.components.base import FontFactory
from app.components.events import SignalConnector
from app.components.images.cover import CoverWithPlaceHolder, Cover
from app.components.labels import Label
from app.components.widgets import ExtendableStyleWidget, Box
from app.helpers.files import ImageEditor
from app.utils.qt import Signals
from app.utils.reflections import suppressException


class CurrentSongInfo(ExtendableStyleWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        super()._initComponent()

        self.__displaySongInfo(musicPlayer.getCurrentSong())

    def _createUI(self) -> None:
        self._mainLayout = Box(self)
        self._mainLayout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self._background = CoverWithPlaceHolder(self)
        self._background.setFixedSize(self.size())
        self._background.setPlaceHolderCover(Cover.Props.fromBytes(self.__blurBackgroundOf(Images.defaultPlaylistCover)))

        self._cover = CoverWithPlaceHolder()
        self._cover.setFixedSize(256, 256)
        self._cover.setPlaceHolderCover(Cover.Props.fromBytes(Images.defaultPlaylistCover, width=256, height=256, radius=16))

        self._titleLabel = Label(autoChangeTheme=False)
        self._titleLabel.setFont(FontFactory.create(family="Segoe UI Semibold", size=14))
        self._titleLabel.setClassName("text-white bg-none")

        self._titleLabel.setAlignment(Qt.AlignHCenter)

        self._artistLabel = Label(autoChangeTheme=False)
        self._artistLabel.setFont(FontFactory.create(size=9))
        self._artistLabel.setClassName("text-white-50 bg-none")
        self._artistLabel.setAlignment(Qt.AlignHCenter)

        self._mainLayout.addWidget(self._cover, alignment=Qt.AlignHCenter)
        self._mainLayout.addSpacing(12)
        self._mainLayout.addWidget(self._titleLabel, alignment=Qt.AlignHCenter)
        self._mainLayout.addSpacing(8)
        self._mainLayout.addWidget(self._artistLabel, alignment=Qt.AlignHCenter)
        self._mainLayout.addStretch()

        self._signalConnector = SignalConnector(self)

    def _connectSignalSlots(self) -> None:
        self._signalConnector.connect(musicPlayer.songChanged, lambda song: self.__displaySongInfo(song))
        self.destroyed.connect(lambda: Signals.disconnect(musicPlayer.songChanged, lambda song: self.__displaySongInfo(song)))

    def resizeEvent(self, a0: typing.Optional[QtGui.QResizeEvent]) -> None:
        super().resizeEvent(a0)
        self._background.setFixedSize(a0.size())
        self._titleLabel.setFixedWidth(a0.size().width() - self.contentsMargins().left() - self.contentsMargins().right())
        self._artistLabel.setFixedWidth(a0.size().width() - self.contentsMargins().left() - self.contentsMargins().right())

    @suppressException
    def __displaySongInfo(self, song: Song) -> None:
        if song is None:
            return

        self._titleLabel.setText(song.getTitle())
        self._artistLabel.setText(song.getArtist())

        if song.isCoverLoaded():
            self.__setCover(song.getCover())
        else:
            self.__setCover(None)
            song.coverChanged.connect(self.__setCover)
            song.loadCover()

    @suppressException
    def __setCover(self, cover: Optional[bytes]) -> None:
        self._cover.setCover(Cover.Props.fromBytes(cover, width=256, height=256, radius=16))

        blurCover = None if cover is None else self.__blurBackgroundOf(cover)
        self._background.setCover(Cover.Props.fromBytes(blurCover))

    @staticmethod
    def __blurBackgroundOf(cover: bytes) -> bytes:
        return ImageEditor.of(cover).resize(width=720, height=540).gaussianBlur(blurRadius=100).darken(33).toBytes()
