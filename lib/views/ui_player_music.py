from typing import Optional

from constants.ui.base import ApplicationImage
from constants.ui.qss import Backgrounds, ColorBoxes, Colors, Paddings
from constants.ui.qt import AppCursors, AppIcons
from modules.screens.components.font_builder import FontBuilder
from modules.screens.components.icon_buttons import IconButton, MultiIconButton, ToggleIconButton
from modules.screens.components.labels import EditableLabel, StandardLabel
from modules.screens.components.sliders import HorizontalSlider
from modules.screens.themes.theme_builders import ButtonThemeBuilder, HorizontalSliderThemeBuilder, LabelThemeBuilder
from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtGui import QIntValidator, QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from utils.helpers.my_string import Stringify
from utils.ui.application_utils import UiUtils
from widgets.image_displayer import ImageDisplayer

from .view import View


class UIPlayerMusic(QWidget, View):
    def __init__(self, parent: Optional["QWidget"] = None):
        super(UIPlayerMusic, self).__init__(parent)
        self.setupUi()

    def setupUi(self) -> None:
        icons = AppIcons()
        cursors = AppCursors()
        buttonThemeBuilder = ButtonThemeBuilder()

        # Button constructors
        normalButtonThemeStyle = (
            buttonThemeBuilder.addLightModeBackground(Backgrounds.CIRCLE_HIDDEN_PRIMARY_25)
            .addDarkModeBackground(None)
            .build(itemSize=icons.SIZES.LARGE.height())
        )
        toggleButtonThemeStyle = (
            buttonThemeBuilder.addLightModeBackground(Backgrounds.CIRCLE_HIDDEN_PRIMARY_25)
            .addLightModeActiveBackground(Backgrounds.CIRCLE_HIDDEN_DANGER_25)
            .build(itemSize=icons.SIZES.LARGE.height())
        )
        sliderThemeBuilder = HorizontalSliderThemeBuilder()
        labelThemeBuilder = LabelThemeBuilder()

        # Font constructors
        fontBuilder = FontBuilder()
        normalFont = fontBuilder.withSize(9).build()
        emphasizedFont = fontBuilder.withSize(10).withWeight("bold").build()

        # =================UI=================
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setContentsMargins(40, 0, 40, 0)
        self.mainLayout.setSpacing(0)

        # =================LEFT=================
        self.left = QHBoxLayout()
        self.left.setContentsMargins(0, 0, 0, 0)
        self.left.setSpacing(12)
        self.mainLayout.addLayout(self.left)

        self.songCover = ImageDisplayer()
        self.songCover.setFixedSize(64, 64)
        self.songCover.setDefaultPixmap(self.__getPixmapForSongCover(ApplicationImage.defaultSongCover))
        self.left.addWidget(self.songCover)

        self.songTitle = StandardLabel.render(font=emphasizedFont)
        self.songArtist = StandardLabel.render(normalFont)
        self._addThemeForItem(
            self.songTitle,
            labelThemeBuilder.addLightModeTextColor(ColorBoxes.BLACK).addDarkModeTextColor(ColorBoxes.WHITE).build(),
        )
        self._addThemeForItem(
            self.songArtist,
            labelThemeBuilder.addLightModeTextColor(ColorBoxes.GRAY)
            .addDarkModeTextColor(ColorBoxes.WHITE)
            .build(itemSize=self.songArtist.width()),
        )
        self.songInfoLayout = QVBoxLayout()
        self.songInfoLayout.setContentsMargins(0, 0, 0, 0)
        self.songInfoLayout.setSpacing(0)
        self.left.addLayout(self.songInfoLayout, stretch=1)
        self.songInfoLayout.addStretch(0)
        self.songInfoLayout.addWidget(self.songTitle)
        self.songInfoLayout.addWidget(self.songArtist)
        self.songInfoLayout.addStretch(0)

        # =================PREVIOUS - PLAY - NEXT=================
        self.playBtns = QHBoxLayout()
        self.playBtns.setContentsMargins(0, 0, 0, 0)
        self.playBtns.setSpacing(8)
        self.left.addLayout(self.playBtns)

        self.prevSongBtn = IconButton.render(
            padding=Paddings.RELATIVE_50,
            size=icons.SIZES.LARGE,
            lightModeIcon=UiUtils.paintIcon(icons.PREVIOUS, Colors.PRIMARY),
        )
        self.prevSongBtn.setCursor(cursors.HAND)
        self.playBtns.addWidget(self.prevSongBtn)
        self._addThemeForItem(item=self.prevSongBtn, theme=normalButtonThemeStyle)
        self.playBtn = ToggleIconButton.render(
            padding=Paddings.RELATIVE_50,
            size=icons.SIZES.XLARGE,
            lightModeIcon=UiUtils.paintIcon(icons.PLAY, Colors.PRIMARY),
            lightModeCheckedIcon=UiUtils.paintIcon(icons.PAUSE, Colors.PRIMARY),
            darkModeIcon=UiUtils.paintIcon(icons.PLAY, Colors.WHITE),
            darkModeCheckedIcon=UiUtils.paintIcon(icons.PAUSE, Colors.WHITE),
        )
        self._addThemeForItem(
            item=self.playBtn,
            theme=(
                buttonThemeBuilder.addLightModeBackground(Backgrounds.CIRCLE_PRIMARY_25)
                .addLightModeActiveBackground(Backgrounds.CIRCLE_PRIMARY_25)
                .addDarkModeBackground(Backgrounds.CIRCLE_PRIMARY)
                .addDarkModeActiveBackground(Backgrounds.CIRCLE_PRIMARY)
                .build(itemSize=icons.SIZES.XLARGE.height())
            ),
        )
        self.playBtn.setChecked(False)
        self.playBtn.setCursor(cursors.HAND)
        self.playBtns.addWidget(self.playBtn)
        self._addButtonToList(self.playBtn)

        self.nextSongBtn = IconButton.render(
            padding=Paddings.RELATIVE_50,
            size=icons.SIZES.LARGE,
            lightModeIcon=UiUtils.paintIcon(icons.NEXT, Colors.PRIMARY),
        )
        self.nextSongBtn.setCursor(cursors.HAND)
        self.playBtns.addWidget(self.nextSongBtn)
        self._addThemeForItem(self.nextSongBtn, normalButtonThemeStyle)
        # =================CENTER=================
        self.center = QHBoxLayout()
        self.center.setContentsMargins(0, 0, 0, 0)
        self.center.setSpacing(4)
        self.mainLayout.addLayout(self.center)

        self.playingTime = StandardLabel.render(font=normalFont)
        self._addThemeForItem(
            self.playingTime,
            labelThemeBuilder.build(itemSize=self.playingTime.width()),
        )
        self.playingTime.setFixedWidth(60)
        self.playingTime.setAlignment(Qt.AlignRight)
        self.center.addWidget(self.playingTime)

        self.timeSlider = HorizontalSlider.render(height=12)
        self._addThemeForItem(
            self.timeSlider,
            theme=sliderThemeBuilder.addLightHandleColor(ColorBoxes.PRIMARY)
            .addLightLineColor(ColorBoxes.HOVERABLE_PRIMARY_25)
            .addDarkLineColor(ColorBoxes.HOVERABLE_WHITE_25)
            .build(itemSize=self.timeSlider.height()),
        )
        self.timeSlider.setFixedSize(250, 12)
        self.timeSlider.setProperty("value", 0)
        self.center.addWidget(self.timeSlider)

        self.totalTime = StandardLabel.render(font=normalFont)
        self._addThemeForItem(
            self.totalTime,
            labelThemeBuilder.build(itemSize=self.totalTime.width()),
        )
        self.totalTime.setFixedWidth(60)
        self.totalTime.setAlignment(Qt.AlignLeft)
        self.center.addWidget(self.totalTime)
        self.displayPlayingTime(0)
        self.displayTotalTime(0)

        # =================RIGHT=================
        self.right = QHBoxLayout()
        self.right.setContentsMargins(0, 0, 0, 0)
        self.right.setSpacing(8)
        self.mainLayout.addLayout(self.right)

        self.loopBtn = ToggleIconButton.render(
            size=icons.SIZES.LARGE,
            padding=Paddings.RELATIVE_50,
            lightModeIcon=UiUtils.paintIcon(icons.LOOP, Colors.PRIMARY),
            lightModeCheckedIcon=UiUtils.paintIcon(icons.LOOP, Colors.DANGER),
        )
        self.loopBtn.setCursor(cursors.HAND)
        self.right.addWidget(self.loopBtn)
        self._addThemeForItem(self.loopBtn, toggleButtonThemeStyle)

        self.shuffleBtn = ToggleIconButton.render(
            size=icons.SIZES.LARGE,
            padding=Paddings.RELATIVE_50,
            lightModeIcon=UiUtils.paintIcon(icons.SHUFFLE, Colors.PRIMARY),
            lightModeCheckedIcon=UiUtils.paintIcon(icons.SHUFFLE, Colors.DANGER),
        )
        self.shuffleBtn.setCursor(cursors.HAND)
        self.right.addWidget(self.shuffleBtn)
        self._addThemeForItem(self.shuffleBtn, toggleButtonThemeStyle)

        self.loveBtn = ToggleIconButton.render(
            size=icons.SIZES.LARGE,
            padding=Paddings.RELATIVE_50,
            lightModeIcon=UiUtils.paintIcon(icons.LOVE, Colors.PRIMARY),
            lightModeCheckedIcon=UiUtils.paintIcon(icons.LOVE, Colors.DANGER),
        )
        self.loveBtn.setCursor(cursors.HAND)
        self.right.addWidget(self.loveBtn)
        self._addThemeForItem(self.loveBtn, toggleButtonThemeStyle)

        self.volumeBtn = MultiIconButton.render(
            size=icons.SIZES.LARGE,
            padding=Paddings.RELATIVE_50,
            icons=[
                UiUtils.paintIcon(icons.VOLUME_UP, Colors.PRIMARY),
                UiUtils.paintIcon(icons.VOLUME_DOWN, Colors.PRIMARY),
                UiUtils.paintIcon(icons.VOLUME_SILENT, Colors.PRIMARY),
            ],
        )
        self.volumeBtn.setCursor(cursors.HAND)
        self.volumeBtn.clicked.connect(self.__showVolumeSlider)
        self.right.addWidget(self.volumeBtn)
        self._addThemeForItem(self.volumeBtn, normalButtonThemeStyle)

        self.inputs = QWidget()
        self.rightBoxes = QHBoxLayout(self.inputs)
        self.rightBoxes.setContentsMargins(0, 0, 0, 0)
        self.right.addWidget(self.inputs, 1)

        self.volumeSlider = HorizontalSlider.render(height=48)
        self._addThemeForItem(
            self.volumeSlider,
            theme=(
                sliderThemeBuilder.addLightModeBackground(Backgrounds.ROUNDED_PRIMARY_25)
                .addDarkModeBackground(Backgrounds.ROUNDED_WHITE_25)
                .build(itemSize=48)
            ),
        )
        self.volumeSlider.setSliderPosition(100)
        self.volumeSlider.setVisible(False)
        self.volumeSlider.valueChanged.connect(self.__changeVolumeIcon)
        self.rightBoxes.addWidget(self.volumeSlider)

        self.timerInput = EditableLabel.render(font=emphasizedFont)
        self.timerInput.setAlignment(Qt.AlignCenter)
        self.timerInput.setFixedHeight(48)
        self.timerInput.setValidator(QIntValidator())
        self.timerInput.setVisible(False)
        self.rightBoxes.addWidget(self.timerInput)
        self._addThemeForItem(
            self.timerInput,
            theme=(
                labelThemeBuilder.addLightModeTextColor(ColorBoxes.PRIMARY)
                .addLightModeBackground(Backgrounds.ROUNDED_PRIMARY_25)
                .addDarkModeTextColor(ColorBoxes.WHITE)
                .addDarkModeBackground(Backgrounds.ROUNDED_WHITE_25)
                .build(itemSize=self.timerInput.width())
            ),
        )
        self.timerBtn = IconButton.render(
            padding=Paddings.RELATIVE_50,
            size=icons.SIZES.LARGE,
            lightModeIcon=UiUtils.paintIcon(icons.TIMER, Colors.PRIMARY),
        )
        self.timerBtn.setCursor(cursors.HAND)
        self.timerBtn.clicked.connect(self.__showTimerInput)
        self.right.addWidget(self.timerBtn)
        self._addThemeForItem(self.timerBtn, normalButtonThemeStyle)

        QMetaObject.connectSlotsByName(self)

    def connectController(self, controller) -> None:
        pass

    def translate(self, language: dict) -> None:
        languageTextForSongTitle = language.get("song_title")
        languageTextForSongArtist = language.get("song_artist")

        self.songTitle.setDefaultText(languageTextForSongTitle)
        self.songArtist.setDefaultText(languageTextForSongArtist)
        self.timerInput.setPlaceholderText(language.get("enter_timer_minute"))

    def displaySongInfo(
        self,
        cover: bytes = None,
        title: str = None,
        artist: str = None,
        loveState: bool = False,
    ) -> None:
        if artist is None and title is not None:
            artist = ""
        self.songCover.setPixmap(self.__getPixmapForSongCover(cover))
        self.songTitle.setText(title)
        self.songTitle.setCursorPosition(0)
        self.songArtist.setText(artist)
        self.songArtist.setCursorPosition(0)
        self.loveBtn.setChecked(loveState)

    def displayPlayingTime(self, time: float) -> None:
        self.playingTime.setText(Stringify.floatToClockTime(time))

    def displayTotalTime(self, time: float) -> None:
        self.totalTime.setText(Stringify.floatToClockTime(time))

    def runTimeSlider(self, currentTime: float, totalTime: float) -> None:
        TIME_FIX_FOR_CASE_WHEN_DEVIDING_FOR_ZERO: float = 999999.0
        if totalTime == 0:
            totalTime = TIME_FIX_FOR_CASE_WHEN_DEVIDING_FOR_ZERO
        position = int(currentTime * 100 / totalTime)
        self.timeSlider.setSliderPosition(position)

    def setLoopState(self, state: bool) -> None:
        self.loopBtn.setChecked(state)

    def setShuffleState(self, state: bool) -> None:
        self.shuffleBtn.setChecked(state)

    def setLoveState(self, state: bool) -> None:
        self.loveBtn.setChecked(state)

    def setVolume(self, volume: int) -> None:
        self.volumeSlider.setValue(volume)
        self.__changeVolumeIcon()

    def setPlayingState(self, state: bool) -> None:
        self.playBtn.setChecked(state)

    def isLooping(self) -> bool:
        return self.loopBtn.isChecked()

    def isShuffling(self) -> bool:
        return self.shuffleBtn.isChecked()

    def isPlaying(self) -> bool:
        return self.playBtn.isChecked()

    def getTimerValue(self) -> int:
        return int(self.timerInput.text())

    def getCurrentTimeSliderPosition(self) -> int:
        return self.timeSlider.sliderPosition()

    def getCurrentVolumeValue(self) -> int:
        return self.volumeSlider.value()

    def closeTimerBox(self) -> None:
        self.timerInput.clear()
        self.timerInput.hide()

    def connectSignalsToController(self, controller) -> None:
        self.prevSongBtn.clicked.connect(controller.handlePreviousSong)
        self.playBtn.clicked.connect(controller.handlePlaySong)
        self.nextSongBtn.clicked.connect(controller.handleNextSong)
        self.timeSlider.sliderPressed.connect(controller.handlePausedTimeSlider)
        self.timeSlider.sliderReleased.connect(controller.handleUnpausedTimeSlider)
        self.loopBtn.clicked.connect(controller.handleClickedLoop)
        self.shuffleBtn.clicked.connect(controller.handleClickedShuffle)
        self.loveBtn.clicked.connect(controller.handleLoveSong)
        self.volumeSlider.valueChanged.connect(controller.handleChangVolume)
        self.timerInput.returnPressed.connect(controller.handleEnteredTimer)

    def __getPixmapForSongCover(self, coverAsByte: bytes) -> QPixmap:
        if coverAsByte is None:
            return None
        pixmap = UiUtils.getSquaredPixmapFromBytes(coverAsByte, edge=self.songCover.width(), radius=12)
        return pixmap

    def __changeVolumeIcon(self) -> None:
        volume: int = self.volumeSlider.value()
        VOLUME_UP_ICON = 0
        VOLUME_DOWN_ICON = 1
        SILENT_ICON = 2
        icon = SILENT_ICON
        if 0 < volume <= 33:
            icon = VOLUME_DOWN_ICON
        if 33 < volume <= 100:
            icon = VOLUME_UP_ICON
        self.volumeBtn.setCurrentIcon(icon)

    def __showVolumeSlider(self) -> None:
        self.volumeSlider.setVisible(not self.volumeSlider.isVisible())
        self.timerInput.setVisible(False)

    def __showTimerInput(self) -> None:
        self.timerInput.setVisible(not self.timerInput.isVisible())
        self.volumeSlider.setVisible(False)
