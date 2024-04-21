from abc import ABC
from typing import Optional, Union

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from app.components.base import Component, Cover, LabelWithDefaultText, Factory, StateIcon, CoverProps
from app.components.sliders import HorizontalSlider
from app.helpers.others import Times
from app.helpers.stylesheets import Colors, Paddings
from app.resource.qt import Images, Icons


class MusicPlayerBar(QWidget, Component, ABC):

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)
        self._createUI()
        self._connectSignalSlots()
        self._assignShortcuts()

        self.setDefaultCover(Images.DEFAULT_SONG_COVER)
        self._btnPrevSong.applyLightMode()
        self._btnPlaySong.applyLightMode()
        self._btnPauseSong.applyLightMode()
        self._btnNextSong.applyLightMode()
        self._sliderTime.applyLightMode()
        self._btnTimer.applyLightMode()

        self.setTotalTime(60)
        self.setPlayingTime(60)

    def _createUI(self) -> None:
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._mainLayout = QHBoxLayout(self)
        self._mainLayout.setContentsMargins(20, 0, 20, 0)
        self._mainLayout.setSpacing(0)

        self._left = QHBoxLayout()
        self._left.setContentsMargins(4, 0, 0, 0)
        self._left.setSpacing(12)
        self._left.setAlignment(Qt.AlignVCenter)

        self._middle = QHBoxLayout()
        self._middle.setContentsMargins(0, 0, 0, 0)
        self._middle.setSpacing(4)

        self._right = QHBoxLayout()
        self._right.setContentsMargins(0, 0, 0, 0)
        self._right.setSpacing(8)
        self._right.setAlignment(Qt.AlignVCenter)

        self._mainLayout.addLayout(self._left)
        self._mainLayout.addLayout(self._middle)
        self._mainLayout.addLayout(self._right)

        # ======================================== LEFT ========================================
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

        self._playButtons = QHBoxLayout()
        self._playButtons.setContentsMargins(0, 0, 0, 0)
        self._playButtons.setSpacing(8)

        self._btnPrevSong = Factory.createIconButton(size=Icons.LARGE, padding=Paddings.RELATIVE_50)
        self._btnPrevSong.setLightModeIcon(Icons.PREVIOUS.withColor(Colors.PRIMARY))
        self._btnPrevSong.setDarkModeIcon(Icons.PREVIOUS.withColor(Colors.WHITE))
        self._btnPrevSong.setClassName("hover:bg-primary-10 bg-none rounded-full", "dark:bg-primary-25 dark:hover:bg-primary")

        self._btnPlaySong = Factory.createIconButton(size=Icons.X_LARGE, padding=Paddings.RELATIVE_50)
        self._btnPlaySong.setLightModeIcon(Icons.PLAY.withColor(Colors.PRIMARY))
        self._btnPlaySong.setDarkModeIcon(Icons.PLAY.withColor(Colors.WHITE))
        self._btnPlaySong.setClassName("hover:bg-primary-25 bg-primary-10 rounded-full", "dark:bg-primary dark:hover:bg-primary")

        self._btnPauseSong = Factory.createIconButton(size=Icons.X_LARGE, padding=Paddings.RELATIVE_50)
        self._btnPauseSong.setLightModeIcon(Icons.PAUSE.withColor(Colors.PRIMARY))
        self._btnPauseSong.setDarkModeIcon(Icons.PAUSE.withColor(Colors.WHITE))
        self._btnPauseSong.setClassName("hover:bg-primary-25 bg-primary-10 rounded-full", "dark:bg-primary dark:hover:bg-primary")
        self._btnPauseSong.hide()

        self._btnNextSong = Factory.createIconButton(size=Icons.LARGE, padding=Paddings.RELATIVE_50)
        self._btnNextSong.setLightModeIcon(Icons.NEXT.withColor(Colors.PRIMARY))
        self._btnNextSong.setDarkModeIcon(Icons.NEXT.withColor(Colors.WHITE))
        self._btnNextSong.setClassName("hover:bg-primary-10 bg-none rounded-full", "dark:bg-primary-25 dark:hover:bg-primary")

        self._playButtons.addWidget(self._btnPrevSong)
        self._playButtons.addWidget(self._btnPlaySong)
        self._playButtons.addWidget(self._btnPauseSong)
        self._playButtons.addWidget(self._btnNextSong)

        self._left.addWidget(self._songCover)
        self._left.addLayout(self._infoLayout, stretch=1)
        self._left.addLayout(self._playButtons)

        # ======================================== MIDDLE ========================================
        self._labelPlayingTime = LabelWithDefaultText()
        self._labelPlayingTime.setFixedWidth(60)
        self._labelPlayingTime.setFont(Factory.createFont(size=9))
        self._labelPlayingTime.setClassName("text-black dark:text-white")
        self._labelPlayingTime.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self._sliderTime = HorizontalSlider()
        self._sliderTime.setFixedWidth(250)
        self._sliderTime.setFixedHeight(12)
        self._sliderTime.setSliderSize(handle=10)
        self._sliderTime.setPageStep(0)
        self._sliderTime.setMaximum(100)
        self._sliderTime.setProperty("value", 0)

        self._labelTotalTime = LabelWithDefaultText()
        self._labelTotalTime.setFixedWidth(60)
        self._labelTotalTime.setFont(Factory.createFont(size=9))
        self._labelTotalTime.setClassName("text-black dark:text-white")
        self._labelTotalTime.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self._middle.addWidget(self._labelPlayingTime)
        self._middle.addWidget(self._sliderTime)
        self._middle.addWidget(self._labelTotalTime)

        # ======================================== RIGHT ========================================
        self._btnLoop = Factory.createToggleButton(Icons.LARGE, Paddings.RELATIVE_50)
        self._btnLoop.setActiveIcon(Icons.LOOP.withColor(Colors.PRIMARY))
        self._btnLoop.setInactiveIcon(Icons.LOOP.withColor(Colors.GRAY))
        self._btnLoop.setClassName("rounded-full bg-none active/hover:bg-primary-12 inactive/hover:bg-gray-12")
        self._btnLoop.setActive(False)

        self._btnShuffle = Factory.createToggleButton(Icons.LARGE, Paddings.RELATIVE_50)
        self._btnShuffle.setActiveIcon(Icons.SHUFFLE.withColor(Colors.PRIMARY))
        self._btnShuffle.setInactiveIcon(Icons.SHUFFLE.withColor(Colors.GRAY))
        self._btnShuffle.setClassName("rounded-full bg-none active/hover:bg-primary-12 inactive/hover:bg-gray-12")
        self._btnShuffle.setActive(False)

        self._btnLove = Factory.createToggleButton(Icons.LARGE, Paddings.RELATIVE_50)
        self._btnLove.setActiveIcon(Icons.LOVE.withColor(Colors.DANGER))
        self._btnLove.setInactiveIcon(Icons.LOVE.withColor(Colors.GRAY))
        self._btnLove.setClassName("rounded-full bg-none active/hover:bg-danger-12 inactive/hover:bg-gray-12")
        self._btnLove.setActive(False)

        self._btnVolume = Factory.createMultiStatesButton(Icons.LARGE, Paddings.RELATIVE_50)
        self._btnVolume.setIcons([
            StateIcon(Icons.VOLUME_UP.withColor(Colors.PRIMARY)),
            StateIcon(Icons.VOLUME_DOWN.withColor(Colors.PRIMARY)),
            StateIcon(Icons.VOLUME_SILENT.withColor(Colors.PRIMARY)),
        ])
        self._btnVolume.setClassName("rounded-full bg-none hover:bg-primary-12")
        self._btnVolume.setChangeStateOnPressed(False)
        self._btnVolume.setActiveState(0)

        self._volumeBox = QWidget()
        self._volumeBoxLayout = QHBoxLayout(self._volumeBox)
        self._volumeBoxLayout.setContentsMargins(0, 0, 0, 0)

        self._btnTimer = Factory.createIconButton(size=Icons.LARGE, padding=Paddings.RELATIVE_50)
        self._btnTimer.setLightModeIcon(Icons.TIMER.withColor(Colors.PRIMARY))
        self._btnTimer.setClassName("bg-none hover:bg-primary-10 rounded-full", "dark:bg-primary-25 dark:hover:bg-primary")

        self._right.addWidget(self._btnLoop)
        self._right.addWidget(self._btnShuffle)
        self._right.addWidget(self._btnLove)
        self._right.addWidget(self._btnVolume)
        self._right.addWidget(self._volumeBox, 1)
        self._right.addWidget(self._btnTimer)

    def _connectSignalSlots(self) -> None:
        self._btnPlaySong.clicked.connect(lambda: self.setPlay(False))
        self._btnPauseSong.clicked.connect(lambda: self.setPlay(True))

    def _assignShortcuts(self) -> None:
        pass

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

    def setPlayingTime(self, time: float) -> None:
        self._labelPlayingTime.setText(Times.toString(time))

    def setTotalTime(self, time: float) -> None:
        self._labelTotalTime.setText(Times.toString(time))
