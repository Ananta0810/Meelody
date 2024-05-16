import contextlib
from time import sleep
from typing import Optional

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QShortcut

from app.common.models import Song
from app.common.others import musicPlayer, translator
from app.common.statics.qt import Images, Icons
from app.common.statics.styles import Colors
from app.common.statics.styles import Paddings
from app.components.base import Component, FontFactory
from app.components.buttons import ButtonFactory, StateIcon
from app.components.dialogs import Dialogs
from app.components.images.cover import CoverWithPlaceHolder, Cover
from app.components.labels import LabelWithPlaceHolder, Label
from app.components.sliders import HorizontalSlider
from app.utils.others import Times
from app.views.windows.main_window.player_bar.timer_dialog import TimerDialog


class MusicPlayerBar(QWidget, Component):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.__songLength: float = 0
        self.__canRunTimeSlider = True
        self.__currentSong: Optional[Song] = None

        super()._initComponent()

        self._songCover.setPlaceHolderCover(self.__createCover(Images.defaultSongCover))
        self.setPlayingTime(0)
        self.setTotalTime(0)
        self._loopBtn.setActive(musicPlayer.isLooping())
        self._shuffleBtn.setActive(musicPlayer.isShuffle())
        self._volumeSlider.setValue(musicPlayer.getVolume())

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
        self._songCover = CoverWithPlaceHolder()
        self._songCover.setFixedSize(64, 64)

        self._titleLabel = LabelWithPlaceHolder()
        self._titleLabel.enableEllipsis()
        self._titleLabel.setFixedWidth(128)
        self._titleLabel.setFont(FontFactory.create(size=10, bold=True))
        self._titleLabel.setClassName("text-black dark:text-white bg-none")

        self._artistLabel = LabelWithPlaceHolder()
        self._artistLabel.enableEllipsis()
        self._artistLabel.setFixedWidth(128)
        self._artistLabel.setFont(FontFactory.create(size=9))
        self._artistLabel.setClassName("text-black dark:text-gray bg-none")

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

        self._playButtons.addWidget(self._prevSongBtn)
        self._playButtons.addWidget(self._playSongBtn)
        self._playButtons.addWidget(self._pauseSongBtn)
        self._playButtons.addWidget(self._nextSongBtn)

        self._left.addWidget(self._songCover)
        self._left.addLayout(self._infoLayout, stretch=1)
        self._left.addLayout(self._playButtons)

        # ======================================== MIDDLE ========================================
        self._playingTimeLabel = Label()
        self._playingTimeLabel.setFixedWidth(60)
        self._playingTimeLabel.setFont(FontFactory.create(size=9))
        self._playingTimeLabel.setClassName("text-black dark:text-white bg-none")
        self._playingTimeLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self._timeSlider = HorizontalSlider()
        self._timeSlider.setFixedWidth(250)
        self._timeSlider.setFixedHeight(12)
        self._timeSlider.setSliderSize(handle=10)
        self._timeSlider.setPageStep(0)
        self._timeSlider.setMaximum(100)
        self._timeSlider.setProperty("value", 0)
        self._timeSlider.setClassName("dark:handle/bg-white dark:track/active:bg-white")

        self._totalTimeLabel = Label()
        self._totalTimeLabel.setFixedWidth(60)
        self._totalTimeLabel.setFont(FontFactory.create(size=9))
        self._totalTimeLabel.setClassName("text-black dark:text-white bg-none")
        self._totalTimeLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self._middle.addWidget(self._playingTimeLabel)
        self._middle.addWidget(self._timeSlider)
        self._middle.addWidget(self._totalTimeLabel)

        # ======================================== RIGHT ========================================
        self._loopBtn = ButtonFactory.createToggleButton(Icons.large, Paddings.relative50)
        self._loopBtn.setActiveIcon(Icons.loop.withColor(Colors.primary), Icons.loop.withColor(Colors.white))
        self._loopBtn.setInactiveIcon(Icons.loop.withColor(Colors.gray), Icons.loop.withColor(Colors.gray))
        self._loopBtn.setClassName(
            "rounded-full bg-none active/hover:bg-primary-12 inactive/hover:bg-gray-12",
            "dark:inactive/hover:bg-white-20 dark:active/hover:bg-white-20"
        )
        self._loopBtn.setActive(False)

        self._shuffleBtn = ButtonFactory.createToggleButton(Icons.large, Paddings.relative50)
        self._shuffleBtn.setActiveIcon(Icons.shuffle.withColor(Colors.primary), Icons.shuffle.withColor(Colors.white))
        self._shuffleBtn.setInactiveIcon(Icons.shuffle.withColor(Colors.gray), Icons.shuffle.withColor(Colors.gray))
        self._shuffleBtn.setClassName(
            "rounded-full bg-none active/hover:bg-primary-12 inactive/hover:bg-gray-12",
            "dark:inactive/hover:bg-white-20 dark:active/hover:bg-white-20"
        )
        self._shuffleBtn.setActive(False)

        self._loveBtn = ButtonFactory.createToggleButton(Icons.large, Paddings.relative50)
        self._loveBtn.setActiveIcon(Icons.loved.withColor(Colors.danger))
        self._loveBtn.setInactiveIcon(Icons.love.withColor(Colors.gray))
        self._loveBtn.setClassName(
            "rounded-full bg-none active/hover:bg-danger-12 inactive/hover:bg-gray-12",
            "dark:inactive/hover:bg-white-20 dark:active/hover:bg-danger-20"
        )
        self._loveBtn.setActive(False)

        self._volumeBtn = ButtonFactory.createMultiStatesButton(Icons.large, Paddings.relative50)
        self._volumeBtn.setIcons([
            StateIcon(Icons.volumeUp.withColor(Colors.primary), Icons.volumeUp.withColor(Colors.white)),
            StateIcon(Icons.volumeDown.withColor(Colors.primary), Icons.volumeDown.withColor(Colors.white)),
            StateIcon(Icons.volumeSilent.withColor(Colors.primary), Icons.volumeSilent.withColor(Colors.white)),
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

        self._timerBtn = ButtonFactory.createIconButton(size=Icons.large, padding=Paddings.relative50)
        self._timerBtn.setLightModeIcon(Icons.timer.withColor(Colors.primary))
        self._timerBtn.setDarkModeIcon(Icons.timer.withColor(Colors.white))
        self._timerBtn.setClassName("bg-none hover:bg-primary-10 rounded-full", "dark:bg-none dark:hover:bg-white-20")

        self._right.addWidget(self._loopBtn)
        self._right.addWidget(self._shuffleBtn)
        self._right.addWidget(self._loveBtn)
        self._right.addWidget(self._volumeBtn)
        self._right.addWidget(self._volumeBox, 1)
        self._right.addWidget(self._timerBtn)

        self._timerDialog = None

    def _createThreads(self):
        self._playerTrackingThread = PlayerTrackingThread(self)

    def translateUI(self) -> None:
        self._titleLabel.setPlaceHolder(translator.translate("MUSIC_PLAYER.SONG_TITLE"))
        self._artistLabel.setPlaceHolder(translator.translate("MUSIC_PLAYER.SONG_ARTIST"))

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

        self._volumeBtn.setToolTips([
            translator.translate("MUSIC_PLAYER.TOOLTIP_VOLUME_BTN"),
            translator.translate("MUSIC_PLAYER.TOOLTIP_VOLUME_BTN"),
            translator.translate("MUSIC_PLAYER.TOOLTIP_VOLUME_BTN"),
        ])

        self._timerBtn.setToolTip(translator.translate("MUSIC_PLAYER.TOOLTIP_TIMER_BTN"))

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
        self._timerBtn.clicked.connect(lambda: self.__openTimer())

        musicPlayer.loadFailed.connect(lambda: self.__notifySongNotFound())
        musicPlayer.played.connect(lambda: self.__setPLaying(True))
        musicPlayer.paused.connect(lambda: self.__setPLaying(False))

        musicPlayer.played.connect(lambda: self._playerTrackingThread.start())
        musicPlayer.paused.connect(lambda: self._playerTrackingThread.quit())
        musicPlayer.songChanged.connect(lambda song: self.__selectSong(song))
        musicPlayer.loopChanged.connect(lambda a0: self._loopBtn.setActive(a0))
        musicPlayer.shuffleChanged.connect(lambda a0: self._shuffleBtn.setActive(a0))
        musicPlayer.volumeChanged.connect(lambda volume: self.__setVolume(volume))

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

    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self._mainLayout.setContentsMargins(left, top, right, bottom)

    def __skipTo(self, position: int) -> None:
        self._timeSlider.setValue(position)
        try:
            musicPlayer.skipToTime(musicPlayer.getCurrentSong().getLength() * position / 100)
        except AttributeError:
            self._timeSlider.setValue(0)

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
            self.__currentSong.coverChanged.disconnect(self.__setCover)
            with contextlib.suppress(RuntimeError):
                self._loveBtn.clicked.disconnect()

        self.__currentSong = song

        # Connect signals
        song.loved.connect(self.__updateLoveState)
        song.coverChanged.connect(self.__setCover)
        self._loveBtn.clicked.connect(lambda: self.__currentSong.updateLoveState(self._loveBtn.isActive()))

        # Display song information
        self.setTotalTime(song.getLength())
        self._titleLabel.setText(song.getTitle())
        self._artistLabel.setText(song.getArtist())
        self.__updateLoveState(song.isLoved())
        if song.isCoverLoaded():
            self.__setCover(song.getCover())
        else:
            self.__setCover(None)
            song.loadCover()

    def __setCover(self, cover: Optional[bytes]) -> None:
        self._songCover.setCover(self.__createCover(cover))

    def __updateLoveState(self, state: bool) -> None:
        self._loveBtn.setActive(state)

    def __setVolume(self, volume: int) -> None:
        VOLUME_UP_STATE: int = 0
        VOLUME_DOWN_STATE: int = 1
        SILENT_STATE: int = 2
        state = SILENT_STATE

        if 0 < volume <= 33:
            state = VOLUME_DOWN_STATE
        if 33 < volume <= 100:
            state = VOLUME_UP_STATE

        self._volumeSlider.setValue(volume)
        self._volumeBtn.setActiveState(state)

    def __openTimer(self) -> None:
        if self._timerDialog is None:
            self._timerDialog = TimerDialog()
        self._timerDialog.show()

    @staticmethod
    def __notifySongNotFound():
        return Dialogs.alert(translator.translate("MUSIC_PLAYER.PLAYING_DELETED_SONG"))

    @staticmethod
    def __createCover(data: bytes) -> Optional[Cover.Props]:
        if data is None:
            return None
        return Cover.Props.fromBytes(data, width=64, height=64, radius=12)


class PlayerTrackingThread(QThread):

    def __init__(self, musicPlayerUI: MusicPlayerBar) -> None:
        super().__init__()
        self.__musicPlayerUI = musicPlayerUI

    def run(self) -> None:
        interval: float = musicPlayer.refreshRate()

        while musicPlayer.isPlaying():
            self.__musicPlayerUI.setPlayingTime(musicPlayer.getPlayingTime())
            sleep(interval)
