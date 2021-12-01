from sys import path

from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtGui import QCursor, QIntValidator
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QWidget

path.append("./lib")
from constants.ui import alignment, colors, icons, images
from constants.ui.qss import *
from modules.screens.components.buttons.icon_button_factory import IconButtonFactory
from modules.screens.components.font_builder import FontBuilder
from modules.screens.components.label_factory import LabelFactory
from modules.screens.components.slider_factory import SliderFactory
from modules.screens.qss.qss_elements import *
from utils.helpers.my_string import Stringify
from utils.ui.application_ui_utils import ApplicationUIUtils as AppUI
from widgets.image_label import ImageLabel


class UIPlayerMusic(QWidget):
    def setupUi(self):
        ICONS = icons.Icons()
        ALIGNMENT = alignment.Alignment()
        buttonFactory = IconButtonFactory()
        fontBuilder = FontBuilder()
        COLORS = colors.Colors
        HAND_CURSOR = QCursor(Qt.PointingHandCursor)
        APP_IMGS = images.ApplicationImage

        standardIconButtonRenderer = buttonFactory.getButton("")
        toggleButtonRenderer = buttonFactory.getButton("toggle")
        multipleIconButtonRenderer = buttonFactory.getButton("multiple-icon")
        horizontalSlider = SliderFactory().get(type="horizontal")
        labelFactory = LabelFactory()
        standardLabelRenderer = labelFactory.getLabel("")

        normalIconButtonBackground = QSSBackground(
            borderRadius=0.5,
            color=QSSColors.HIDDEN_PRIMARY,
        )
        checkedIconButtonBackground = QSSBackground(
            borderRadius=0.5,
            color=QSSColors.HIDDEN_DANGER,
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
        self.song_cover.setDefaultPixmap(
            self.getPixmapForSongCover(APP_IMGS.defaultSongCover)
        )
        self.song_cover.setPixmap(None)
        self.left.addWidget(self.song_cover)

        self.song_info_layout = QVBoxLayout()
        self.song_info_layout.setContentsMargins(0, 0, 0, 0)
        self.song_info_layout.setSpacing(0)
        self.left.addLayout(self.song_info_layout, stretch=1)

        self.song_title = standardLabelRenderer.render(
            font=QSSFont(fontBuilder.withSize(10).withWeight("bold").build()),
        )
        self.song_title.setText("Song's artist")

        self.song_artist = standardLabelRenderer.render(
            font=QSSFont(fontBuilder.withSize(10).build())
        )
        self.song_artist.setText("Song's artist")

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
            padding=QSSPaddings.RELATIVE_50,
            iconSize=ICONS.SIZES.SMALL,
            icon=AppUI.paintIcon(ICONS.PREVIOUS, COLORS.PRIMARY),
            background=normalIconButtonBackground,
        )
        self.previous_song_btn.setCursor(HAND_CURSOR)
        self.play_buttons.addWidget(self.previous_song_btn)

        self.play_song_btn = toggleButtonRenderer.render(
            padding=QSSPaddings.RELATIVE_75,
            iconSize=ICONS.SIZES.MEDIUM,
            icon=AppUI.paintIcon(ICONS.PLAY, COLORS.PRIMARY),
            checkedIcon=AppUI.paintIcon(ICONS.PAUSE, COLORS.PRIMARY),
            background=QSSBackground(
                borderRadius=0.5,
                color=QSSColors.PRIMARY,
            ),
        )
        self.play_song_btn.setChecked(False)
        self.play_song_btn.setCursor(HAND_CURSOR)
        self.play_buttons.addWidget(self.play_song_btn)

        self.next_song_btn = standardIconButtonRenderer.render(
            padding=QSSPaddings.RELATIVE_50,
            iconSize=ICONS.SIZES.SMALL,
            icon=AppUI.paintIcon(ICONS.NEXT, COLORS.PRIMARY),
            background=normalIconButtonBackground,
        )
        self.next_song_btn.setCursor(HAND_CURSOR)
        self.play_buttons.addWidget(self.next_song_btn)

        # =================CENTER=================
        self.center = QWidget()

        self.main_layout.addWidget(self.center, 0, ALIGNMENT.CENTER)
        self.center_layout = QHBoxLayout(self.center)
        self.center_layout.setContentsMargins(0, 0, 0, 0)

        self.playing_time = QLabel()
        self.center_layout.addWidget(self.playing_time)
        self.displayPlayingTime(0)

        self.time_slider = horizontalSlider.render(
            height=12,
            lineColor=QSSColors.PRIMARY,
            handleColor=QSSColors.FLAT_PRIMARY,
        )
        self.time_slider.setFixedSize(250, 12)
        self.time_slider.setProperty("value", 0)
        self.center_layout.addWidget(self.time_slider)

        self.total_time = QLabel()
        self.center_layout.addWidget(self.total_time)
        self.displayTotalTime(0)

        # =================RIGHT=================
        self.right = QHBoxLayout()
        self.right.setContentsMargins(0, 0, 0, 0)
        self.right.setSpacing(8)
        self.main_layout.addLayout(self.right)

        self.loop_btn = toggleButtonRenderer.render(
            padding=QSSPaddings.RELATIVE_100,
            iconSize=ICONS.SIZES.SMALL,
            icon=AppUI.paintIcon(ICONS.LOOP, COLORS.PRIMARY),
            checkedIcon=AppUI.paintIcon(ICONS.LOOP, COLORS.DANGER),
            background=normalIconButtonBackground,
            checkedBackground=checkedIconButtonBackground,
        )
        self.loop_btn.setCursor(HAND_CURSOR)
        self.right.addWidget(self.loop_btn)

        self.shuffle_btn = toggleButtonRenderer.render(
            padding=QSSPaddings.RELATIVE_100,
            iconSize=ICONS.SIZES.SMALL,
            icon=AppUI.paintIcon(ICONS.SHUFFLE, COLORS.PRIMARY),
            checkedIcon=AppUI.paintIcon(ICONS.SHUFFLE, COLORS.DANGER),
            background=normalIconButtonBackground,
            checkedBackground=checkedIconButtonBackground,
        )
        self.shuffle_btn.setCursor(HAND_CURSOR)
        self.right.addWidget(self.shuffle_btn)

        self.love_btn = toggleButtonRenderer.render(
            padding=QSSPaddings.RELATIVE_100,
            iconSize=ICONS.SIZES.SMALL,
            icon=AppUI.paintIcon(ICONS.LOVE, COLORS.PRIMARY),
            checkedIcon=AppUI.paintIcon(ICONS.LOVE, COLORS.DANGER),
            background=normalIconButtonBackground,
            checkedBackground=checkedIconButtonBackground,
        )
        self.love_btn.setCursor(HAND_CURSOR)
        self.right.addWidget(self.love_btn)

        self.volume_btn = multipleIconButtonRenderer.render(
            padding=QSSPaddings.RELATIVE_100,
            iconSize=ICONS.SIZES.SMALL,
            icons=[
                AppUI.paintIcon(ICONS.VOLUME_UP, COLORS.PRIMARY),
                AppUI.paintIcon(ICONS.VOLUME_DOWN, COLORS.PRIMARY),
                AppUI.paintIcon(ICONS.VOLUME_SILENT, COLORS.PRIMARY),
            ],
            background=normalIconButtonBackground,
        )
        self.volume_btn.setCursor(HAND_CURSOR)
        self.volume_btn.clicked.connect(self.showVolumeSlider)
        self.right.addWidget(self.volume_btn)

        self.timer_boxs = QWidget()
        self.timer_boxs_layout = QHBoxLayout(self.timer_boxs)
        self.timer_boxs_layout.setContentsMargins(0, 0, 0, 0)
        self.right.addWidget(self.timer_boxs, 1)

        self.volume_slider = horizontalSlider.render(
            height=48,
            lineColor=QSSColors.PRIMARY,
            handleColor=QSSColors.FLAT_PRIMARY,
            background=QSSBackground(
                borderRadius=12,
                color=QSSColors.BLACK,
            ),
        )
        self.volume_slider.setSliderPosition(100)
        self.volume_slider.setVisible(False)
        self.volume_slider.valueChanged.connect(self.changeVolumeIcon)
        self.timer_boxs_layout.addWidget(self.volume_slider)

        self.timer_box = labelFactory.getLabel("editable").render(
            font=QSSFont(fontBuilder.withSize(10).withWeight("bold").build()),
            alignment=ALIGNMENT.CENTER,
            background=QSSBackground(
                borderRadius=12,
                color=QSSColors.BLACK,
            ),
        )
        self.timer_box.setFixedHeight(48)
        self.timer_box.setPlaceholderText("Enter Minute")
        self.timer_box.setValidator(QIntValidator())
        self.timer_box.setVisible(False)
        self.timer_boxs_layout.addWidget(self.timer_box)

        self.timer_btn = standardIconButtonRenderer.render(
            padding=QSSPaddings.RELATIVE_100,
            iconSize=ICONS.SIZES.SMALL,
            icon=AppUI.paintIcon(ICONS.TIMER, COLORS.PRIMARY),
            background=normalIconButtonBackground,
        )
        self.timer_btn.setCursor(HAND_CURSOR)
        self.timer_btn.clicked.connect(self.showTimerBox)
        self.right.addWidget(self.timer_btn)

        QMetaObject.connectSlotsByName(self)

    def displaySongInfo(self, cover, title, artist):
        coverAsPixmap = None
        if cover is not None:
            coverAsPixmap = self.getPixmapForSongCover(cover)
        self.song_cover.setPixmap(coverAsPixmap)
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
        self.timer_box.clear()
        self.volume_slider.setVisible(False)

    def displayPlayingTime(self, time: float):
        self.playing_time.setText(Stringify.floatToClockTime(time))

    def displayTotalTime(self, time: float):
        self.total_time.setText(Stringify.floatToClockTime(time))

    def runTimeSlider(self, currentTime: float, totalTime: float):
        position = int(currentTime * 100 / totalTime)
        self.time_slider.setSliderPosition(position)

    def isLooping(self) -> bool:
        return self.loop_btn.isChecked()

    def isShuffling(self) -> bool:
        return self.shuffle_btn.isChecked()

    def isPlaying(self) -> bool:
        return self.play_song_btn.isChecked()

    def getTimerValue(self) -> int:
        return int(self.timer_box.text())

    def closeTimerBox(self):
        self.timer_box.clear()
        self.timer_box.hide()
