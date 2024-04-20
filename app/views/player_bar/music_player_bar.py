from abc import ABC
from typing import Optional, Union

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from app.components.base import Component, Cover, LabelWithDefaultText, Factory
from app.components.base.cover import CoverProps
from app.helpers.stylesheets import Colors, Paddings
from app.resource.qt import Images, Icons


class MusicPlayerBar(QWidget, Component, ABC):

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)
        self._createUI()
        self.setDefaultCover(Images.DEFAULT_SONG_COVER)
        self._assignShortcuts()
        self._btnPrevSong.applyDarkMode()
        self._btnPlaySong.applyDarkMode()
        self._btnPauseSong.applyDarkMode()
        self._btnNextSong.applyDarkMode()

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

        self._btnPrevSong = Factory.createIconButton(size=Icons.LARGE, padding=Paddings.RELATIVE_50)
        self._btnPrevSong.setLightModeIcon(Icons.PREVIOUS.withColor(Colors.PRIMARY))
        self._btnPrevSong.setDarkModeIcon(Icons.NEXT.withColor(Colors.WHITE))
        self._btnPrevSong.setClassName("hover:bg-primary-10 bg-none rounded-full",
                                       "dark:bg-primary-25 dark:hover:bg-primary")

        self._btnPlaySong = Factory.createIconButton(size=Icons.X_LARGE, padding=Paddings.RELATIVE_50)
        self._btnPlaySong.setLightModeIcon(Icons.PLAY.withColor(Colors.PRIMARY))
        self._btnPlaySong.setDarkModeIcon(Icons.PLAY.withColor(Colors.WHITE))
        self._btnPlaySong.setClassName("hover:bg-primary-25 bg-primary-10 rounded-full",
                                       "dark:bg-primary dark:hover:bg-primary")

        self._btnPauseSong = Factory.createIconButton(size=Icons.X_LARGE, padding=Paddings.RELATIVE_50)
        self._btnPauseSong.setLightModeIcon(Icons.PAUSE.withColor(Colors.PRIMARY))
        self._btnPauseSong.setDarkModeIcon(Icons.PAUSE.withColor(Colors.WHITE))
        self._btnPauseSong.setClassName("hover:bg-primary-25 bg-primary-10 rounded-full",
                                        "dark:bg-primary dark:hover:bg-primary")
        self._btnPauseSong.hide()

        self._btnNextSong = Factory.createIconButton(size=Icons.LARGE, padding=Paddings.RELATIVE_50)
        self._btnNextSong.setLightModeIcon(Icons.NEXT.withColor(Colors.PRIMARY))
        self._btnNextSong.setDarkModeIcon(Icons.NEXT.withColor(Colors.WHITE))
        self._btnNextSong.setClassName("hover:bg-primary-10 bg-none rounded-full",
                                       "dark:bg-primary-25 dark:hover:bg-primary")

        self._playButtons.addWidget(self._btnPrevSong)
        self._playButtons.addWidget(self._btnPlaySong)
        self._playButtons.addWidget(self._btnPauseSong)
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
        self._btnPlaySong.clicked.connect(lambda: self.setPlay(False))
        self._btnPauseSong.clicked.connect(lambda: self.setPlay(True))

    def setDefaultCover(self, cover: bytes) -> None:
        self._songCover.setDefaultCover(self.__createCover(cover))

    @staticmethod
    def __createCover(data: bytes) -> Union[CoverProps, None]:
        if data is None:
            return None
        return CoverProps.fromBytes(data, width=64, height=64, radius=16)

    def setPlay(self, isPlaying: bool) -> None:
        self._btnPlaySong.setVisible(isPlaying)
        self._btnPauseSong.setVisible(not isPlaying)
