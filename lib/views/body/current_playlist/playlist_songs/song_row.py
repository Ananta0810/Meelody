from typing import Optional

from constants.ui.qss import Colors, Paddings
from constants.ui.qt import AppCursors, AppIcons, IconSizes
from modules.screens.components.font_builder import FontBuilder
from modules.screens.components.icon_buttons import IconButton, ToggleIconButton
from modules.screens.components.labels import DoubleClickedEditableLabel, LabelWithDefaultText
from modules.screens.themes.theme_builders import ThemeData
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QWidget
from utils.helpers.my_string import Stringify
from utils.ui.application_utils import UiUtils
from views.view import View
from widgets.image_displayer import ImageDisplayer
from widgets.mouse_observer import ClickObserver


# @memory.cache
def getSongCoverPixmap(coverAsByte: bytes) -> QPixmap:
    if coverAsByte is None:
        return None
    return UiUtils.getEditedPixmapFromBytes(coverAsByte, width=64, height=64, radius=12)


class SongItem(QWidget, View):
    def __init__(self, parent: Optional["QWidget"] = None):
        super(SongItem, self).__init__(parent)
        self.defaultArtist = ""
        self.setupUi()

    def setupUi(self) -> None:
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setContentsMargins(20, 12, 20, 12)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setAlignment(Qt.AlignLeft)
        self.setLayout(self.mainLayout)

        self.info = QHBoxLayout()
        self.info.setSpacing(24)
        self.info.setContentsMargins(0, 8, 0, 8)

        self.buttons = QWidget()
        self.buttonsLayout = QHBoxLayout(self.buttons)
        self.buttonsLayout.setContentsMargins(8, 8, 8, 8)
        self.buttonsLayout.setSpacing(8)

        self.extraButtons = QWidget()
        self.extraButtonsLayout = QHBoxLayout(self.extraButtons)
        self.extraButtonsLayout.setSpacing(8)
        self.extraButtonsLayout.setContentsMargins(8, 8, 8, 8)

        self.mainLayout.addLayout(self.info)
        self.mainLayout.addWidget(self.buttons)
        self.mainLayout.addWidget(self.extraButtons)

        self.cover = ImageDisplayer(self)
        self.cover.setFixedSize(64, 64)
        self.info.addWidget(self.cover)
        self.coverObserver = ClickObserver(self.cover)

        font = FontBuilder().withSize(10).build()
        self.title = DoubleClickedEditableLabel.render(font)
        self.info.addWidget(self.title, 1)

        self.artist = DoubleClickedEditableLabel.render(font)
        self.info.addWidget(self.artist, 1)

        self.length = LabelWithDefaultText.render(font)
        self.length.setFixedWidth(64)
        self.length.setAlignment(Qt.AlignCenter)
        self.info.addWidget(self.length)

        icons = AppIcons()
        btnCursor = AppCursors().HAND
        self.moreBtn = IconButton.render(
            size=IconSizes.LARGE,
            padding=Paddings.RELATIVE_50,
            lightModeIcon=UiUtils.paintIcon(icons.MORE, Colors.PRIMARY),
        )
        self.moreBtn.setCursor(btnCursor)
        self.moreBtn.clicked.connect(self.showMore)
        self._addButtonToList(self.moreBtn)
        self.buttonsLayout.addWidget(self.moreBtn)

        self.loveBtn = ToggleIconButton.render(
            size=IconSizes.LARGE,
            padding=Paddings.RELATIVE_50,
            lightModeIcon=UiUtils.paintIcon(icons.LOVE, Colors.PRIMARY),
            lightModeCheckedIcon=UiUtils.paintIcon(icons.LOVE, Colors.DANGER),
        )
        self.loveBtn.setCursor(btnCursor)
        self._addButtonToList(self.loveBtn)
        self.buttonsLayout.addWidget(self.loveBtn)

        self.playBtn = IconButton.render(
            size=IconSizes.LARGE,
            padding=Paddings.RELATIVE_50,
            lightModeIcon=UiUtils.paintIcon(icons.PLAY, Colors.PRIMARY),
            darkModeIcon=UiUtils.paintIcon(icons.PLAY, Colors.WHITE),
        )
        self.playBtn.setCursor(btnCursor)
        self._addButtonToList(self.playBtn)
        self.buttonsLayout.addWidget(self.playBtn)

        self.addToPlaylistBtn = IconButton.render(
            size=IconSizes.LARGE,
            padding=Paddings.RELATIVE_75,
            lightModeIcon=UiUtils.paintIcon(icons.ADD, Colors.PRIMARY),
        )
        self.addToPlaylistBtn.setCursor(btnCursor)
        self._addButtonToList(self.addToPlaylistBtn)
        self.extraButtonsLayout.addWidget(self.addToPlaylistBtn)

        self.editBtn = IconButton.render(
            size=IconSizes.LARGE,
            padding=Paddings.RELATIVE_50,
            lightModeIcon=UiUtils.paintIcon(icons.EDIT, Colors.PRIMARY),
        )
        self.editBtn.setCursor(btnCursor)
        self._addButtonToList(self.editBtn)
        self.extraButtonsLayout.addWidget(self.editBtn)

        self.deleteBtn = IconButton.render(
            size=IconSizes.LARGE,
            padding=Paddings.RELATIVE_50,
            lightModeIcon=UiUtils.paintIcon(icons.DELETE, Colors.PRIMARY),
        )
        self.deleteBtn.setCursor(btnCursor)
        self._addButtonToList(self.deleteBtn)
        self.extraButtonsLayout.addWidget(self.deleteBtn)

        self.closeBtn = IconButton.render(
            size=IconSizes.MEDIUM,
            padding=Paddings.RELATIVE_50,
            lightModeIcon=UiUtils.paintIcon(icons.CLOSE, Colors.WHITE),
            parent=self,
        )
        self.closeBtn.move(
            self.sizeHint().width() - IconSizes.MEDIUM.width() / 2,
            self.extraButtons.rect().top() + 4,
        )
        self.closeBtn.setCursor(btnCursor)
        self.closeBtn.clicked.connect(lambda: self.showLess())
        self._addButtonToList(self.closeBtn)

        self.showLess()

    def showMore(self):
        self.buttons.hide()
        self.closeBtn.show()
        self.extraButtons.show()

    def showLess(self):
        self.buttons.show()
        self.closeBtn.hide()
        self.extraButtons.hide()

    def setWidgetThemes(self, theme: ThemeData) -> None:
        self._addThemeForItem(self, theme)
        self._addThemeForItem(self.extraButtons, theme)

    def setButtonThemes(self, primary: ThemeData, secondary: ThemeData, danger: ThemeData) -> None:
        self._addThemeForItem(self.moreBtn, primary)
        self._addThemeForItem(self.loveBtn, primary)
        self._addThemeForItem(self.deleteBtn, primary)
        self._addThemeForItem(self.editBtn, primary)
        self._addThemeForItem(self.addToPlaylistBtn, primary)
        self._addThemeForItem(self.playBtn, secondary)
        self._addThemeForItem(self.closeBtn, danger)

    def setTextThemes(self, primary: ThemeData, secondary: ThemeData) -> None:
        self._addThemeForItem(self.title, primary)
        self._addThemeForItem(self.artist, secondary)
        self._addThemeForItem(self.length, secondary)

    def setCover(self, cover: bytes) -> None:
        self.cover.setPixmap(getSongCoverPixmap(cover))

    def setTitle(self, title: str) -> None:
        if title is None:
            title = self.defaultTitle
        self.title.setText(title)
        self.title.setCursorPosition(0)

    def setArtist(self, artist: str) -> None:
        if artist is None:
            artist = self.defaultArtist
        self.artist.setText(artist)
        self.artist.setCursorPosition(0)

    def setLength(self, length: float) -> None:
        if length is None:
            length = self.defaultLength
        self.length.setText(Stringify.floatToClockTime(length))

    def setLoveState(self, state: bool) -> None:
        self.loveBtn.setChecked(state)

    # def setDefaultCover(self, cover: bytes) -> None:
    #     self.cover.setDefaultPixmap(getSongCoverPixmap(cover))

    def setDefaultCover(self, cover: QPixmap) -> None:
        self.cover.setDefaultPixmap(cover)

    def setDefaultArtist(self, artist: str) -> None:
        self.defaultArtist = artist

    def clearInfo(self):
        self.setCover(None)
