import contextlib
from time import sleep
from typing import Optional

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QShortcut

from app.common.models import Song
from app.common.others import musicPlayer, translator
from app.common.statics.qt import Icons
from app.common.statics.styles import Colors
from app.common.statics.styles import Paddings
from app.components.base import Component, FontFactory
from app.components.buttons import ButtonFactory, StateIcon
from app.components.events import SignalConnector
from app.components.labels import Label
from app.components.sliders import HorizontalSlider
from app.components.widgets import Box, FlexBox
from app.utils.others import Times
from app.utils.qt import Widgets
from app.utils.reflections import suppressException
from app.views.windows.main_window.player_bar.timer_dialog import TimerDialog


class MusicPlayerBar(QWidget, Component):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.__songLength: float = 0
        self.__canRunTimeSlider = True
        self.__currentSong: Optional[Song] = None

        super()._initComponent()

        self._loopBtn.setActive(musicPlayer.isLooping())
        self._shuffleBtn.setActive(musicPlayer.isShuffle())
        self.setPlayingTime(musicPlayer.getPlayingTime())
        self._playSongBtn.setVisible(not musicPlayer.isPlaying())
        self._pauseSongBtn.setVisible(musicPlayer.isPlaying())

        song = musicPlayer.getCurrentSong()
        if song is None:
            self.setTotalTime(0)
            self._loveBtn.setActive(False)
        else:
            self.__selectSong(song)

        if musicPlayer.isPlaying():
            self._playerTrackingThread.start()

    def _createUI(self) -> None:
        self.setAttribute(Qt.WA_StyledBackground)

        self._mainLayout = Box(self)
        self.setLayout(self._mainLayout)

        self._upperLayout = FlexBox()
        self._upperLayout.setContentsMargins(8, 0, 8, 0)
        self._lowerLayout = FlexBox()

        self._mainLayout.addLayout(self._upperLayout)
        self._mainLayout.addSpacing(8)
        self._mainLayout.addLayout(self._lowerLayout)

        self._left = QWidget()
        self._left.setFixedWidth(180)

        self._leftLayout = FlexBox(self._left)
        self._leftLayout.setContentsMargins(4, 0, 0, 0)
        self._leftLayout.setSpacing(12)
        self._leftLayout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self._middle = QWidget()
        self._middleLayout = FlexBox(self._middle)
        self._middleLayout.setSpacing(8)
        self._middleLayout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self._right = QWidget()
        self._right.setFixedWidth(180)

        self._rightLayout = FlexBox(self._right)
        self._rightLayout.setContentsMargins(0, 0, 0, 0)
        self._rightLayout.setSpacing(8)
        self._rightLayout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self._lowerLayout.addWidget(self._left)
        self._lowerLayout.addStretch()
        self._lowerLayout.addWidget(self._middle, alignment=Qt.AlignHCenter)
        self._lowerLayout.addStretch()
        self._lowerLayout.addWidget(self._right)

        # ======================================== UPPER ========================================
        self._playingTimeLabel = Label()
        self._playingTimeLabel.setFixedWidth(48)
        self._playingTimeLabel.setFont(FontFactory.create(size=9))
        self._playingTimeLabel.setClassName("text-black dark:text-white bg-none")
        self._playingTimeLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self._timeSlider = HorizontalSlider()
        self._timeSlider.setFixedHeight(12)
        self._timeSlider.setSliderSize(handle=10)
        self._timeSlider.setPageStep(0)
        self._timeSlider.setMaximum(100)
        self._timeSlider.setProperty("value", 0)
        self._timeSlider.setClassName("dark:handle/bg-white dark:track/active:bg-white")

        self._totalTimeLabel = Label()
        self._totalTimeLabel.setFixedWidth(48)
        self._totalTimeLabel.setFont(FontFactory.create(size=9))
        self._totalTimeLabel.setClassName("text-black dark:text-white bg-none")
        self._totalTimeLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self._upperLayout.addWidget(self._playingTimeLabel)
        self._upperLayout.addWidget(self._timeSlider, stretch=1)
        self._upperLayout.addWidget(self._totalTimeLabel)

        # ======================================== LEFT ========================================
        self.volumeBtn = ButtonFactory.createMultiStatesButton(Icons.large, Paddings.relative50)
        self.volumeBtn.setIcons([
            StateIcon(Icons.volumeUp.withColor(Colors.primary), Icons.volumeUp.withColor(Colors.white)),
            StateIcon(Icons.volumeDown.withColor(Colors.primary), Icons.volumeDown.withColor(Colors.white)),
            StateIcon(Icons.volumeSilent.withColor(Colors.primary), Icons.volumeSilent.withColor(Colors.white)),
        ])

        self.volumeBtn.setClassName("rounded-full bg-none hover:bg-primary-12 dark:hover:bg-white-20")
        self.volumeBtn.setChangeStateOnPressed(False)
        self.volumeBtn.setActiveState(0)

        self._leftLayout.addWidget(self.volumeBtn)

        # ======================================== MIDDLE ========================================

        self._prevSongBtn = ButtonFactory.createIconButton(size=Icons.large, padding=Paddings.relative50)
        self._prevSongBtn.setLightModeIcon(Icons.previous.withColor(Colors.primary))
        self._prevSongBtn.setDarkModeIcon(Icons.previous.withColor(Colors.white))
        self._prevSongBtn.setClassName("hover:bg-primary-10 bg-none rounded-full", "dark:bg-none dark:hover:bg-white-20")

        self._playSongBtn = ButtonFactory.createIconButton(size=Icons.xLarge, padding=Paddings.relative50)
        self._playSongBtn.setLightModeIcon(Icons.play.withColor(Colors.primary))
        self._playSongBtn.setDarkModeIcon(Icons.play.withColor(Colors.white))
        self._playSongBtn.setClassName("hover:bg-primary-25 bg-primary-10 rounded-full", "dark:bg-primary dark:hover:bg-primary")

        self._pauseSongBtn = ButtonFactory.createIconButton(size=Icons.xLarge, padding=Paddings.relative50)
        self._pauseSongBtn.setLightModeIcon(Icons.pause.withColor(Colors.primary))
        self._pauseSongBtn.setDarkModeIcon(Icons.pause.withColor(Colors.white))
        self._pauseSongBtn.setClassName("hover:bg-primary-25 bg-primary-10 rounded-full", "dark:bg-primary dark:hover:bg-primary")
        self._pauseSongBtn.hide()

        self._nextSongBtn = ButtonFactory.createIconButton(size=Icons.large, padding=Paddings.relative50)
        self._nextSongBtn.setLightModeIcon(Icons.next.withColor(Colors.primary))
        self._nextSongBtn.setDarkModeIcon(Icons.next.withColor(Colors.white))
        self._nextSongBtn.setClassName("hover:bg-primary-10 bg-none rounded-full", "dark:bg-none dark:hover:bg-white-20")

        self._shuffleBtn = ButtonFactory.createToggleButton(Icons.large, Paddings.relative50)
        self._shuffleBtn.setActiveIcon(Icons.shuffle.withColor(Colors.primary), Icons.shuffle.withColor(Colors.white))
        self._shuffleBtn.setInactiveIcon(Icons.shuffle.withColor(Colors.gray), Icons.shuffle.withColor(Colors.gray))
        self._shuffleBtn.setClassName(
            "rounded-full bg-none active/hover:bg-primary-12 inactive/hover:bg-gray-12",
            "dark:inactive/hover:bg-white-20 dark:active/hover:bg-white-20"
        )

        self._loopBtn = ButtonFactory.createToggleButton(Icons.large, Paddings.relative50)
        self._loopBtn.setActiveIcon(Icons.loop.withColor(Colors.primary), Icons.loop.withColor(Colors.white))
        self._loopBtn.setInactiveIcon(Icons.loop.withColor(Colors.gray), Icons.loop.withColor(Colors.gray))
        self._loopBtn.setClassName(
            "rounded-full bg-none active/hover:bg-primary-12 inactive/hover:bg-gray-12",
            "dark:inactive/hover:bg-white-20 dark:active/hover:bg-white-20"
        )

        self._middleLayout.addWidget(self._shuffleBtn)
        self._middleLayout.addWidget(self._prevSongBtn)
        self._middleLayout.addWidget(self._playSongBtn)
        self._middleLayout.addWidget(self._pauseSongBtn)
        self._middleLayout.addWidget(self._nextSongBtn)
        self._middleLayout.addWidget(self._loopBtn)

        # ======================================== RIGHT ========================================

        self._loveBtn = ButtonFactory.createToggleButton(Icons.large, Paddings.relative50)
        self._loveBtn.setActiveIcon(Icons.loved.withColor(Colors.danger))
        self._loveBtn.setInactiveIcon(Icons.love.withColor(Colors.gray))
        self._loveBtn.setClassName(
            "rounded-full bg-none active/hover:bg-danger-12 inactive/hover:bg-gray-12",
            "dark:inactive/hover:bg-white-20 dark:active/hover:bg-danger-20"
        )

        self._timerBtn = ButtonFactory.createIconButton(size=Icons.large, padding=Paddings.relative50)
        self._timerBtn.setLightModeIcon(Icons.timer.withColor(Colors.primary))
        self._timerBtn.setDarkModeIcon(Icons.timer.withColor(Colors.white))
        self._timerBtn.setClassName("bg-none hover:bg-primary-10 rounded-full", "dark:bg-none dark:hover:bg-white-20")

        self._rightLayout.addWidget(self._loveBtn)
        self._rightLayout.addWidget(self._timerBtn)

        self._timerDialog = None
        self._signalConnector = SignalConnector(self)

    def _createThreads(self):
        self._playerTrackingThread = PlayerTrackingThread(self)

    def translateUI(self) -> None:
        self._prevSongBtn.setToolTip(f'{translator.translate("MUSIC_PLAYER.TOOLTIP_PREV_BTN")} (Ctrl + ←)')
        self._nextSongBtn.setToolTip(f'{translator.translate("MUSIC_PLAYER.TOOLTIP_NEXT_BTN")} (Ctrl + →)')
        self._pauseSongBtn.setToolTip(f'{translator.translate("MUSIC_PLAYER.TOOLTIP_PAUSE_BTN")} (Ctrl + Space)')
        self._playSongBtn.setToolTip(f'{translator.translate("MUSIC_PLAYER.TOOLTIP_PLAY_BTN")} (Ctrl + Space)')

        self._loopBtn.setToolTips([
            translator.translate("MUSIC_PLAYER.TOOLTIP_UN_LOOP_BTN"),
            translator.translate("MUSIC_PLAYER.TOOLTIP_LOOP_BTN")
        ])

        self._shuffleBtn.setToolTips([
            translator.translate("MUSIC_PLAYER.TOOLTIP_UN_SHUFFLE_BTN"),
            translator.translate("MUSIC_PLAYER.TOOLTIP_SHUFFLE_BTN")
        ])

        self._loveBtn.setToolTips([
            translator.translate("MUSIC_PLAYER.TOOLTIP_UN_LOVE_BTN"),
            translator.translate("MUSIC_PLAYER.TOOLTIP_LOVE_BTN")
        ])

        self.volumeBtn.setToolTips([
            translator.translate("MUSIC_PLAYER.TOOLTIP_VOLUME_BTN"),
            translator.translate("MUSIC_PLAYER.TOOLTIP_VOLUME_BTN"),
            translator.translate("MUSIC_PLAYER.TOOLTIP_VOLUME_BTN"),
        ])

        self._timerBtn.setToolTip(translator.translate("MUSIC_PLAYER.TOOLTIP_TIMER_BTN"))

    def _connectSignalSlots(self) -> None:
        self._timeSlider.sliderPressed.connect(lambda: self.__setCanRunTimeSlider(False))
        self._timeSlider.sliderReleased.connect(lambda: self.__setCanRunTimeSlider(True))

        self._playSongBtn.clicked.connect(lambda: musicPlayer.play())
        self._pauseSongBtn.clicked.connect(lambda: musicPlayer.pause())
        self._prevSongBtn.clicked.connect(lambda: musicPlayer.playPreviousSong())
        self._nextSongBtn.clicked.connect(lambda: musicPlayer.playNextSong())
        self._timeSlider.sliderReleased.connect(lambda: self.__skipTo(self._timeSlider.sliderPosition()))
        self._loopBtn.clicked.connect(lambda: musicPlayer.setLooping(self._loopBtn.isActive()))
        self._shuffleBtn.clicked.connect(lambda: musicPlayer.setShuffle(self._shuffleBtn.isActive()))
        self._timerBtn.clicked.connect(lambda: self.__openTimer())

        self._signalConnector.connect(musicPlayer.played, lambda: self.__setPLaying(True))
        self._signalConnector.connect(musicPlayer.paused, lambda: self.__setPLaying(False))

        self._signalConnector.connect(musicPlayer.played, lambda: self._playerTrackingThread.start())
        self._signalConnector.connect(musicPlayer.paused, lambda: self._playerTrackingThread.quit())
        self._signalConnector.connect(musicPlayer.songChanged, lambda song: self.__selectSong(song))
        self._signalConnector.connect(musicPlayer.loopChanged, lambda a0: self._loopBtn.setActive(a0))
        self._signalConnector.connect(musicPlayer.shuffleChanged, lambda a0: self._shuffleBtn.setActive(a0))
        self._signalConnector.connect(musicPlayer.volumeChanged, lambda volume: self.__changeVolumeIcon(volume))

    def _assignShortcuts(self) -> None:
        playShortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Space), self._playSongBtn)
        playShortcut.activated.connect(lambda: self._playSongBtn.click())

        pauseShortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Space), self._pauseSongBtn)
        pauseShortcut.activated.connect(lambda: self._pauseSongBtn.click())

        prevShortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Left), self._prevSongBtn)
        prevShortcut.activated.connect(lambda: self._prevSongBtn.click())

        nextShortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Right), self._nextSongBtn)
        nextShortcut.activated.connect(lambda: self._nextSongBtn.click())

        shortcut0 = QShortcut(QKeySequence(Qt.Key_0), self._timeSlider)
        shortcut0.activated.connect(lambda: self.__skipTo(0))

        shortcut1 = QShortcut(QKeySequence(Qt.Key_1), self._timeSlider)
        shortcut1.activated.connect(lambda: self.__skipTo(10))

        shortcut2 = QShortcut(QKeySequence(Qt.Key_2), self._timeSlider)
        shortcut2.activated.connect(lambda: self.__skipTo(20))

        shortcut3 = QShortcut(QKeySequence(Qt.Key_3), self._timeSlider)
        shortcut3.activated.connect(lambda: self.__skipTo(30))

        shortcut4 = QShortcut(QKeySequence(Qt.Key_4), self._timeSlider)
        shortcut4.activated.connect(lambda: self.__skipTo(40))

        shortcut5 = QShortcut(QKeySequence(Qt.Key_5), self._timeSlider)
        shortcut5.activated.connect(lambda: self.__skipTo(50))

        shortcut6 = QShortcut(QKeySequence(Qt.Key_6), self._timeSlider)
        shortcut6.activated.connect(lambda: self.__skipTo(60))

        shortcut7 = QShortcut(QKeySequence(Qt.Key_7), self._timeSlider)
        shortcut7.activated.connect(lambda: self.__skipTo(70))

        shortcut8 = QShortcut(QKeySequence(Qt.Key_8), self._timeSlider)
        shortcut8.activated.connect(lambda: self.__skipTo(80))

        shortcut9 = QShortcut(QKeySequence(Qt.Key_9), self._timeSlider)
        shortcut9.activated.connect(lambda: self.__skipTo(90))

    @suppressException
    def __skipTo(self, position: int) -> None:
        self._timeSlider.setValue(position)
        try:
            musicPlayer.skipToTime(musicPlayer.getCurrentSong().getLength() * position / 100)
        except AttributeError:
            self._timeSlider.setValue(0)

    @suppressException
    def __setPLaying(self, isPlaying: bool) -> None:
        self._playSongBtn.setVisible(not isPlaying)
        self._pauseSongBtn.setVisible(isPlaying)

    @suppressException
    def setTotalTime(self, time: float) -> None:
        self.__songLength = time
        self._totalTimeLabel.setText(Times.toString(time))

    @suppressException
    def setPlayingTime(self, time: float) -> None:
        if not self.__canRunTimeSlider:
            return

        if Widgets.isDeleted(self._playingTimeLabel):
            return

        self._playingTimeLabel.setText(Times.toString(time))
        position = 0 if self.__songLength == 0 else int(time * 100 / self.__songLength)
        self._timeSlider.setSliderPosition(position)

    @suppressException
    def __setCanRunTimeSlider(self, enable: bool) -> None:
        self.__canRunTimeSlider = enable

    @suppressException
    def __selectSong(self, song: Song) -> None:
        if self.__currentSong is not None:
            self.__currentSong.loved.disconnect(self.__updateLoveState)
            with contextlib.suppress(RuntimeError):
                self._loveBtn.clicked.disconnect()

        self.__currentSong = song

        # Connect signals
        song.loved.connect(self.__updateLoveState)
        self._loveBtn.clicked.connect(lambda: self.__currentSong.updateLoveState(self._loveBtn.isActive()))

        # Display song information
        self.setTotalTime(song.getLength())
        self.__updateLoveState(song.isLoved())

    @suppressException
    def __updateLoveState(self, state: bool) -> None:
        self._loveBtn.setActive(state)

    @suppressException
    def __changeVolumeIcon(self, volume: int) -> None:
        VOLUME_UP_STATE: int = 0
        VOLUME_DOWN_STATE: int = 1
        SILENT_STATE: int = 2
        state = SILENT_STATE

        if 0 < volume <= 33:
            state = VOLUME_DOWN_STATE
        if 33 < volume <= 100:
            state = VOLUME_UP_STATE
        self.volumeBtn.setActiveState(state)

    @suppressException
    def __openTimer(self) -> None:
        if self._timerDialog is None:
            self._timerDialog = TimerDialog()
        self._timerDialog.show()

    def close(self) -> bool:
        return super().close()


class PlayerTrackingThread(QThread):

    def __init__(self, musicPlayerUI: MusicPlayerBar) -> None:
        super().__init__()
        self.__musicPlayerUI = musicPlayerUI

    @suppressException
    def run(self) -> None:
        interval: float = musicPlayer.refreshRate()

        while musicPlayer.isPlaying() and not Widgets.isDeleted(self.__musicPlayerUI):
            self.__musicPlayerUI.setPlayingTime(musicPlayer.getPlayingTime())
            sleep(interval)
