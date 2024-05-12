from contextlib import suppress
from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from app.common.models import Song
from app.common.others import musicPlayer
from app.common.statics.qt import Images
from app.components.base import FontFactory
from app.components.images.cover import CoverWithPlaceHolder, Cover
from app.components.labels import Label
from app.components.widgets import ExtendableStyleWidget, Box


class CurrentSongInfo(ExtendableStyleWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        self.__song: Optional[Song] = None

        super().__init__(parent)
        super()._initComponent()

        self.__displaySongInfo(musicPlayer.getCurrentSong())

    def _createUI(self) -> None:
        self._mainLayout = Box(self)
        self._mainLayout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self._cover = CoverWithPlaceHolder()
        self._cover.setFixedSize(256, 256)
        self._cover.setPlaceHolderCover(self.__createCover(Images.defaultPlaylistCover))

        self._titleLabel = Label()
        self._titleLabel.setFont(FontFactory.create(family="Segoe UI Semibold", size=14))
        self._titleLabel.setClassName("text-black dark:text-white bg-none")
        self._titleLabel.setText("Song name here")

        self._artistLabel = Label()
        self._artistLabel.setFont(FontFactory.create(size=9))
        self._artistLabel.setClassName("text-gray bg-none")
        self._artistLabel.setText("Song artist here")

        self._mainLayout.addWidget(self._cover, alignment=Qt.AlignHCenter)
        self._mainLayout.addSpacing(12)
        self._mainLayout.addWidget(self._titleLabel, alignment=Qt.AlignHCenter)
        self._mainLayout.addSpacing(8)
        self._mainLayout.addWidget(self._artistLabel, alignment=Qt.AlignHCenter)
        self._mainLayout.addStretch()

    def _connectSignalSlots(self) -> None:
        musicPlayer.songChanged.connect(lambda song: self.__displaySongInfo(song))

    def __displaySongInfo(self, song: Song) -> None:
        if song is None:
            return

        if self.__song is not None:
            with suppress(TypeError):
                self.__song.coverChanged.disconnect(self.__setCover)

        self.__song = song

        self._titleLabel.setText(song.getTitle())
        self._artistLabel.setText(song.getArtist())

        if song.isCoverLoaded():
            self.__setCover(song.getCover())
        else:
            self.__setCover(None)
            song.coverChanged.connect(self.__setCover)
            song.loadCover()

    def __setCover(self, cover: Optional[bytes]) -> None:
        self._cover.setCover(self.__createCover(cover))

    @staticmethod
    def __createCover(data: bytes) -> Optional[Cover.Props]:
        if data is None:
            return None
        return Cover.Props.fromBytes(data, width=256, height=256, radius=16)
