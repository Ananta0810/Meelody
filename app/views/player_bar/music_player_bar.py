from abc import ABC
from time import sleep
from typing import Optional, Union

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QShortcut

from app.common.instances import MUSIC_PLAYER
from app.common.models import Song
from app.components.base import Component, Cover, LabelWithDefaultText, Factory, StateIcon, CoverProps
from app.components.sliders import HorizontalSlider
from app.helpers.others import Times
from app.helpers.stylesheets import Colors, Paddings
from app.resource.qt import Images, Icons


class MusicPlayerBar(QWidget, Component, ABC):

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)
        self.__songLength: float = 0
        self.__canRunTimeSlider = True

        self._createUI()
        self._createThreads()
        self._connectSignalSlots()
        self._assignShortcuts()

        self.setPlayingTime(0)
        self.setTotalTime(0)
        self._songTitle.setText("Song Title")
        self._songArtist.setText("Song Artist")
        
        self.setDefaultCover(Images.DEFAULT_SONG_COVER)
        self._btnPrevSong.applyLightMode()
        self._btnPlaySong.applyLightMode()
        self._btnPauseSong.applyLightMode()
        self._btnNextSong.applyLightMode()
        self._sliderTime.applyLightMode()
        self._btnTimer.applyLightMode()
        self._sliderVolume.applyLightMode()

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
        self._left.setAlignment(Qt.AlignVCenter)

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

        self._songArtist = LabelWithDefaultText()
        self._songArtist.enableEllipsis()
        self._songArtist.setFixedWidth(128)
        self._songArtist.setFont(Factory.createFont(size=9))

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

        self._sliderVolume = HorizontalSlider()
        self._sliderVolume.setFixedHeight(40)
        self._sliderVolume.setPageStep(0)
        self._sliderVolume.setMaximum(100)
        self._sliderVolume.setProperty("value", 0)
        self._sliderVolume.setClassName("rounded-8 bg-primary-10")
        self._sliderVolume.setSliderPosition(100)
        self._sliderVolume.hide()

        self._volumeBoxLayout.addWidget(self._sliderVolume)

        self._btnTimer = Factory.createIconButton(size=Icons.LARGE, padding=Paddings.RELATIVE_50)
        self._btnTimer.setLightModeIcon(Icons.TIMER.withColor(Colors.PRIMARY))
        self._btnTimer.setClassName("bg-none hover:bg-primary-10 rounded-full", "dark:bg-primary-25 dark:hover:bg-primary")

        self._right.addWidget(self._btnLoop)
        self._right.addWidget(self._btnShuffle)
        self._right.addWidget(self._btnLove)
        self._right.addWidget(self._btnVolume)
        self._right.addWidget(self._volumeBox, 1)
        self._right.addWidget(self._btnTimer)

    def _createThreads(self):
        self._playerTrackingThread = PlayerTrackingThread(self)

    def _connectSignalSlots(self) -> None:
        self._btnVolume.clicked.connect(lambda: self._sliderVolume.setVisible(not self._sliderVolume.isVisible()))
        self._sliderTime.sliderPressed.connect(lambda: self.__setCanRunTimeSlider(False))
        self._sliderTime.sliderReleased.connect(lambda: self.__setCanRunTimeSlider(True))

        self._btnPlaySong.clicked.connect(lambda: MUSIC_PLAYER.play())
        self._btnPauseSong.clicked.connect(lambda: MUSIC_PLAYER.pause())
        self._btnPrevSong.clicked.connect(lambda: MUSIC_PLAYER.playPreviousSong())
        self._btnNextSong.clicked.connect(lambda: MUSIC_PLAYER.playNextSong())
        self._btnLoop.clicked.connect(lambda: MUSIC_PLAYER.setLooping(self._btnLoop.isActive()))
        self._btnShuffle.clicked.connect(lambda: MUSIC_PLAYER.setShuffle(self._btnShuffle.isActive()))
        self._sliderVolume.valueChanged.connect(lambda: MUSIC_PLAYER.setVolume(self._sliderVolume.value()))
        self._sliderTime.sliderReleased.connect(lambda: self.__skipTo(self._sliderTime.sliderPosition()))

        MUSIC_PLAYER.played.connect(lambda: self._playerTrackingThread.start())
        MUSIC_PLAYER.paused.connect(lambda: self._playerTrackingThread.quit())
        MUSIC_PLAYER.songChanged.connect(lambda song: self.__selectSong(song))
        MUSIC_PLAYER.loopChanged.connect(lambda a0: self._btnLoop.setActive(a0))
        MUSIC_PLAYER.shuffleChanged.connect(lambda a0: self._btnShuffle.setActive(a0))
        MUSIC_PLAYER.volumeChanged.connect(lambda volume: self.__changeVolumeIcon(volume))

    def _assignShortcuts(self) -> None:
        play_shortcut = QShortcut(QKeySequence(Qt.Key_Space), self._btnPlaySong)
        play_shortcut.activated.connect(self._btnPlaySong.click)

        pause_shortcut = QShortcut(QKeySequence(Qt.Key_Space), self._btnPauseSong)
        pause_shortcut.activated.connect(self._btnPauseSong.click)

        prev_shortcut = QShortcut(QKeySequence(Qt.Key_Left), self._btnPrevSong)
        prev_shortcut.activated.connect(self._btnPrevSong.click)

        next_shortcut = QShortcut(QKeySequence(Qt.Key_Right), self._btnNextSong)
        next_shortcut.activated.connect(self._btnNextSong.click)

        shortcut_0 = QShortcut(QKeySequence(Qt.Key_0), self._sliderTime)
        shortcut_0.activated.connect(lambda: self.__skipTo(0))

        shortcut_1 = QShortcut(QKeySequence(Qt.Key_1), self._sliderTime)
        shortcut_1.activated.connect(lambda: self.__skipTo(10))

        shortcut_2 = QShortcut(QKeySequence(Qt.Key_2), self._sliderTime)
        shortcut_2.activated.connect(lambda: self.__skipTo(20))

        shortcut_3 = QShortcut(QKeySequence(Qt.Key_3), self._sliderTime)
        shortcut_3.activated.connect(lambda: self.__skipTo(30))

        shortcut_4 = QShortcut(QKeySequence(Qt.Key_4), self._sliderTime)
        shortcut_4.activated.connect(lambda: self.__skipTo(40))

        shortcut_5 = QShortcut(QKeySequence(Qt.Key_5), self._sliderTime)
        shortcut_5.activated.connect(lambda: self.__skipTo(50))

        shortcut_6 = QShortcut(QKeySequence(Qt.Key_6), self._sliderTime)
        shortcut_6.activated.connect(lambda: self.__skipTo(60))

        shortcut_7 = QShortcut(QKeySequence(Qt.Key_7), self._sliderTime)
        shortcut_7.activated.connect(lambda: self.__skipTo(70))

        shortcut_8 = QShortcut(QKeySequence(Qt.Key_8), self._sliderTime)
        shortcut_8.activated.connect(lambda: self.__skipTo(80))

        shortcut_9 = QShortcut(QKeySequence(Qt.Key_9), self._sliderTime)
        shortcut_9.activated.connect(lambda: self.__skipTo(90))

    def __skipTo(self, position: int) -> None:
        self._sliderTime.setValue(position)
        try:
            MUSIC_PLAYER.skipToTime(MUSIC_PLAYER.getCurrentSong().getLength() * position / 100)
            MUSIC_PLAYER.play()
        except AttributeError:
            self._sliderTime.setValue(0)

    def setDefaultCover(self, cover: bytes) -> None:
        self._songCover.setDefaultCover(self.__createCover(cover))

    @staticmethod
    def __createCover(data: bytes) -> Union[CoverProps, None]:
        if data is None:
            return None
        return CoverProps.fromBytes(data, width=64, height=64, radius=12)

    def setPlay(self, isPlaying: bool) -> None:
        self._btnPlaySong.setVisible(isPlaying)
        self._btnPauseSong.setVisible(not isPlaying)

    def setTotalTime(self, time: float) -> None:
        self.__songLength = time
        self._labelTotalTime.setText(Times.toString(time))

    def setPlayingTime(self, time: float) -> None:
        if not self.__canRunTimeSlider:
            return
        self._labelPlayingTime.setText(Times.toString(time))
        position = 0 if self.__songLength == 0 else int(time * 100 / self.__songLength)
        self._sliderTime.setSliderPosition(position)

    def __setCanRunTimeSlider(self, enable: bool) -> None:
        self.__canRunTimeSlider = enable

    def __selectSong(self, song: Song) -> None:
        self.setTotalTime(song.getLength())
        self._songTitle.setText(song.getTitle())
        self._songArtist.setText(song.getArtist())
        self._songCover.setCover(self.__createCover(song.getCover()))

    def __changeVolumeIcon(self, volume: int) -> None:
        VOLUME_UP_STATE: int = 0
        VOLUME_DOWN_STATE: int = 1
        SILENT_STATE: int = 2
        state = SILENT_STATE

        if 0 < volume <= 33:
            state = VOLUME_DOWN_STATE
        if 33 < volume <= 100:
            state = VOLUME_UP_STATE
        self._btnVolume.setActiveState(state)


class PlayerTrackingThread(QThread):

    def __init__(self, musicPlayer: MusicPlayerBar) -> None:
        super().__init__()
        self.__musicPlayer = musicPlayer

    def run(self) -> None:
        interval: float = MUSIC_PLAYER.refreshRate()

        while MUSIC_PLAYER.isPlaying():
            self.__musicPlayer.setPlayingTime(MUSIC_PLAYER.getPlayingTime())
            sleep(interval)
