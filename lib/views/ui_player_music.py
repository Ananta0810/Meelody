from sys import path

from PyQt5.QtCore import QMetaObject
from PyQt5.QtGui import QIntValidator, QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

path.append("./lib")
from constants.ui.base import ApplicationImage
from constants.ui.qss import *
from constants.ui.qt import AppAlignment, AppCursors, AppIcons
from modules.screens.components.factories import *
from modules.screens.components.font_builder import FontBuilder
from modules.screens.qss.qss_elements import *
from utils.helpers.my_string import Stringify
from utils.ui.application_utils import ApplicationUIUtils as AppUI
from widgets.image_displayer import ImageDisplayer


class UIPlayerMusic(QWidget):
    def setupUi(self, controller):
        self.controller = controller
        self.themeItems = {}
        Icons = AppIcons()
        Alignment = AppAlignment()
        Cursors = AppCursors()

        # Button constructors
        buttonFactory = IconButtonFactory()
        standardIconButtonRenderer = buttonFactory.getByType("default")
        toggleButtonRenderer = buttonFactory.getByType("toggle")
        primaryButtonBackground = Background(
            borderRadius=0.5,
            color=ColorBoxes.HIDDEN_PRIMARY,
        )
        normalButtonThemeStyle = (
            standardIconButtonRenderer.getThemeBuilder()
            .addLightModeBackground(primaryButtonBackground)
            .build(itemSize=Icons.SIZES.LARGE.height())
        )
        toggleButtonThemeStyle = (
            toggleButtonRenderer.getThemeBuilder()
            .addLightModeBackground(primaryButtonBackground)
            .addLightModeActiveBackground(
                Background(
                    borderRadius=0.5,
                    color=ColorBoxes.HIDDEN_DANGER,
                )
            )
            .build(itemSize=Icons.SIZES.LARGE.height())
        )
        horizontalSlider = SliderFactory().getByType("horizontal")
        sliderThemeBuilder = horizontalSlider.getThemeBuilder()
        labelFactory = LabelFactory()
        labelRenderer = labelFactory.getByType("default")
        editableLabel = labelFactory.getByType("editable")
        labelThemeBuilder = labelRenderer.getThemeBuilder()

        # Font constructors
        fontBuilder = FontBuilder()
        normalFont = fontBuilder.withSize(9).build()
        emphasizedFont = fontBuilder.withSize(10).withWeight("bold").build()

        # =================UI=================
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(40, 0, 40, 0)
        self.main_layout.setSpacing(0)

        # =================LEFT=================
        self.left = QHBoxLayout()
        self.left.setContentsMargins(0, 0, 0, 0)
        self.left.setSpacing(12)
        self.main_layout.addLayout(self.left)

        self.song_cover = ImageDisplayer()
        self.song_cover.setFixedSize(64, 64)
        self.song_cover.setDefaultPixmap(
            self.__getPixmapForSongCover(ApplicationImage.defaultSongCover)
        )
        self.left.addWidget(self.song_cover)

        self.song_title = labelRenderer.render(font=emphasizedFont)
        self.__addThemeForItem(
            self.song_title,
            labelThemeBuilder.addLightModeTextColor(ColorBoxes.BLACK)
            .addDarkModeTextColor(ColorBoxes.WHITE)
            .build(itemSize=self.song_title.width()),
        )
        self.song_artist = labelRenderer.render(normalFont)
        self.__addThemeForItem(
            self.song_artist,
            labelThemeBuilder.addLightModeTextColor(ColorBoxes.GRAY)
            .addDarkModeTextColor(ColorBoxes.WHITE)
            .build(itemSize=self.song_artist.width()),
        )
        self.song_info_layout = QVBoxLayout()
        self.song_info_layout.setContentsMargins(0, 0, 0, 0)
        self.song_info_layout.setSpacing(0)
        self.left.addLayout(self.song_info_layout, stretch=1)
        self.song_info_layout.addStretch(0)
        self.song_info_layout.addWidget(self.song_title)
        self.song_info_layout.addWidget(self.song_artist)
        self.song_info_layout.addStretch(0)

        # =================PREVIOUS - PLAY - NEXT=================
        self.play_buttons = QHBoxLayout()
        self.play_buttons.setContentsMargins(0, 0, 0, 0)
        self.play_buttons.setSpacing(8)
        self.left.addLayout(self.play_buttons)

        self.previous_song_btn = standardIconButtonRenderer.render(
            padding=Paddings.RELATIVE_50,
            size=Icons.SIZES.LARGE,
            icon=AppUI.paintIcon(Icons.PREVIOUS, Colors.PRIMARY),
        )
        self.previous_song_btn.setCursor(Cursors.HAND)
        self.play_buttons.addWidget(self.previous_song_btn)
        self.__addThemeForItem(
            item=self.previous_song_btn, theme=normalButtonThemeStyle
        )
        self.play_song_btn = toggleButtonRenderer.render(
            padding=Paddings.RELATIVE_50,
            size=Icons.SIZES.XLARGE,
            icon=AppUI.paintIcon(Icons.PLAY, Colors.WHITE),
            checkedIcon=AppUI.paintIcon(Icons.PAUSE, Colors.WHITE),
        )
        self.__addThemeForItem(
            item=self.play_song_btn,
            theme=(
                toggleButtonRenderer.getThemeBuilder()
                .addLightModeBackground(
                    Background(
                        borderRadius=0.5,
                        color=ColorBoxes.PRIMARY_LIGHTEN,
                    )
                )
                .addDarkModeBackground(
                    Background(
                        borderRadius=0.5,
                        color=ColorBoxes.PRIMARY,
                    )
                )
                .build(itemSize=Icons.SIZES.XLARGE.height())
            ),
        )
        self.play_song_btn.setChecked(False)
        self.play_song_btn.setCursor(Cursors.HAND)
        self.play_buttons.addWidget(self.play_song_btn)

        self.next_song_btn = standardIconButtonRenderer.render(
            padding=Paddings.RELATIVE_50,
            size=Icons.SIZES.LARGE,
            icon=AppUI.paintIcon(Icons.NEXT, Colors.PRIMARY),
        )
        self.next_song_btn.setCursor(Cursors.HAND)
        self.play_buttons.addWidget(self.next_song_btn)
        self.__addThemeForItem(self.next_song_btn, normalButtonThemeStyle)
        # =================CENTER=================
        self.center = QHBoxLayout()
        self.center.setContentsMargins(0, 0, 0, 0)
        self.center.setSpacing(4)
        self.main_layout.addLayout(self.center)

        self.playing_time = labelRenderer.render(font=normalFont)
        self.__addThemeForItem(
            self.playing_time,
            labelThemeBuilder.build(itemSize=self.playing_time.width()),
        )
        self.playing_time.setFixedWidth(60)
        self.playing_time.setAlignment(Alignment.RIGHT)
        self.center.addWidget(self.playing_time)

        self.time_slider = horizontalSlider.render(height=12)
        self.__addThemeForItem(
            self.time_slider,
            theme=sliderThemeBuilder.addLightHandleColor(ColorBoxes.PRIMARY)
            .addLightLineColor(ColorBoxes.PRIMARY_LIGHTEN)
            .addDarkLineColor(ColorBoxes.WHITE_LIGHTEN)
            .build(itemSize=self.time_slider.height()),
        )
        self.time_slider.setFixedSize(250, 12)
        self.time_slider.setProperty("value", 0)
        self.center.addWidget(self.time_slider)

        self.total_time = labelRenderer.render(font=normalFont)
        self.__addThemeForItem(
            self.total_time,
            labelThemeBuilder.build(itemSize=self.total_time.width()),
        )
        self.total_time.setFixedWidth(60)
        self.total_time.setAlignment(Alignment.LEFT)
        self.center.addWidget(self.total_time)
        self.displayPlayingTime(0)
        self.displayTotalTime(0)

        # =================RIGHT=================
        self.right = QHBoxLayout()
        self.right.setContentsMargins(0, 0, 0, 0)
        self.right.setSpacing(8)
        self.main_layout.addLayout(self.right)

        self.loop_btn = toggleButtonRenderer.render(
            size=Icons.SIZES.LARGE,
            padding=Paddings.RELATIVE_50,
            icon=AppUI.paintIcon(Icons.LOOP, Colors.PRIMARY),
            checkedIcon=AppUI.paintIcon(Icons.LOOP, Colors.DANGER),
        )
        self.loop_btn.setCursor(Cursors.HAND)
        self.right.addWidget(self.loop_btn)
        self.__addThemeForItem(self.loop_btn, toggleButtonThemeStyle)

        self.shuffle_btn = toggleButtonRenderer.render(
            size=Icons.SIZES.LARGE,
            padding=Paddings.RELATIVE_50,
            icon=AppUI.paintIcon(Icons.SHUFFLE, Colors.PRIMARY),
            checkedIcon=AppUI.paintIcon(Icons.SHUFFLE, Colors.DANGER),
        )
        self.shuffle_btn.setCursor(Cursors.HAND)
        self.right.addWidget(self.shuffle_btn)
        self.__addThemeForItem(self.shuffle_btn, toggleButtonThemeStyle)

        self.love_btn = toggleButtonRenderer.render(
            size=Icons.SIZES.LARGE,
            padding=Paddings.RELATIVE_50,
            icon=AppUI.paintIcon(Icons.LOVE, Colors.PRIMARY),
            checkedIcon=AppUI.paintIcon(Icons.LOVE, Colors.DANGER),
        )
        self.love_btn.setCursor(Cursors.HAND)
        self.right.addWidget(self.love_btn)
        self.__addThemeForItem(self.love_btn, toggleButtonThemeStyle)

        self.volume_btn = buttonFactory.getByType("multiple-icon").render(
            size=Icons.SIZES.LARGE,
            padding=Paddings.RELATIVE_50,
            icons=[
                AppUI.paintIcon(Icons.VOLUME_UP, Colors.PRIMARY),
                AppUI.paintIcon(Icons.VOLUME_DOWN, Colors.PRIMARY),
                AppUI.paintIcon(Icons.VOLUME_SILENT, Colors.PRIMARY),
            ],
        )
        self.volume_btn.setCursor(Cursors.HAND)
        self.volume_btn.clicked.connect(self.__showVolumeSlider)
        self.right.addWidget(self.volume_btn)
        self.__addThemeForItem(self.volume_btn, normalButtonThemeStyle)

        self.timer_inputs = QWidget()
        self.right_boxes = QHBoxLayout(self.timer_inputs)
        self.right_boxes.setContentsMargins(0, 0, 0, 0)
        self.right.addWidget(self.timer_inputs, 1)

        self.volume_slider = horizontalSlider.render(height=48)
        self.__addThemeForItem(
            self.volume_slider,
            theme=(
                sliderThemeBuilder.addLightModeBackground(
                    Background(
                        borderRadius=12,
                        color=ColorBoxes.PRIMARY_LIGHTEN,
                    )
                )
                .addDarkModeBackground(
                    Background(
                        borderRadius=12,
                        color=ColorBoxes.WHITE_LIGHTEN,
                    )
                )
                .build(itemSize=48)
            ),
        )
        self.volume_slider.setSliderPosition(100)
        self.volume_slider.setVisible(False)
        self.volume_slider.valueChanged.connect(self.__changeVolumeIcon)
        self.right_boxes.addWidget(self.volume_slider)

        self.timer_input = editableLabel.render(
            font=emphasizedFont,
            alignment=Alignment.CENTER,
        )
        self.timer_input.setFixedHeight(48)
        self.timer_input.setPlaceholderText("Enter Minute")
        self.timer_input.setValidator(QIntValidator())
        self.timer_input.setVisible(False)
        self.right_boxes.addWidget(self.timer_input)
        self.__addThemeForItem(
            self.timer_input,
            theme=(
                editableLabel.getThemeBuilder()
                .addLightModeTextColor(ColorBoxes.PRIMARY)
                .addLightModeBackground(
                    Background(
                        borderRadius=12,
                        color=ColorBoxes.BLACK_LIGHTEN,
                    )
                )
                .addDarkModeTextColor(ColorBoxes.WHITE)
                .addDarkModeBackground(
                    Background(
                        borderRadius=12,
                        color=ColorBoxes.WHITE_LIGHTEN,
                    )
                )
                .build(itemSize=self.timer_input.width())
            ),
        )
        self.timer_btn = standardIconButtonRenderer.render(
            padding=Paddings.RELATIVE_50,
            size=Icons.SIZES.LARGE,
            icon=AppUI.paintIcon(Icons.TIMER, Colors.PRIMARY),
        )
        self.timer_btn.setCursor(Cursors.HAND)
        self.timer_btn.clicked.connect(self.__showTimerInput)
        self.right.addWidget(self.timer_btn)
        self.__addThemeForItem(self.timer_btn, normalButtonThemeStyle)

        self.__connectSignals()
        QMetaObject.connectSlotsByName(self)

    def darkMode(self):
        for item in self.themeItems:
            darkModeStyleSheet = self.themeItems.get(item).darkMode
            if darkModeStyleSheet is None or darkModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(darkModeStyleSheet)

    def lightMode(self):
        for item in self.themeItems:
            lightModeStyleSheet = self.themeItems.get(item).lightMode
            if lightModeStyleSheet is None or lightModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(lightModeStyleSheet)

    def displaySongInfo(self, cover: bytes, title: str, artist: str) -> None:
        coverAsPixmap = (
            self.__getPixmapForSongCover(cover) if cover is not None else None
        )
        self.song_cover.setPixmap(coverAsPixmap)
        self.song_title.setText(title or "song's title")
        self.song_artist.setText(artist or "song's artist")

    def displayPlayingTime(self, time: float) -> None:
        self.playing_time.setText(Stringify.floatToClockTime(time))

    def displayTotalTime(self, time: float) -> None:
        self.total_time.setText(Stringify.floatToClockTime(time))

    def runTimeSlider(self, currentTime: float, totalTime: float) -> None:
        position = int(currentTime * 100 / totalTime)
        self.time_slider.setSliderPosition(position)

    def isLooping(self) -> bool:
        return self.loop_btn.isChecked()

    def isShuffling(self) -> bool:
        return self.shuffle_btn.isChecked()

    def isPlaying(self) -> bool:
        return self.play_song_btn.isChecked()

    def getTimerValue(self) -> int:
        return int(self.timer_input.text())

    def getCurrentTimeSliderPosition(self) -> int:
        return self.time_slider.sliderPosition()

    def getCurrentVolumeValue(self) -> int:
        return self.volume_slider.value()

    def closeTimerBox(self) -> None:
        self.timer_input.clear()
        self.timer_input.hide()

    def setPlayingState(self, state: bool) -> None:
        self.play_song_btn.setChecked(state)

    def __connectSignals(self) -> None:
        self.previous_song_btn.clicked.connect(
            self.controller.handlePreviousSong
        )
        self.play_song_btn.clicked.connect(self.controller.handlePlaySong)
        self.next_song_btn.clicked.connect(self.controller.handleNextSong)
        self.time_slider.sliderPressed.connect(
            self.controller.handlePausedTimeSlider
        )
        self.time_slider.sliderReleased.connect(
            self.controller.handleUnpausedTimeSlider
        )
        self.shuffle_btn.clicked.connect(self.controller.handleClickedShuffle)
        self.love_btn.clicked.connect(self.controller.handleLoveSong)
        self.volume_slider.valueChanged.connect(
            self.controller.handleChangVolume
        )
        self.timer_input.returnPressed.connect(
            self.controller.handleEnteredTimer
        )

    def __getPixmapForSongCover(self, coverAsByte: bytes) -> QPixmap:
        return AppUI.getSquaredPixmapFromBytes(
            coverAsByte, edge=self.song_cover.width(), radius=12
        )

    def __changeVolumeIcon(self) -> None:
        volume: int = self.volume_slider.value()
        VOLUME_UP_ICON = 0
        VOLUME_DOWN_ICON = 1
        SILENT_ICON = 2
        icon = SILENT_ICON
        if 0 < volume <= 50:
            icon = VOLUME_DOWN_ICON
        if 50 < volume <= 100:
            icon = VOLUME_UP_ICON
        self.volume_btn.setCurrentIcon(icon)

    def __showVolumeSlider(self) -> None:
        self.volume_slider.setVisible(not self.volume_slider.isVisible())
        self.timer_input.setVisible(False)

    def __showTimerInput(self) -> None:
        self.timer_input.setVisible(not self.timer_input.isVisible())
        self.volume_slider.setVisible(False)

    def __addThemeForItem(self, item, theme: str):
        self.themeItems[item] = theme
