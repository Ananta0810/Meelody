from sys import path

from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtGui import QCursor, QIntValidator
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QWidget

path.append(".")
from lib.constants.ui import alignment, colors, icons
from lib.constants.ui.background_color import BackgroundColorSamples
from lib.modules.screens.background import Background
from lib.modules.screens.components.buttons.icon_button_factory import IconButtonFactory
from lib.modules.screens.components.font_builder import FontBuilder
from lib.modules.screens.components.slider.horizontal_slider import HorizontalSlider
from lib.utils.helpers.my_string import Stringify
from lib.utils.ui.color_utils import ColorUtils
from lib.utils.ui.icon_utils import IconUtils
from lib.widgets.image_label import ImageLabel


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
        self.music_play_buttons_layout = QHBoxLayout()
        self.music_play_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.music_play_buttons_layout.setSpacing(8)
        self.left.addLayout(self.music_play_buttons_layout)

        self.previous_song_btn = normalButtonForm.export(
            iconSize=ICONS.SIZES.SMALL,
            icon=IconUtils.colorize(
                ICONS.PREVIOUS, ColorUtils.getQColorFromColor(COLORS.PRIMARY)
            ),
            cursor=HAND_CURSOR,
        )

        self.music_play_buttons_layout.addWidget(self.previous_song_btn)

        self.play_song_btn = (
            buttonFactory.getButton("checkable")
            .withBackground(background.PRIMARY)
            .export(
                padding=0.75,
                iconSize=ICONS.SIZES.MEDIUM,
                icon=IconUtils.colorize(
                    ICONS.PLAY, ColorUtils.getQColorFromColor(COLORS.PRIMARY)
                ),
                checkedIcon=IconUtils.colorize(
                    ICONS.PAUSE, ColorUtils.getQColorFromColor(COLORS.PRIMARY)
                ),
                cursor=HAND_CURSOR,
            )
        )
        self.play_song_btn.setChecked(False)
        self.music_play_buttons_layout.addWidget(self.play_song_btn)

        self.next_song_btn = normalButtonForm.export(
            iconSize=ICONS.SIZES.SMALL,
            icon=IconUtils.colorize(
                ICONS.NEXT, ColorUtils.getQColorFromColor(COLORS.PRIMARY)
            ),
            cursor=HAND_CURSOR,
        )
        self.music_play_buttons_layout.addWidget(self.next_song_btn)

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
            icon=IconUtils.colorize(
                ICONS.LOOP, ColorUtils.getQColorFromColor(COLORS.PRIMARY)
            ),
            checkedIcon=IconUtils.colorize(
                ICONS.LOOP, ColorUtils.getQColorFromColor(COLORS.DANGER)
            ),
            cursor=HAND_CURSOR,
        )
        self.right.addWidget(self.loop_btn)

        self.shuffle_btn = musicToggleButtonForm.export(
            padding=1,
            iconSize=ICONS.SIZES.SMALL,
            icon=IconUtils.colorize(
                ICONS.SHUFFLE, ColorUtils.getQColorFromColor(COLORS.PRIMARY)
            ),
            checkedIcon=IconUtils.colorize(
                ICONS.SHUFFLE, ColorUtils.getQColorFromColor(COLORS.DANGER)
            ),
            cursor=HAND_CURSOR,
        )
        self.right.addWidget(self.shuffle_btn)

        self.love_btn = musicToggleButtonForm.export(
            padding=1,
            iconSize=ICONS.SIZES.SMALL,
            icon=IconUtils.colorize(
                ICONS.LOVE, ColorUtils.getQColorFromColor(COLORS.PRIMARY)
            ),
            checkedIcon=IconUtils.colorize(
                ICONS.LOVE, ColorUtils.getQColorFromColor(COLORS.DANGER)
            ),
            cursor=HAND_CURSOR,
        )

        self.right.addWidget(self.love_btn)

        self.volume_btn = (
            buttonFactory.getButton("multiple-icon")
            .withBackground(background.HIDDEN_PRIMARY)
            .export(
                padding=1,
                iconSize=ICONS.SIZES.SMALL,
                iconList={
                    "volume up": IconUtils.colorize(
                        ICONS.VOLUME_UP, ColorUtils.getQColorFromColor(COLORS.PRIMARY)
                    ),
                    "volume down": IconUtils.colorize(
                        ICONS.VOLUME_DOWN, ColorUtils.getQColorFromColor(COLORS.PRIMARY)
                    ),
                    "silent volume": IconUtils.colorize(
                        ICONS.VOLUME_SILENT,
                        ColorUtils.getQColorFromColor(COLORS.PRIMARY),
                    ),
                },
                cursor=HAND_CURSOR,
            )
        )
        self.volume_btn.setCurrentIcon("volume up")

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
            icon=IconUtils.colorize(
                ICONS.TIMER, ColorUtils.getQColorFromColor(COLORS.PRIMARY)
            ),
            cursor=HAND_CURSOR,
        )

        self.timer_btn.clicked.connect(self.showTimerBox)
        self.right.addWidget(self.timer_btn)

        QMetaObject.connectSlotsByName(self)

    def changeVolumeIcon(self):
        volume: int = self.volume_slider.value()
        currentIcon = "silent volume"
        if 0 < volume <= 50:
            currentIcon = "volume down"
        if 50 < volume <= 100:
            currentIcon = "volume up"
        self.volume_btn.setCurrentIcon(currentIcon)

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
