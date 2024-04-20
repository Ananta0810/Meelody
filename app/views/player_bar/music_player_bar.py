from abc import ABC
from typing import Optional, Union

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from app.components.base import Component, Cover, LabelWithDefaultText, Factory
from app.components.base.cover import CoverProps
from app.helpers.stylesheets import Color
from app.resource.qt import Images, Icons


class MusicPlayerBar(QWidget, Component, ABC):

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)
        self._createUI()
        self.setDefaultCover(Images.DEFAULT_SONG_COVER)
        self._assignShortcuts()

    def _createUI(self) -> None:
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._mainLayout = QHBoxLayout(self)
        self._mainLayout.setContentsMargins(20, 0, 20, 0)
        self._mainLayout.setSpacing(0)

        self._left = QHBoxLayout()
        self._left.setContentsMargins(4, 0, 0, 0)
        self._left.setSpacing(12)
        self._left.setAlignment(Qt.AlignVCenter)

        # =================COVER - TITLE - ARTIST=================
        self._songCover = Cover()
        self._songCover.setFixedSize(64, 64)

        self._songTitle = LabelWithDefaultText()
        self._songTitle.enableEllipsis()
        self._songTitle.setFixedWidth(128)
        self._songTitle.setFont(Factory.createFont(size=10, bold=True))
        self._songTitle.setText("Song Title")

        self._songArtist = LabelWithDefaultText()
        self._songArtist.enableEllipsis()
        self._songArtist.setFixedWidth(128)
        self._songArtist.setFont(Factory.createFont(size=9))
        self._songArtist.setText("Song Artist")

        self._infoLayout = QVBoxLayout()
        self._infoLayout.setContentsMargins(0, 0, 0, 0)
        self._infoLayout.setSpacing(0)

        self._infoLayout.addStretch(0)
        self._infoLayout.addWidget(self._songTitle)
        self._infoLayout.addWidget(self._songArtist)
        self._infoLayout.addStretch(0)

        # =================PREVIOUS - PLAY - NEXT=================
        self._playButtons = QHBoxLayout()
        self._playButtons.setContentsMargins(0, 0, 0, 0)
        self._playButtons.setSpacing(8)

        self._btnPrevSong = Factory.createIconButton(size=Icons.LARGE)
        self._btnPrevSong.setLightModeIcon(Icons.PREVIOUS.withColor(Color(128, 64, 255)))
        self._btnPrevSong.setClassName("hover:bg-primary-10 bg-none rounded-full")

        self._btnPlaySong = Factory.createIconButton(size=Icons.LARGE)
        self._btnPlaySong.setLightModeIcon(Icons.PLAY.withColor(Color(128, 64, 255)))
        self._btnPlaySong.setClassName("hover:bg-primary-25 bg-primary-10 rounded-full")

        self._btnNextSong = Factory.createIconButton(size=Icons.LARGE)
        self._btnNextSong.setLightModeIcon(Icons.NEXT.withColor(Color(128, 64, 255)))
        self._btnNextSong.setClassName("hover:bg-primary-10 bg-none rounded-full")

        self._playButtons.addWidget(self._btnPrevSong)
        self._playButtons.addWidget(self._btnPlaySong)
        self._playButtons.addWidget(self._btnNextSong)

        self._left.addWidget(self._songCover)
        self._left.addLayout(self._infoLayout, stretch=1)
        self._left.addLayout(self._playButtons)

        self._mainLayout.addLayout(self._left)
        self._mainLayout.addStretch()

    def _connectSignalSlots(self) -> None:
        pass

    def _assignShortcuts(self) -> None:
        super()._assignShortcuts()

    def applyDarkMode(self) -> None:
        pass

    def applyLightMode(self) -> None:
        pass

    def setDefaultCover(self, cover: bytes) -> None:
        self._songCover.setDefaultCover(self.__createCover(cover))

    @staticmethod
    def __createCover(data: bytes) -> Union[CoverProps, None]:
        if data is None:
            return None
        return CoverProps.fromBytes(data, width=64, height=64, radius=16)
