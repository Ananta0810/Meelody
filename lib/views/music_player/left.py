from typing import Optional

from constants.ui.qss import Backgrounds, ColorBoxes, Colors, Paddings
from constants.ui.qt import AppCursors, AppIcons
from modules.screens.components.font_builder import FontBuilder
from modules.screens.components.icon_buttons import IconButton, ToggleIconButton
from modules.screens.components.labels import StandardLabel
from modules.screens.themes.theme_builders import ButtonThemeBuilder, LabelThemeBuilder
from PyQt5.QtCore import QMetaObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from utils.ui.application_utils import UiUtils
from views.view import View
from widgets.image_displayer import ImageDisplayer


class MusicPlayerLeftSide(QHBoxLayout, View):
    def __init__(self, parent: Optional["QWidget"] = None):
        super(MusicPlayerLeftSide, self).__init__(parent)
        self.setupUi()

    def setupUi(self) -> None:
        icons = AppIcons()
        cursors = AppCursors()
        buttonThemeBuilder = ButtonThemeBuilder()
        changeSongBtnTheme = (
            buttonThemeBuilder.addLightModeBackground(Backgrounds.CIRCLE_HIDDEN_PRIMARY_25)
            .addDarkModeBackground(None)
            .build(itemSize=icons.SIZES.LARGE.height())
        )
        labelThemeBuilder = LabelThemeBuilder()
        fontBuilder = FontBuilder()

        # =================Ui=================
        self.songCover = ImageDisplayer()
        self.songCover.setFixedSize(64, 64)
        self.addWidget(self.songCover)

        self.songTitle = StandardLabel.render(font=fontBuilder.withSize(10).withWeight("bold").build())
        self._addThemeForItem(
            self.songTitle,
            labelThemeBuilder.addLightModeTextColor(ColorBoxes.BLACK).addDarkModeTextColor(ColorBoxes.WHITE).build(),
        )
        self.songArtist = StandardLabel.render(font=fontBuilder.withSize(9).withWeight("normal").build())
        self._addThemeForItem(
            self.songArtist,
            labelThemeBuilder.addLightModeTextColor(ColorBoxes.GRAY).addDarkModeTextColor(ColorBoxes.WHITE).build(),
        )
        self.songInfoLayout = QVBoxLayout()
        self.songInfoLayout.setContentsMargins(0, 0, 0, 0)
        self.songInfoLayout.setSpacing(0)
        self.addLayout(self.songInfoLayout, stretch=1)
        self.songInfoLayout.addStretch(0)
        self.songInfoLayout.addWidget(self.songTitle)
        self.songInfoLayout.addWidget(self.songArtist)
        self.songInfoLayout.addStretch(0)

        # =================PREVIOUS - PLAY - NEXT=================
        self.playerButtons = QHBoxLayout()
        self.playerButtons.setContentsMargins(0, 0, 0, 0)
        self.playerButtons.setSpacing(8)
        self.addLayout(self.playerButtons)

        self.prevSongBtn = IconButton.render(
            padding=Paddings.RELATIVE_50,
            size=icons.SIZES.LARGE,
            lightModeIcon=UiUtils.paintIcon(icons.PREVIOUS, Colors.PRIMARY),
        )
        self.prevSongBtn.setCursor(cursors.HAND)
        self.playerButtons.addWidget(self.prevSongBtn)
        self._addThemeForItem(item=self.prevSongBtn, theme=changeSongBtnTheme)

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
        self.playerButtons.addWidget(self.playBtn)
        self._addButtonToList(self.playBtn)

        self.nextSongBtn = IconButton.render(
            padding=Paddings.RELATIVE_50,
            size=icons.SIZES.LARGE,
            lightModeIcon=UiUtils.paintIcon(icons.NEXT, Colors.PRIMARY),
        )
        self.nextSongBtn.setCursor(cursors.HAND)
        self.playerButtons.addWidget(self.nextSongBtn)
        self._addThemeForItem(self.nextSongBtn, changeSongBtnTheme)
        QMetaObject.connectSlotsByName(self)

    def setPlayingState(self, state: bool) -> None:
        self.playBtn.setChecked(state)

    def isPlaying(self) -> bool:
        return self.playBtn.isChecked()

    def setTitle(self, title: str) -> None:
        self.songTitle.setText(title)
        self.songTitle.setCursorPosition(0)

    def setArtist(self, artist: str) -> None:
        self.songArtist.setText(artist)
        self.songArtist.setCursorPosition(0)

    def setCover(self, cover: bytes) -> None:
        self.songCover.setPixmap(self.__getPixmapForSongCover(cover))

    def setDefaultCover(self, cover: bytes) -> None:
        self.songCover.setDefaultPixmap(self.__getPixmapForSongCover(cover))

    def __getPixmapForSongCover(self, coverAsByte: bytes) -> QPixmap:
        if coverAsByte is None:
            return None
        pixmap = UiUtils.getSquaredPixmapFromBytes(coverAsByte, edge=64, radius=12)
        return pixmap
