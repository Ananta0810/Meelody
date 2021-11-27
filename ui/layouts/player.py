# from PyQt5 import QtCore, QtGui, QtWidgets
from sys import path

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

path.append(".")
from ui.base.alignment import Align
from ui.base.colors import Colors
from ui.base.cursors import Cursors
from ui.base.icons import Icons
from ui.base.palette import Palette
from ui.components.buttons.icon_button_factory import IconButtonFactory
from ui.components.font_builder import FontBuilder
from ui.components.slider.horizontal_slider import HorizontalSlider
from ui.models.background import Background
from ui.models.background_color import BackgroundColor
from ui.overridden.image_label import ImageLabel
from ui.utils.color_utils import ColorUtils
from ui.utils.icon_utils import IconUtils
from utils.common_types.my_string import Stringify


class UIPlayerMusic(QWidget):
    play_song_signal = pyqtSignal()
    love_signal = pyqtSignal()
    shuffle_signal = pyqtSignal()

    def setupUi(self):
        self._run_time_slider = True

        icons = Icons()
        cursors = Cursors()
        alignment = Align()
        palette = Palette()
        slider = HorizontalSlider(
            lineSize=2,
            lineColor=BackgroundColor(normal=Colors.BLACK.withAlpha(0.15)),
            handleSize=10,
            handleColor=BackgroundColor(normal=Colors.PRIMARY),
        )
        iconButtonFactory = IconButtonFactory()
        fontBuilder = FontBuilder()
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
        self.song_title.setPalette(palette.PRIMARY)
        self.song_artist = QLabel()
        self.song_artist.setText("Song's artist")
        self.song_artist.setStyleSheet(f"color: {str(Colors.DISABLED)}")

        self.song_info_layout.addStretch(0)
        self.song_info_layout.addWidget(self.song_title)
        self.song_info_layout.addWidget(self.song_artist)
        self.song_info_layout.addStretch(0)

        # =================PREVIOUS - PLAY - NEXT=================
        self.music_play_buttons_layout = QHBoxLayout()
        self.music_play_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.left.addLayout(self.music_play_buttons_layout)

        self.previous_song_btn = iconButtonFactory.createButton(
            type="hidden-primary",
            padding=0.5,
            iconSize=icons.SIZES.SMALL,
            icon=IconUtils.changeColor(
                icons.PREVIOUS, ColorUtils.getQColorFromColor(Colors.PRIMARY)
            ),
            cursor=cursors.HAND,
        )
        self.music_play_buttons_layout.addWidget(self.previous_song_btn)

        self.play_song_btn = iconButtonFactory.createButton(
            type="checkable-primary",
            padding=0.75,
            iconSize=icons.SIZES.MEDIUM,
            icon=IconUtils.changeColor(
                icons.PLAY, ColorUtils.getQColorFromColor(Colors.PRIMARY)
            ),
            checkedIcon=IconUtils.changeColor(
                icons.PAUSE, ColorUtils.getQColorFromColor(Colors.PRIMARY)
            ),
            cursor=cursors.HAND,
        )
        self.play_song_btn.setChecked(False)
        self.music_play_buttons_layout.addWidget(self.play_song_btn)

        self.next_song_btn = iconButtonFactory.createButton(
            type="hidden-primary",
            padding=0.5,
            iconSize=icons.SIZES.SMALL,
            icon=IconUtils.changeColor(
                icons.NEXT, ColorUtils.getQColorFromColor(Colors.PRIMARY)
            ),
            cursor=cursors.HAND,
        )
        self.music_play_buttons_layout.addWidget(self.next_song_btn)
        self.music_play_buttons_layout.setSpacing(8)

        # =================CENTER=================
        self.center = QWidget()

        self.main_layout.addWidget(self.center, 0, alignment.CENTER)
        self.center_layout = QHBoxLayout(self.center)
        self.center_layout.setContentsMargins(0, 0, 0, 0)

        self.time_playing = QLabel()
        self.center_layout.addWidget(self.time_playing)

        self.time_slider = slider.export(12)
        self.time_slider.setFixedSize(250, 12)

        self.time_slider.setProperty("value", 0)
        self.time_slider.setOrientation(Qt.Horizontal)
        self.time_slider.setTickPosition(QSlider.NoTicks)
        self.center_layout.addWidget(self.time_slider)

        self.time_end = QLabel()
        self.center_layout.addWidget(self.time_end)

        # =================RIGHT=================

        self.right = QHBoxLayout()
        self.right.setContentsMargins(0, 0, 0, 0)
        self.right.setSpacing(8)
        self.main_layout.addLayout(self.right)

        self.loop_btn = iconButtonFactory.createButton(
            type="checkable-hidden-primary-danger",
            padding=1,
            iconSize=icons.SIZES.SMALL,
            icon=IconUtils.changeColor(
                icons.LOOP, ColorUtils.getQColorFromColor(Colors.PRIMARY)
            ),
            checkedIcon=IconUtils.changeColor(
                icons.LOOP, ColorUtils.getQColorFromColor(Colors.DANGER)
            ),
            cursor=cursors.HAND,
        )
        self.right.addWidget(self.loop_btn)

        self.shuffle_btn = iconButtonFactory.createButton(
            type="checkable-hidden-primary-danger",
            padding=1,
            iconSize=icons.SIZES.SMALL,
            icon=IconUtils.changeColor(
                icons.SHUFFLE, ColorUtils.getQColorFromColor(Colors.PRIMARY)
            ),
            checkedIcon=IconUtils.changeColor(
                icons.SHUFFLE, ColorUtils.getQColorFromColor(Colors.DANGER)
            ),
            cursor=cursors.HAND,
        )
        self.right.addWidget(self.shuffle_btn)

        self.love_btn = iconButtonFactory.createButton(
            type="checkable-hidden-primary-danger",
            padding=1,
            iconSize=icons.SIZES.SMALL,
            icon=IconUtils.changeColor(
                icons.LOVE, ColorUtils.getQColorFromColor(Colors.PRIMARY)
            ),
            checkedIcon=IconUtils.changeColor(
                icons.LOVE, ColorUtils.getQColorFromColor(Colors.DANGER)
            ),
            cursor=cursors.HAND,
        )
        self.right.addWidget(self.love_btn)

        self.volume_btn = iconButtonFactory.createButton(
            type="hidden-primary",
            padding=1,
            iconSize=icons.SIZES.SMALL,
            icon=IconUtils.changeColor(
                icons.VOLUME_UP, ColorUtils.getQColorFromColor(Colors.PRIMARY)
            ),
            cursor=cursors.HAND,
        )
        self.volume_btn.clicked.connect(self.showVolumeSlider)
        self.right.addWidget(self.volume_btn)

        self.timer_boxs = QWidget()
        self.timer_boxs_layout = QHBoxLayout(self.timer_boxs)
        self.timer_boxs_layout.setContentsMargins(0, 0, 0, 0)
        self.right.addWidget(self.timer_boxs, 1)

        slider.background = Background(
            color=BackgroundColor(
                normal=Colors.PRIMARY.withAlpha(0.15),
                hover=Colors.PRIMARY.withAlpha(0.25),
            ),
            roundness=12,
        )

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
        self.timer_box.setAlignment(alignment.CENTER)
        self.timer_box.setPlaceholderText("Enter Minute")
        self.timer_box.setValidator(QIntValidator())
        self.timer_box.setVisible(False)
        self.timer_boxs_layout.addWidget(self.timer_box)

        self.timer_btn = iconButtonFactory.createButton(
            type="hidden-primary",
            padding=1,
            iconSize=icons.SIZES.SMALL,
            icon=IconUtils.changeColor(
                icons.TIMER, ColorUtils.getQColorFromColor(Colors.PRIMARY)
            ),
            cursor=cursors.HAND,
        )
        self.timer_btn.clicked.connect(self.showTimerBox)
        self.right.addWidget(self.timer_btn)

        QMetaObject.connectSlotsByName(self)

    def changeVolumeIcon(self):
        volume: int = self.volume_slider.value()
        icons = Icons()
        if volume == 0:
            self.volume_btn.setIcon(
                IconUtils.changeColor(
                    icons.VOLUME_SILENT,
                    ColorUtils.getQColorFromColor(Colors.PRIMARY),
                )
            )
            return
        if volume <= 50:
            self.volume_btn.setIcon(
                IconUtils.changeColor(
                    icons.VOLUME_DOWN,
                    ColorUtils.getQColorFromColor(Colors.PRIMARY),
                )
            )
            return
        self.volume_btn.setIcon(
            IconUtils.changeColor(
                icons.VOLUME_UP, ColorUtils.getQColorFromColor(Colors.PRIMARY)
            )
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
