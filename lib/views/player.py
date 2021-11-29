from sys import path

from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtGui import QCursor, QIntValidator
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QWidget

path.append("./lib")
from constants.ui import alignment, colors, icons
from constants.ui.background_color import BackgroundColorSamples
from modules.screens.background import Background
from modules.screens.components.buttons.icon_button_factory import IconButtonFactory
from modules.screens.components.font_builder import FontBuilder
from modules.screens.components.slider.horizontal_slider import HorizontalSlider
from utils.helpers.my_string import Stringify
from utils.ui.application_ui_utils import ApplicationUIUtils as AppUI
from widgets.image_label import ImageLabel


class UIPlayerMusic(QWidget):
    def setupUi(self):
        ICONS = icons.Icons()
        ALIGNMENT = alignment.Alignment()
        background = BackgroundColorSamples()
        buttonFactory = IconButtonFactory()
        fontBuilder = FontBuilder()
        COLORS = colors.Colors
        HAND_CURSOR = QCursor(Qt.PointingHandCursor)

        normalButtonForm = buttonFactory.getButton()
        normalButtonForm.backgroundColor = background.HIDDEN_PRIMARY

        musicToggleButtonForm = buttonFactory.getButton("checkable").withBackground(
            background.HIDDEN_PRIMARY, background.HIDDEN_DANGER
        )
        slider = HorizontalSlider(
            lineColor=background.BLACK,
            handleColor=background.FLAT_PRIMARY,
        )

        # =================UI=================
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(40, 0, 40, 0)
        self.main_layout.setSpacing(40)

        # =================LEFT=================
        self.left = QHBoxLayout()
        self.left.setContentsMargins(0, 0, 0, 0)
        self.left.setSpacing(12)
        self.main_layout.addLayout(self.left)

        self.song_cover = ImageLabel()
        self.song_cover.setFixedSize(64, 64)
        self.left.addWidget(self.song_cover)

        self.song_info_layout = QVBoxLayout()
        self.song_info_layout.setContentsMargins(0, 0, 0, 0)
        self.song_info_layout.setSpacing(8)
        self.left.addLayout(self.song_info_layout, stretch=1)

        self.song_title = QLabel()
        self.song_title.setText("Song's title")
        self.song_title.setFont(fontBuilder.withSize(10).withWeight("bold").build())

        self.song_artist = QLabel()
        self.song_artist.setText("Song's artist")
        self.song_artist.setStyleSheet(f"color: {str(COLORS.DISABLED)}")

        self.song_info_layout.addStretch(0)
        self.song_info_layout.addWidget(self.song_title)
        self.song_info_layout.addWidget(self.song_artist)
        self.song_info_layout.addStretch(0)

        # =================PREVIOUS - PLAY - NEXT=================
        self.play_buttons = QHBoxLayout()
        self.play_buttons.setContentsMargins(0, 0, 0, 0)
        self.play_buttons.setSpacing(8)
        self.left.addLayout(self.play_buttons)

        self.previous_song_btn = normalButtonForm.export(
            iconSize=ICONS.SIZES.SMALL,
            icon=AppUI.paintIcon(ICONS.PREVIOUS, COLORS.PRIMARY),
            cursor=HAND_CURSOR,
        )
        self.play_buttons.addWidget(self.previous_song_btn)

        self.play_song_btn = (
            buttonFactory.getButton("checkable")
            .withBackground(background.PRIMARY)
            .export(
                padding=0.75,
                iconSize=ICONS.SIZES.MEDIUM,
                icon=AppUI.paintIcon(ICONS.PLAY, COLORS.PRIMARY),
                checkedIcon=AppUI.paintIcon(ICONS.PAUSE, COLORS.PRIMARY),
                cursor=HAND_CURSOR,
            )
        )
        self.play_song_btn.setChecked(False)
        self.play_buttons.addWidget(self.play_song_btn)

        self.next_song_btn = normalButtonForm.export(
            iconSize=ICONS.SIZES.SMALL,
            icon=AppUI.paintIcon(ICONS.NEXT, COLORS.PRIMARY),
            cursor=HAND_CURSOR,
        )
        self.play_buttons.addWidget(self.next_song_btn)

        # =================CENTER=================
        self.center = QWidget()

        self.main_layout.addWidget(self.center, 0, ALIGNMENT.CENTER)
        self.center_layout = QHBoxLayout(self.center)
        self.center_layout.setContentsMargins(0, 0, 0, 0)

        self.time_playing = QLabel()
        self.center_layout.addWidget(self.time_playing)

        self.time_slider = slider.export(12)
        self.time_slider.setFixedSize(250, 12)

        self.time_slider.setProperty("value", 0)
        self.center_layout.addWidget(self.time_slider)

        self.time_end = QLabel()
        self.center_layout.addWidget(self.time_end)

        # =================RIGHT=================
        self.right = QHBoxLayout()
        self.right.setContentsMargins(0, 0, 0, 0)
        self.right.setSpacing(8)
        self.main_layout.addLayout(self.right)

        self.loop_btn = musicToggleButtonForm.export(
            padding=1,
            iconSize=ICONS.SIZES.SMALL,
            icon=AppUI.paintIcon(ICONS.LOOP, COLORS.PRIMARY),
            checkedIcon=AppUI.paintIcon(ICONS.LOOP, COLORS.DANGER),
            cursor=HAND_CURSOR,
        )
        self.right.addWidget(self.loop_btn)

        self.shuffle_btn = musicToggleButtonForm.export(
            padding=1,
            iconSize=ICONS.SIZES.SMALL,
            icon=AppUI.paintIcon(ICONS.SHUFFLE, COLORS.PRIMARY),
            checkedIcon=AppUI.paintIcon(ICONS.SHUFFLE, COLORS.DANGER),
            cursor=HAND_CURSOR,
        )
        self.right.addWidget(self.shuffle_btn)

        self.love_btn = musicToggleButtonForm.export(
            padding=1,
            iconSize=ICONS.SIZES.SMALL,
            icon=AppUI.paintIcon(ICONS.LOVE, COLORS.PRIMARY),
            checkedIcon=AppUI.paintIcon(ICONS.LOVE, COLORS.DANGER),
            cursor=HAND_CURSOR,
        )
        self.right.addWidget(self.love_btn)

        self.volume_btn = (
            buttonFactory.getButton("multiple-icon")
            .withBackground(background.HIDDEN_PRIMARY)
            .export(
                padding=1,
                iconSize=ICONS.SIZES.SMALL,
                iconList=[
                    AppUI.paintIcon(ICONS.VOLUME_UP, COLORS.PRIMARY),
                    AppUI.paintIcon(ICONS.VOLUME_DOWN, COLORS.PRIMARY),
                    AppUI.paintIcon(ICONS.VOLUME_SILENT, COLORS.PRIMARY),
                ],
                cursor=HAND_CURSOR,
            )
        )
        self.volume_btn.clicked.connect(self.showVolumeSlider)
        self.right.addWidget(self.volume_btn)

        self.timer_boxs = QWidget()
        self.timer_boxs_layout = QHBoxLayout(self.timer_boxs)
        self.timer_boxs_layout.setContentsMargins(0, 0, 0, 0)
        self.right.addWidget(self.timer_boxs, 1)

        slider.background = Background(color=background.PRIMARY, roundness=12)
        self.volume_slider = slider.export(40)
        self.volume_slider.setSliderPosition(100)
        self.volume_slider.setVisible(False)
        self.volume_slider.valueChanged.connect(self.changeVolumeIcon)
        self.timer_boxs_layout.addWidget(self.volume_slider)

        self.timer_box = QLineEdit()
        self.timer_box.setStyleSheet(
            "QLineEdit{background:rgba(160,160,160,0.2);border-radius:12px;padding:0px 16px 0px}\n"
            "QLineEdit::hover{background:rgba(160,160,160,0.25)}"
        )
        self.timer_box.setFixedHeight(40)
        self.timer_box.setAlignment(ALIGNMENT.CENTER)
        self.timer_box.setPlaceholderText("Enter Minute")
        self.timer_box.setValidator(QIntValidator())
        self.timer_box.setVisible(False)
        self.timer_boxs_layout.addWidget(self.timer_box)

        self.timer_btn = normalButtonForm.export(
            padding=1,
            iconSize=ICONS.SIZES.SMALL,
            icon=AppUI.paintIcon(ICONS.TIMER, COLORS.PRIMARY),
            cursor=HAND_CURSOR,
        )
        self.timer_btn.clicked.connect(self.showTimerBox)
        self.right.addWidget(self.timer_btn)

        QMetaObject.connectSlotsByName(self)

    def displaySongInfo(self, cover, title, artist):
        self.song_cover.setPixmap(cover)
        self.song_title.setText(title)
        self.song_artist.setText(artist)

    def changeVolumeIcon(self):
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

    def getPixmapForSongCover(self, coverAsByte):
        return AppUI.getSquaredPixmapFromBytes(
            coverAsByte, self.song_cover.width(), radius=12
        )

    def showVolumeSlider(self):
        self.volume_slider.setVisible(not self.volume_slider.isVisible())
        self.timer_box.setVisible(False)

    def showTimerBox(self):
        self.timer_box.setVisible(not self.timer_box.isVisible())
        self.volume_slider.setVisible(False)

    def displayPlayingTime(self, time: float):
        self.time_playing.setText(Stringify.floatToClockTime(time))

    def displayTotalTime(self, time: float):
        self.time_end.setText(Stringify.floatToClockTime(time))

    def runTimeSlider(self, currentTime: float, totalTime: float):
        position = int(currentTime * 100 / totalTime)
        self.time_slider.setSliderPosition(position)

    def isLooping(self):
        return self.loop_btn.isChecked()

    def isShuffling(self):
        return self.shuffle_btn.isChecked()
