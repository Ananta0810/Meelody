from constants.ui.base import ApplicationImage
from constants.ui.qss import ColorBoxes, Colors, Paddings
from constants.ui.qt import AppCursors, AppIcons
from modules.screens.components.editable_playlist_card import EditablePlaylistCard
from modules.screens.components.font_builder import FontBuilder
from modules.screens.components.icon_buttons import IconButton
from modules.screens.components.playlist_card import PlaylistCard
from modules.screens.others.animation import Animation
from modules.screens.qss.qss_elements import Background
from modules.screens.themes.theme_builders import ThemeData
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QScrollArea, QWidget
from utils.ui.application_utils import UiUtils
from utils.ui.application_utils import UiUtils as AppUtils


class UiPlaylistCarousel(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.themeItems = {}
        self.buttonsWithDarkMode = []
        self.isDarkMode = False
        self.setupUi()

    def setupUi(self):
        self.icons = AppIcons()
        self.cursors = AppCursors()

        self.playlistLabelFont = FontBuilder().withSize(16).withWeight("bold").build()
        self.buttonTheme = (
            IconButton.getThemeBuilder()
            .addLightModeBackground(
                Background(
                    borderRadius=0.5,
                    color=ColorBoxes.PRIMARY_LIGHTEN_HOVERABLE_25,
                )
            )
            .addDarkModeBackground(None)
            .build(itemSize=self.icons.SIZES.MEDIUM.height())
        )
        self.buttonIcons: dict[str, QIcon] = {
            "lightModeEditBtn": AppUtils.paintIcon(self.icons.EDIT, Colors.white),
            "lightModeDeleteBtn": AppUtils.paintIcon(self.icons.DELETE, Colors.white),
            "darkModeEditBtn": None,
            "darkModeDeleteBtn": None,
        }
        self.hoverAnimation = Animation(1.0, 1.1, 250)

        # =================UI=================
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.inner = QWidget()
        self.setWidget(self.inner)

        self.main_layout = QHBoxLayout(self.inner)
        self.main_layout.setAlignment(Qt.AlignLeft)
        self.main_layout.setSpacing(32)

        # =================Library=================
        self.defaultPlaylistCover = self.__getPixmapForPlaylistCover(ApplicationImage.defaultPlaylistCover)

        self.library = PlaylistCard(self.playlistLabelFont)
        self.library.setAnimation(self.hoverAnimation)
        self.library.setFixedSize(256, 320)
        self.library.setCursor(self.cursors.HAND)
        self.library.setCover(self.defaultPlaylistCover)
        self.library.setLabelText("Library")

        self.favourites = PlaylistCard(self.playlistLabelFont)
        self.favourites.setAnimation(self.hoverAnimation)
        self.favourites.setFixedSize(256, 320)
        self.favourites.setCursor(self.cursors.HAND)
        self.favourites.setCover(self.__getPixmapForPlaylistCover(ApplicationImage.favouritesCover))
        self.favourites.setLabelText("Favourites")

        self.main_layout.addWidget(self.library)
        self.main_layout.addWidget(self.favourites)

        # =================New playlist=================
        self.add_playlist_card = QWidget()
        self.add_playlist_card.setFixedSize(256, 320)
        self.add_playlist_card.setObjectName("add_playlist_card")
        self.__addThemeForItem(
            self.add_playlist_card,
            theme=ThemeData(
                lightMode="#add_playlist_card{background:rgba(0,0,0,0.1);border-radius:24px}",
                darkMode="#add_playlist_card{background:rgba(255,255,255,0.25);border-radius:24px}",
            ),
        )
        self.add_playlist_btn = IconButton.render(
            padding=Paddings.RELATIVE_67,
            size=self.icons.SIZES.LARGE,
            lightModeIcon=AppUtils.paintIcon(self.icons.ADD, Colors.PRIMARY),
            darkModeIcon=AppUtils.paintIcon(self.icons.ADD, Colors.white),
            parent=self.add_playlist_card,
        )
        self.add_playlist_btn.setCursor(self.cursors.HAND)
        self.add_playlist_btn.move(self.add_playlist_card.rect().center() - self.add_playlist_btn.rect().center())
        self.__addButtonToList(self.add_playlist_btn)
        self.__addThemeForItem(
            self.add_playlist_btn,
            theme=(
                IconButton.getThemeBuilder()
                .addLightModeBackground(
                    Background(
                        borderRadius=0.5,
                        color=ColorBoxes.HIDDEN_PRIMARY,
                    )
                )
                .addDarkModeBackground(
                    Background(
                        borderRadius=0.5,
                        color=ColorBoxes.HIDDEN_WHITE,
                    )
                )
                .build(itemSize=self.icons.SIZES.LARGE.height())
            ),
        )
        self.main_layout.addWidget(self.add_playlist_card)

    def connectSignalsToController(self, controller):
        self.add_playlist_btn.clicked.connect(controller.handleAddNewPlaylist)
        self.library.clicked.connect(controller.handleSelectedLibrary)
        self.favourites.clicked.connect(controller.handleSelectedFavourites)

    def lightMode(self) -> None:
        self.isDarkMode = False
        for button in self.buttonsWithDarkMode:
            button.setDarkMode(False)
        for item in self.themeItems:
            lightModeStyleSheet = self.themeItems.get(item).lightMode
            if lightModeStyleSheet is None or lightModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(lightModeStyleSheet)

    def darkMode(self) -> None:
        self.isDarkMode = True
        for button in self.buttonsWithDarkMode:
            button.setDarkMode(True)
        for item in self.themeItems:
            darkModeStyleSheet = self.themeItems.get(item).darkMode
            if darkModeStyleSheet is None or darkModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(darkModeStyleSheet)

    def openChoosingPlaylistCoverDialog(self, index: int, controller) -> None:
        path = QFileDialog.getOpenFileName(self, filter="JPEG, PNG (*.JPEG *.jpeg *.JPG *.jpg *.JPE *.jpe)")[0]
        controller.handleChangedPlaylistCover(index, path)

    def addNewPlaylistAtIndex(self, index: int, controller):
        playlist = EditablePlaylistCard(
            labelFont=self.playlistLabelFont,
            buttonTheme=self.buttonTheme,
            icons=self.buttonIcons,
            iconSize=self.icons.SIZES.MEDIUM,
        )
        playlist.setAnimation(self.hoverAnimation)
        playlist.setFixedSize(256, 320)
        playlist.setDefaultCover(self.defaultPlaylistCover)
        playlist.setDefaultText("Unknown")
        playlist.setCursor(AppCursors.hand())

        playlistIndex = self.__getInsertPositionToLayoutForPlaylistWithIndex(index)
        AppUtils.setAttribute(self, "playlist_card", playlistIndex, playlist)
        self.main_layout.insertWidget(index, playlist)

        playlist.clicked.connect(lambda: controller.handleSelectedPlaylist(playlistIndex))
        playlist.label.returnPressed.connect(
            lambda: controller.handleChangedPlaylistName(playlistIndex, playlist.label.text())
        )
        playlist.deleteBtn.clicked.connect(lambda: controller.handleDeletePlaylistAtIndex(playlistIndex))
        playlist.editBtn.clicked.connect(lambda: self.openChoosingPlaylistCoverDialog(playlistIndex, controller))

    def addNewEmptyPlaylist(self, controller):
        appendPosition = self.main_layout.count() - 1
        self.addNewPlaylistAtIndex(appendPosition, controller)
        return self.getTotalPlaylistInLayout() - 1

    def showPlaylistAtIndex(self, index: int) -> None:
        self.getPlaylistByIndex(index).show()

    def hidePlaylistAtIndex(self, index: int) -> None:
        self.getPlaylistByIndex(index).hide()

    def displayPlaylistInfoAtIndex(self, index: int, name: str, cover: bytes) -> None:
        self.changePlaylistNameAtIndex(index, name)
        self.changePlaylistCoverAtIndex(index, cover)

    def getPlaylistByIndex(self, index: int) -> EditablePlaylistCard:
        return AppUtils.getAttribute(self, "playlist_card", index)

    def changePlaylistCoverAtIndex(self, index: int, cover: bytes) -> None:
        self.getPlaylistByIndex(index).setCover(self.__getPixmapForPlaylistCover(cover))

    def changePlaylistNameAtIndex(self, index: int, name: str) -> None:
        self.getPlaylistByIndex(index).setText(name)

    def removePlaylistInfoAtIndex(self, index: int) -> None:
        self.displayPlaylistInfoAtIndex(index, name=None, cover=None)

    def displayPlaylistInRange(self, start: int, end: int) -> None:
        for index in range(start, end):
            self.getPlaylistByIndex(index).show()
        for index in range(end, self.getTotalPlaylistInLayout()):
            self.getPlaylistByIndex(index).hide()
        AppUtils.getAttribute(self, "playlist_card", end).setParent(None)

    def getTotalPlaylistInLayout(self) -> int:
        return self.main_layout.count() - 3

    def getNumberOfPlaylistDisplaying(self) -> int:
        count: int = 0
        while True:
            playlist = self.getPlaylistByIndex(count)
            if playlist is None:
                return count
            if not playlist.isVisible():
                return count
            playlistIsEmpty = playlist.label.isDisplayingDefaultText()
            if playlistIsEmpty:
                return count
            count += 1

    def addPlaylists(self, numberOfPlaylist: int) -> None:
        for index in range(0, numberOfPlaylist + 1):
            self.addNewEmptyPlaylist(controller=self)

    def hidePlaylistInRange(self, start: int, end: int):
        for index in range(start, end):
            self.hidePlaylistAtIndex(index)
            self.removePlaylistInfoAtIndex(index)

    def __getInsertPositionToLayoutForPlaylistWithIndex(self, index) -> int:
        countOfItemsBeforePlaylist = 2
        return index - countOfItemsBeforePlaylist

    def __addThemeForItem(self, item, theme: ThemeData) -> None:
        self.themeItems[item] = theme

    def __addButtonToList(self, item) -> None:
        self.buttonsWithDarkMode.append(item)

    def __getPixmapForPlaylistCover(self, coverAsByte: bytes) -> QPixmap:
        if coverAsByte is None:
            return None
        return AppUtils.getEditedPixmapFromBytes(coverAsByte, width=256, height=320, radius=24)
