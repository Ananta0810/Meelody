import contextlib
from time import sleep
from typing import Optional, Union

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QShortcut

from app.common.models import Song
from app.common.others import musicPlayer
from app.components.base import Component, Cover, LabelWithDefaultText, Factory, StateIcon, CoverProps
from app.components.sliders import HorizontalSlider
from app.helpers.others import Times
from app.helpers.stylesheets import Colors, Paddings
from app.resource.qt import Images, Icons


class MusicPlayerBar(QWidget, Component):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.__songLength: float = 0
        self.__canRunTimeSlider = True
        self.__currentSong: Optional[Song] = None

        super()._initComponent()

        self._titleLabel.setText("Song Title")
        self._artistLabel.setText("Song Artist")
        self.setDefaultCover(Images.DEFAULT_SONG_COVER)
        self.setPlayingTime(0)
        self.setTotalTime(0)

    def _createUI(self) -> None:
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._mainLayout = QHBoxLayout(self)
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

        self._titleLabel = LabelWithDefaultText()
        self._titleLabel.enableEllipsis()
        self._titleLabel.setFixedWidth(128)
        self._titleLabel.setFont(Factory.createFont(size=10, bold=True))
        self._titleLabel.setClassName("text-black dark:text-white")

        self._artistLabel = LabelWithDefaultText()
        self._artistLabel.enableEllipsis()
        self._artistLabel.setFixedWidth(128)
        self._artistLabel.setFont(Factory.createFont(size=9))
        self._artistLabel.setClassName("text-black dark:text-gray")

        self._infoLayout = QVBoxLayout()
        self._infoLayout.setContentsMargins(0, 0, 0, 0)
        self._infoLayout.setSpacing(0)

        self._infoLayout.addStretch(0)
        self._infoLayout.addWidget(self._titleLabel)
        self._infoLayout.addWidget(self._artistLabel)
        self._infoLayout.addStretch(0)

        self._playButtons = QHBoxLayout()
        self._playButtons.setContentsMargins(0, 0, 0, 0)
        self._playButtons.setSpacing(8)

        self._prevSongBtn = Factory.createIconButton(size=Icons.LARGE, padding=Paddings.RELATIVE_50)
        self._prevSongBtn.setLightModeIcon(Icons.PREVIOUS.withColor(Colors.PRIMARY))
        self._prevSongBtn.setDarkModeIcon(Icons.PREVIOUS.withColor(Colors.WHITE))
        self._prevSongBtn.setClassName("hover:bg-primary-10 bg-none rounded-full", "dark:bg-none dark:hover:bg-white-20")

        self._playSongBtn = Factory.createIconButton(size=Icons.X_LARGE, padding=Paddings.RELATIVE_50)
        self._playSongBtn.setLightModeIcon(Icons.PLAY.withColor(Colors.PRIMARY))
        self._playSongBtn.setDarkModeIcon(Icons.PLAY.withColor(Colors.WHITE))
        self._playSongBtn.setClassName("hover:bg-primary-25 bg-primary-10 rounded-full", "dark:bg-primary dark:hover:bg-primary")

        self._pauseSongBtn = Factory.createIconButton(size=Icons.X_LARGE, padding=Paddings.RELATIVE_50)
        self._pauseSongBtn.setLightModeIcon(Icons.PAUSE.withColor(Colors.PRIMARY))
        self._pauseSongBtn.setDarkModeIcon(Icons.PAUSE.withColor(Colors.WHITE))
        self._pauseSongBtn.setClassName("hover:bg-primary-25 bg-primary-10 rounded-full", "dark:bg-primary dark:hover:bg-primary")
        self._pauseSongBtn.hide()

        self._nextSongBtn = Factory.createIconButton(size=Icons.LARGE, padding=Paddings.RELATIVE_50)
        self._nextSongBtn.setLightModeIcon(Icons.NEXT.withColor(Colors.PRIMARY))
        self._nextSongBtn.setDarkModeIcon(Icons.NEXT.withColor(Colors.WHITE))
        self._nextSongBtn.setClassName("hover:bg-primary-10 bg-none rounded-full", "dark:bg-none dark:hover:bg-white-20")

        self._playButtons.addWidget(self._prevSongBtn)
        self._playButtons.addWidget(self._playSongBtn)
        self._playButtons.addWidget(self._pauseSongBtn)
        self._playButtons.addWidget(self._nextSongBtn)

        self._left.addWidget(self._songCover)
        self._left.addLayout(self._infoLayout, stretch=1)
        self._left.addLayout(self._playButtons)

        # ======================================== MIDDLE ========================================
        self._playingTimeLabel = LabelWithDefaultText()
        self._playingTimeLabel.setFixedWidth(60)
        self._playingTimeLabel.setFont(Factory.createFont(size=9))
        self._playingTimeLabel.setClassName("text-black dark:text-white")
        self._playingTimeLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self._timeSlider = HorizontalSlider()
        self._timeSlider.setFixedWidth(250)
        self._timeSlider.setFixedHeight(12)
        self._timeSlider.setSliderSize(handle=10)
        self._timeSlider.setPageStep(0)
        self._timeSlider.setMaximum(100)
        self._timeSlider.setProperty("value", 0)
        self._timeSlider.setClassName("dark:handle/bg-white dark:track/active:bg-white")

        self._totalTimeLabel = LabelWithDefaultText()
        self._totalTimeLabel.setFixedWidth(60)
        self._totalTimeLabel.setFont(Factory.createFont(size=9))
        self._totalTimeLabel.setClassName("text-black dark:text-white")
        self._totalTimeLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self._middle.addWidget(self._playingTimeLabel)
        self._middle.addWidget(self._timeSlider)
        self._middle.addWidget(self._totalTimeLabel)

        # ======================================== RIGHT ========================================
        self._loopBtn = Factory.createToggleButton(Icons.LARGE, Paddings.RELATIVE_50)
        self._loopBtn.setActiveIcon(Icons.LOOP.withColor(Colors.PRIMARY), Icons.LOOP.withColor(Colors.WHITE))
        self._loopBtn.setInactiveIcon(Icons.LOOP.withColor(Colors.GRAY), Icons.LOOP.withColor(Colors.GRAY))
        self._loopBtn.setClassName(
            "rounded-full bg-none active/hover:bg-primary-12 inactive/hover:bg-gray-12",
            "dark:inactive/hover:bg-white-20"
        )
        self._loopBtn.setActive(False)

        self._shuffleBtn = Factory.createToggleButton(Icons.LARGE, Paddings.RELATIVE_50)
        self._shuffleBtn.setActiveIcon(Icons.SHUFFLE.withColor(Colors.PRIMARY), Icons.SHUFFLE.withColor(Colors.WHITE))
        self._shuffleBtn.setInactiveIcon(Icons.SHUFFLE.withColor(Colors.GRAY), Icons.SHUFFLE.withColor(Colors.GRAY))
        self._shuffleBtn.setClassName(
            "rounded-full bg-none active/hover:bg-primary-12 inactive/hover:bg-gray-12",
            "dark:inactive/hover:bg-white-20"
        )
        self._shuffleBtn.setActive(False)

        self._loveBtn = Factory.createToggleButton(Icons.LARGE, Paddings.RELATIVE_50)
        self._loveBtn.setActiveIcon(Icons.LOVE.withColor(Colors.DANGER))
        self._loveBtn.setInactiveIcon(Icons.LOVE.withColor(Colors.GRAY))
        self._loveBtn.setClassName(
            "rounded-full bg-none active/hover:bg-danger-12 inactive/hover:bg-gray-12",
            "dark:inactive/hover:bg-white-20 dark:active/hover:bg-danger-20"
        )
        self._loveBtn.setActive(False)

        self._volumeBtn = Factory.createMultiStatesButton(Icons.LARGE, Paddings.RELATIVE_50)
        self._volumeBtn.setIcons([
            StateIcon(Icons.VOLUME_UP.withColor(Colors.PRIMARY), Icons.VOLUME_UP.withColor(Colors.WHITE)),
            StateIcon(Icons.VOLUME_DOWN.withColor(Colors.PRIMARY), Icons.VOLUME_DOWN.withColor(Colors.WHITE)),
            StateIcon(Icons.VOLUME_SILENT.withColor(Colors.PRIMARY), Icons.VOLUME_SILENT.withColor(Colors.WHITE)),
        ])
        self._volumeBtn.setClassName("rounded-full bg-none hover:bg-primary-12 dark:hover:bg-white-20")
        self._volumeBtn.setChangeStateOnPressed(False)
        self._volumeBtn.setActiveState(0)

        self._volumeBox = QWidget()
        self._volumeBoxLayout = QHBoxLayout(self._volumeBox)
        self._volumeBoxLayout.setContentsMargins(0, 0, 0, 0)

        self._volumeSlider = HorizontalSlider()
        self._volumeSlider.setFixedHeight(40)
        self._volumeSlider.setPageStep(0)
        self._volumeSlider.setMaximum(100)
        self._volumeSlider.setProperty("value", 0)
        self._volumeSlider.setSliderPosition(100)
        self._volumeSlider.setClassName("rounded-8 bg-primary-10 dark:bg-white-20 dark:handle/bg-white dark:track/active:bg-white")
        self._volumeSlider.hide()

        self._volumeBoxLayout.addWidget(self._volumeSlider)

        self._timerBtn = Factory.createIconButton(size=Icons.LARGE, padding=Paddings.RELATIVE_50)
        self._timerBtn.setLightModeIcon(Icons.TIMER.withColor(Colors.PRIMARY))
        self._timerBtn.setDarkModeIcon(Icons.TIMER.withColor(Colors.WHITE))
        self._timerBtn.setClassName("bg-none hover:bg-primary-10 rounded-full", "dark:bg-none dark:hover:bg-white-20")

        self._right.addWidget(self._loopBtn)
        self._right.addWidget(self._shuffleBtn)
        self._right.addWidget(self._loveBtn)
        self._right.addWidget(self._volumeBtn)
        self._right.addWidget(self._volumeBox, 1)
        self._right.addWidget(self._timerBtn)

    def _createThreads(self):
        self._playerTrackingThread = PlayerTrackingThread(self)

    def _connectSignalSlots(self) -> None:
        self._volumeBtn.clicked.connect(lambda: self._volumeSlider.setVisible(not self._volumeSlider.isVisible()))
        self._timeSlider.sliderPressed.connect(lambda: self.__setCanRunTimeSlider(False))
        self._timeSlider.sliderReleased.connect(lambda: self.__setCanRunTimeSlider(True))

        self._playSongBtn.clicked.connect(lambda: musicPlayer.play())
        self._pauseSongBtn.clicked.connect(lambda: musicPlayer.pause())
        self._prevSongBtn.clicked.connect(lambda: musicPlayer.playPreviousSong())
        self._nextSongBtn.clicked.connect(lambda: musicPlayer.playNextSong())
        self._timeSlider.sliderReleased.connect(lambda: self.__skipTo(self._timeSlider.sliderPosition()))
        self._loopBtn.clicked.connect(lambda: musicPlayer.setLooping(self._loopBtn.isActive()))
        self._shuffleBtn.clicked.connect(lambda: musicPlayer.setShuffle(self._shuffleBtn.isActive()))
        self._volumeSlider.valueChanged.connect(lambda: musicPlayer.setVolume(self._volumeSlider.value()))

        musicPlayer.played.connect(lambda: self.__setPLaying(True))
        musicPlayer.paused.connect(lambda: self.__setPLaying(False))

        musicPlayer.played.connect(lambda: self._playerTrackingThread.start())
        musicPlayer.paused.connect(lambda: self._playerTrackingThread.quit())
        musicPlayer.songChanged.connect(lambda song: self.__selectSong(song))
        musicPlayer.loopChanged.connect(lambda a0: self._loopBtn.setActive(a0))
        musicPlayer.shuffleChanged.connect(lambda a0: self._shuffleBtn.setActive(a0))
        musicPlayer.volumeChanged.connect(lambda volume: self.__changeVolumeIcon(volume))

    def _assignShortcuts(self) -> None:
        play_shortcut = QShortcut(QKeySequence(Qt.Key_Space), self._playSongBtn)
        play_shortcut.activated.connect(self._playSongBtn.click)

        pause_shortcut = QShortcut(QKeySequence(Qt.Key_Space), self._pauseSongBtn)
        pause_shortcut.activated.connect(self._pauseSongBtn.click)

        prev_shortcut = QShortcut(QKeySequence(Qt.Key_Left), self._prevSongBtn)
        prev_shortcut.activated.connect(self._prevSongBtn.click)

        next_shortcut = QShortcut(QKeySequence(Qt.Key_Right), self._nextSongBtn)
        next_shortcut.activated.connect(self._nextSongBtn.click)

        shortcut_0 = QShortcut(QKeySequence(Qt.Key_0), self._timeSlider)
        shortcut_0.activated.connect(lambda: self.__skipTo(0))

        shortcut_1 = QShortcut(QKeySequence(Qt.Key_1), self._timeSlider)
        shortcut_1.activated.connect(lambda: self.__skipTo(10))

        shortcut_2 = QShortcut(QKeySequence(Qt.Key_2), self._timeSlider)
        shortcut_2.activated.connect(lambda: self.__skipTo(20))

        shortcut_3 = QShortcut(QKeySequence(Qt.Key_3), self._timeSlider)
        shortcut_3.activated.connect(lambda: self.__skipTo(30))

        shortcut_4 = QShortcut(QKeySequence(Qt.Key_4), self._timeSlider)
        shortcut_4.activated.connect(lambda: self.__skipTo(40))

        shortcut_5 = QShortcut(QKeySequence(Qt.Key_5), self._timeSlider)
        shortcut_5.activated.connect(lambda: self.__skipTo(50))

        shortcut_6 = QShortcut(QKeySequence(Qt.Key_6), self._timeSlider)
        shortcut_6.activated.connect(lambda: self.__skipTo(60))

        shortcut_7 = QShortcut(QKeySequence(Qt.Key_7), self._timeSlider)
        shortcut_7.activated.connect(lambda: self.__skipTo(70))

        shortcut_8 = QShortcut(QKeySequence(Qt.Key_8), self._timeSlider)
        shortcut_8.activated.connect(lambda: self.__skipTo(80))

        shortcut_9 = QShortcut(QKeySequence(Qt.Key_9), self._timeSlider)
        shortcut_9.activated.connect(lambda: self.__skipTo(90))

    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self._mainLayout.setContentsMargins(left, top, right, bottom)

    def __skipTo(self, position: int) -> None:
        self._timeSlider.setValue(position)
        try:
            musicPlayer.skipToTime(musicPlayer.getCurrentSong().getLength() * position / 100)
            musicPlayer.play()
        except AttributeError:
            self._timeSlider.setValue(0)

    def setDefaultCover(self, cover: bytes) -> None:
        self._songCover.setDefaultCover(self.__createCover(cover))

    @staticmethod
    def __createCover(data: bytes) -> Union[CoverProps, None]:
        if data is None:
            return None
        return CoverProps.fromBytes(data, width=64, height=64, radius=12)

    def __setPLaying(self, isPlaying: bool) -> None:
        self._playSongBtn.setVisible(not isPlaying)
        self._pauseSongBtn.setVisible(isPlaying)

    def setTotalTime(self, time: float) -> None:
        self.__songLength = time
        self._totalTimeLabel.setText(Times.toString(time))

    def setPlayingTime(self, time: float) -> None:
        if not self.__canRunTimeSlider:
            return
        self._playingTimeLabel.setText(Times.toString(time))
        position = 0 if self.__songLength == 0 else int(time * 100 / self.__songLength)
        self._timeSlider.setSliderPosition(position)

    def __setCanRunTimeSlider(self, enable: bool) -> None:
        self.__canRunTimeSlider = enable

    def __selectSong(self, song: Song) -> None:
        if self.__currentSong is not None:
            self.__currentSong.loved.disconnect(self.__updateLoveState)
            with contextlib.suppress(RuntimeError):
                self._loveBtn.clicked.disconnect()

        self.__currentSong = song

        self.setTotalTime(song.getLength())
        self._titleLabel.setText(song.getTitle())
        self._artistLabel.setText(song.getArtist())
        self._songCover.setCover(self.__createCover(song.getCover()))
        self.__updateLoveState(song.isLoved())

        # Connect signals
        song.loved.connect(self.__updateLoveState)
        self._loveBtn.clicked.connect(lambda: self.__currentSong.changeLoveState(self._loveBtn.isActive()))

    def __aa(self):
        return self.__currentSong.changeLoveState(self._loveBtn.isActive())

    def __updateLoveState(self, state: bool) -> None:
        self._loveBtn.setActive(state)

    def __changeVolumeIcon(self, volume: int) -> None:
        VOLUME_UP_STATE: int = 0
        VOLUME_DOWN_STATE: int = 1
        SILENT_STATE: int = 2
        state = SILENT_STATE

        if 0 < volume <= 33:
            state = VOLUME_DOWN_STATE
        if 33 < volume <= 100:
            state = VOLUME_UP_STATE
        self._volumeBtn.setActiveState(state)


class PlayerTrackingThread(QThread):

    def __init__(self, musicPlayerUI: MusicPlayerBar) -> None:
        super().__init__()
        self.__musicPlayerUI = musicPlayerUI

    def run(self) -> None:
        interval: float = musicPlayer.refreshRate()

        while musicPlayer.isPlaying():
            self.__musicPlayerUI.setPlayingTime(musicPlayer.getPlayingTime())
            sleep(interval)
