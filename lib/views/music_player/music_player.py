from typing import Optional

from constants.ui.base import ApplicationImage
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QWidget
from views.view import View

from .left import MusicPlayerLeftSide
from .middle import MusicPlayerTimeSlider
from .right import MusicPlayerRightSide


class UIPlayerMusic(QWidget, View):
    def __init__(self, parent: Optional["QWidget"] = None):
        super(UIPlayerMusic, self).__init__(parent)
        self.setupUi()

    def setupUi(self) -> None:
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setContentsMargins(40, 0, 40, 0)
        self.mainLayout.setSpacing(0)

        self.left = MusicPlayerLeftSide()
        self.left.setContentsMargins(0, 0, 0, 0)
        self.left.setSpacing(12)
        self.left.setDefaultCover(ApplicationImage.defaultSongCover)
        self.mainLayout.addLayout(self.left)

        self.center = MusicPlayerTimeSlider()
        self.center.setContentsMargins(0, 0, 0, 0)
        self.center.setSpacing(4)
        self.center.displayPlayingTime(0)
        self.center.displayTotalTime(0)
        self.mainLayout.addLayout(self.center)

        self.right = MusicPlayerRightSide()
        self.right.setContentsMargins(0, 0, 0, 0)
        self.right.setSpacing(8)
        self.mainLayout.addLayout(self.right)

    def lightMode(self) -> None:
        self.left.lightMode()
        self.center.lightMode()
        self.right.lightMode()
        return super().lightMode()

    def darkMode(self) -> None:
        self.left.darkMode()
        self.center.darkMode()
        self.right.darkMode()
        return super().darkMode()

    def translate(self, language: dict) -> None:
        self.left.songTitle.setDefaultText(language.get("song_title"))
        self.left.songArtist.setDefaultText(language.get("song_artist"))
        self.right.timerInput.setPlaceholderText(language.get("enter_timer_minute"))

    def displaySongInfo(
        self, cover: bytes = None, title: str = None, artist: str = None, loveState: bool = False
    ) -> None:
        if artist is None and title is not None:
            artist = ""
        self.left.setCover(cover)
        self.left.setTitle(title)
        self.left.setArtist(artist)
        self.setLoveState(loveState)

    def isPlaying(self) -> bool:
        return self.left.isPlaying()

    def setPlayingState(self, state: bool) -> None:
        self.left.playBtn.setChecked(state)

    def displayPlayingTime(self, time: float) -> None:
        self.center.displayPlayingTime(time)

    def displayTotalTime(self, time: float) -> None:
        self.center.displayTotalTime(time)

    def getTimeSliderPosition(self) -> int:
        return self.center.getTimeSliderPosition()

    def runTimeSlider(self, currentTime: float, totalTime: float) -> None:
        self.center.runTimeSlider(currentTime, totalTime)

    def setLoopState(self, state: bool) -> None:
        self.right.setLoopState(state)

    def setShuffleState(self, state: bool) -> None:
        self.right.setShuffleState(state)

    def setLoveState(self, state: bool) -> None:
        self.right.setLoveState(state)

    def setVolume(self, volume: int) -> None:
        self.right.setVolume(volume)

    def isLooping(self) -> bool:
        return self.right.isLooping()

    def isShuffling(self) -> bool:
        return self.right.isShuffling()

    def getTimerValue(self) -> int:
        return self.right.getTimerValue()

    def getCurrentVolumeValue(self) -> int:
        return self.right.getCurrentVolumeValue()

    def connectToController(self, controller) -> None:
        self.left.prevSongBtn.clicked.connect(controller.handlePreviousSong)
        self.left.playBtn.clicked.connect(controller.handlePlaySong)
        self.left.nextSongBtn.clicked.connect(controller.handleNextSong)
        self.center.timeSlider.sliderPressed.connect(controller.handlePausedTimeSlider)
        self.center.timeSlider.sliderReleased.connect(controller.handleUnpausedTimeSlider)
        self.right.loopBtn.clicked.connect(controller.handleClickedLoop)
        self.right.shuffleBtn.clicked.connect(controller.handleClickedShuffle)
        self.right.loveBtn.clicked.connect(controller.handleLoveSong)
        self.right.volumeSlider.valueChanged.connect(controller.handleChangVolume)
        self.right.timerInput.returnPressed.connect(controller.handleEnteredTimer)
