from typing import Optional

from constants.ui.qss import Backgrounds, ColorBoxes, Colors, Paddings
from constants.ui.qt import AppCursors, AppIcons
from modules.screens.components.font_builder import FontBuilder
from modules.screens.components.icon_buttons import IconButton, MultiIconButton, ToggleIconButton
from modules.screens.components.labels import EditableLabel
from modules.screens.components.sliders import HorizontalSlider
from modules.screens.themes.theme_builders import ButtonThemeBuilder, HorizontalSliderThemeBuilder, LabelThemeBuilder
from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QHBoxLayout, QWidget
from utils.ui.application_utils import UiUtils
from views.view import View


class MusicPlayerRightSide(QHBoxLayout, View):
    def __init__(self, parent: Optional["QWidget"] = None):
        super(MusicPlayerRightSide, self).__init__(parent)
        self.setupUi()

    def setupUi(self) -> None:
        icons = AppIcons()
        cursors = AppCursors()
        buttonThemeBuilder = ButtonThemeBuilder()

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
        font = FontBuilder().withSize(10).withWeight("bold").build()

        # =================UI=================
        self.loopBtn = ToggleIconButton.render(
            size=icons.SIZES.LARGE,
            padding=Paddings.RELATIVE_50,
            lightModeIcon=UiUtils.paintIcon(icons.LOOP, Colors.PRIMARY),
            lightModeCheckedIcon=UiUtils.paintIcon(icons.LOOP, Colors.DANGER),
        )
        self.loopBtn.setCursor(cursors.HAND)
        self._addThemeForItem(self.loopBtn, toggleButtonThemeStyle)
        self.addWidget(self.loopBtn)

        self.shuffleBtn = ToggleIconButton.render(
            size=icons.SIZES.LARGE,
            padding=Paddings.RELATIVE_50,
            lightModeIcon=UiUtils.paintIcon(icons.SHUFFLE, Colors.PRIMARY),
            lightModeCheckedIcon=UiUtils.paintIcon(icons.SHUFFLE, Colors.DANGER),
        )
        self.shuffleBtn.setCursor(cursors.HAND)
        self.addWidget(self.shuffleBtn)
        self._addThemeForItem(self.shuffleBtn, toggleButtonThemeStyle)

        self.loveBtn = ToggleIconButton.render(
            size=icons.SIZES.LARGE,
            padding=Paddings.RELATIVE_50,
            lightModeIcon=UiUtils.paintIcon(icons.LOVE, Colors.PRIMARY),
            lightModeCheckedIcon=UiUtils.paintIcon(icons.LOVE, Colors.DANGER),
        )
        self.loveBtn.setCursor(cursors.HAND)
        self.addWidget(self.loveBtn)
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
        self.addWidget(self.volumeBtn)
        self._addThemeForItem(self.volumeBtn, normalButtonThemeStyle)

        self.inputs = QWidget()
        self.rightBoxes = QHBoxLayout(self.inputs)
        self.rightBoxes.setContentsMargins(0, 0, 0, 0)
        self.addWidget(self.inputs, 1)

        self.volumeSlider = HorizontalSlider.render(height=48)
        self._addThemeForItem(
            self.volumeSlider,
            theme=(
                HorizontalSliderThemeBuilder()
                .addLightHandleColor(ColorBoxes.PRIMARY)
                .addLightLineColor(ColorBoxes.HOVERABLE_PRIMARY_25)
                .addLightModeBackground(Backgrounds.ROUNDED_PRIMARY_25)
                .addDarkModeBackground(Backgrounds.ROUNDED_WHITE_25)
                .build(itemSize=48)
            ),
        )
        self.volumeSlider.setSliderPosition(100)
        self.volumeSlider.setVisible(False)
        self.volumeSlider.valueChanged.connect(self.__changeVolumeIcon)
        self.rightBoxes.addWidget(self.volumeSlider)

        self.timerInput = EditableLabel.render(font=font)
        self.timerInput.setAlignment(Qt.AlignCenter)
        self.timerInput.setFixedHeight(48)
        self.timerInput.setValidator(QIntValidator())
        self.timerInput.setVisible(False)
        self.rightBoxes.addWidget(self.timerInput)
        self._addThemeForItem(
            self.timerInput,
            theme=(
                LabelThemeBuilder()
                .addLightModeTextColor(ColorBoxes.PRIMARY)
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
        self.addWidget(self.timerBtn)
        self._addThemeForItem(self.timerBtn, normalButtonThemeStyle)
        QMetaObject.connectSlotsByName(self)

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

    def getTimeSliderPosition(self) -> int:
        return self.center.timeSlider.sliderPosition()

    def getCurrentVolumeValue(self) -> int:
        return self.volumeSlider.value()

    def closeTimerBox(self) -> None:
        self.timerInput.clear()
        self.timerInput.hide()

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
