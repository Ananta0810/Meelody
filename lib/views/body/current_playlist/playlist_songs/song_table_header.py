from typing import Optional

from constants.ui.qss import Backgrounds, ColorBoxes, Colors, Paddings
from constants.ui.qt import AppCursors, AppIcons
from modules.screens.components.font_builder import FontBuilder
from modules.screens.components.icon_buttons import IconButton
from modules.screens.components.labels import StandardLabel
from modules.screens.themes.theme_builders import (ButtonThemeBuilder,
                                                   LabelThemeBuilder)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QWidget
from utils.ui.application_utils import UiUtils
from views.view import View


class SongTableHeader(QWidget, View):
    def __init__(self, parent: Optional["QWidget"] = None):
        super(SongTableHeader, self).__init__(parent)
        self.setupUi()
        self.setText()

    def setupUi(self) -> None:
        SCROLLBAR_WIDTH = 4
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setContentsMargins(28, 0, 28 + SCROLLBAR_WIDTH, 0)
        self.mainLayout.setSpacing(0)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.info = QHBoxLayout()
        self.info.setContentsMargins(0, 0, 0, 0)
        self.info.setSpacing(24)

        self.buttons = QWidget()
        self.buttonsLayout = QHBoxLayout(self.buttons)
        self.buttonsLayout.setAlignment(Qt.AlignRight)
        self.buttonsLayout.setSpacing(8)
        self.buttonsLayout.setContentsMargins(8, 0, 8, 0)

        self.mainLayout.addLayout(self.info)
        self.mainLayout.addWidget(self.buttons)

        font = FontBuilder().withSize(9).build()
        labelTheme = (
            LabelThemeBuilder().addLightModeTextColor(ColorBoxes.BLACK).addDarkModeTextColor(ColorBoxes.WHITE).build()
        )

        self.track = StandardLabel.render(font)
        self.track.setFixedWidth(64)
        self.track.setAlignment(Qt.AlignCenter)
        self._addThemeForItem(self.track, labelTheme)
        self.info.addWidget(self.track)
        self.info.addStretch(1)
        self.info.addSpacing(24)

        self.artist = StandardLabel.render(font)
        self._addThemeForItem(self.artist, labelTheme)
        self.info.addWidget(self.artist, 1)

        self.length = StandardLabel.render(font)
        self.length.setFixedWidth(64)
        self.length.setAlignment(Qt.AlignCenter)
        self._addThemeForItem(self.length, labelTheme)
        self.info.addWidget(self.length)

        icons = AppIcons()
        buttonTheme = (
            ButtonThemeBuilder()
            .addLightModeBackground(Backgrounds.CIRCLE_PRIMARY_25)
            .addDarkModeBackground(Backgrounds.CIRCLE_WHITE_25)
            .build(icons.SIZES.LARGE.height())
        )

        self.buttonsLayout.addSpacing(48)
        self.buttonsLayout.addSpacing(8)

        self.downloadSongsBtn = IconButton.render(
            size=icons.SIZES.LARGE,
            padding=Paddings.RELATIVE_50,
            lightModeIcon=UiUtils.paintIcon(icons.DOWNLOAD, Colors.PRIMARY),
            darkModeIcon=UiUtils.paintIcon(icons.DOWNLOAD, Colors.WHITE),
        )
        self.downloadSongsBtn.setCursor(AppCursors().HAND)
        self._addButtonToList(self.downloadSongsBtn)
        self._addThemeForItem(self.downloadSongsBtn, theme=buttonTheme)
        self.buttonsLayout.addWidget(self.downloadSongsBtn)

        self.addSongBtn = IconButton.render(
            size=icons.SIZES.LARGE,
            padding=Paddings.RELATIVE_75,
            lightModeIcon=UiUtils.paintIcon(icons.ADD, Colors.PRIMARY),
            darkModeIcon=UiUtils.paintIcon(icons.ADD, Colors.WHITE),
        )
        self.addSongBtn.setCursor(AppCursors().HAND)
        self._addButtonToList(self.addSongBtn)
        self._addThemeForItem(self.addSongBtn, theme=buttonTheme)
        self.buttonsLayout.addWidget(self.addSongBtn)

    def setText(self, track="TRACK", artist: str = "ARTIST", length: str = "LENGTH") -> None:
        self.track.setText(track)
        self.artist.setText(artist)
        self.length.setText(length)
