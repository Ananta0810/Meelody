from typing import Optional, Union

from constants.ui.qss import ColorBoxes, Colors, Paddings
from constants.ui.qt import AppCursors, AppIcons
from modules.screens.components.font_builder import FontBuilder
from modules.screens.components.icon_buttons import IconButton
from modules.screens.components.labels import StandardLabel
from modules.screens.qss.qss_elements import Background
from modules.screens.themes.theme_builders import ButtonThemeBuilder, LabelThemeBuilder, ThemeData
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from utils.ui.application_utils import UiUtils


class PlaylistTableHeader(QWidget):
    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent=parent)
        self.setupUi()
        self.setText()

    def setupUi(self) -> None:
        self.themeItems = {}
        self.buttonsWithDarkMode = []

        # self.setAttribute(Qt.style)
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setContentsMargins(28, 0, 28, 0)
        self.mainLayout.setSpacing(0)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.info = QHBoxLayout()
        self.info.setContentsMargins(0, 0, 0, 0)
        self.info.setSpacing(24)

        self.buttons = QWidget()
        self.buttons.setFixedWidth(178)
        self.buttonsLayout = QHBoxLayout(self.buttons)
        self.buttonsLayout.setAlignment(Qt.AlignRight)

        self.mainLayout.addLayout(self.info)
        self.mainLayout.addWidget(self.buttons)

        font: QFont = FontBuilder().withSize(9).build()
        labelTheme = (
            LabelThemeBuilder().addLightModeTextColor(ColorBoxes.BLACK).addDarkModeTextColor(ColorBoxes.WHITE).build()
        )

        self.track = StandardLabel.render(font)
        self.track.setFixedWidth(64)
        self.track.setAlignment(Qt.AlignCenter)
        self.__addThemeForItem(self.track, labelTheme)
        self.info.addWidget(self.track)
        self.info.addStretch(1)
        self.info.addSpacing(24)

        self.artist = StandardLabel.render(font)
        self.__addThemeForItem(self.artist, labelTheme)
        self.info.addWidget(self.artist, 1)

        self.length = StandardLabel.render(font)
        self.length.setFixedWidth(64)
        self.length.setAlignment(Qt.AlignCenter)
        self.__addThemeForItem(self.length, labelTheme)
        self.info.addWidget(self.length)

        icons = AppIcons()
        buttonTheme = (
            ButtonThemeBuilder()
            .addLightModeBackground(
                Background(
                    borderRadius=0.5,
                    color=ColorBoxes.HOVERABLE_PRIMARY_25,
                )
            )
            .addDarkModeBackground(
                Background(
                    borderRadius=0.5,
                    color=ColorBoxes.HOVERABLE_WHITE_25,
                )
            )
            .build(icons.SIZES.LARGE.height())
        )

        self.downloadSongsBtn = IconButton.render(
            size=icons.SIZES.LARGE,
            padding=Paddings.RELATIVE_50,
            lightModeIcon=UiUtils.paintIcon(icons.DOWNLOAD, Colors.PRIMARY),
            darkModeIcon=UiUtils.paintIcon(icons.DOWNLOAD, Colors.WHITE),
        )
        self.downloadSongsBtn.setCursor(AppCursors().HAND)
        self.__addButtonToList(self.downloadSongsBtn)
        self.__addThemeForItem(self.downloadSongsBtn, theme=buttonTheme)
        self.buttonsLayout.addWidget(self.downloadSongsBtn)

        self.addSongBtn = IconButton.render(
            size=icons.SIZES.LARGE,
            padding=Paddings.RELATIVE_75,
            lightModeIcon=UiUtils.paintIcon(icons.ADD, Colors.PRIMARY),
            darkModeIcon=UiUtils.paintIcon(icons.ADD, Colors.WHITE),
        )
        self.addSongBtn.setCursor(AppCursors().HAND)
        self.__addButtonToList(self.addSongBtn)
        self.__addThemeForItem(self.addSongBtn, theme=buttonTheme)
        self.buttonsLayout.addWidget(self.addSongBtn)

    def setText(self, track="TRACK", artist: str = "ARTIST", length: str = "LENGTH") -> None:
        self.track.setText(track)
        self.artist.setText(artist)
        self.length.setText(length)

    def lightMode(self) -> None:
        for button in self.buttonsWithDarkMode:
            button.setDarkMode(False)
        for item in self.themeItems:
            lightModeStyleSheet = self.themeItems.get(item).lightMode
            if lightModeStyleSheet is None or lightModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(lightModeStyleSheet)

    def darkMode(self) -> None:
        for button in self.buttonsWithDarkMode:
            button.setDarkMode(True)
        for item in self.themeItems:
            darkModeStyleSheet = self.themeItems.get(item).darkMode
            if darkModeStyleSheet is None or darkModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(darkModeStyleSheet)

    def __addButtonToList(self, item) -> None:
        self.buttonsWithDarkMode.append(item)

    def __addThemeForItem(self, item: Optional["QWidget"], theme: ThemeData) -> None:
        self.themeItems[item] = theme
