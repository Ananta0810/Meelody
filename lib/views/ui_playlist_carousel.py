from sys import path

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

path.append("./lib")
from constants.ui.base import ApplicationImage
from constants.ui.qss import ColorBoxes, Colors, Paddings
from constants.ui.qt import AppCursors, AppIcons
from modules.entities.playlist_info import PlaylistInfo
from modules.screens.components.factories import IconButtonFactory, LabelFactory
from modules.screens.components.font_builder import FontBuilder
from modules.screens.qss.qss_elements import Background
from modules.screens.themes.theme_builders import ThemeData
from utils.ui.application_utils import ApplicationUIUtils as AppUI
from widgets.hoverable_widget import HoverableWidget
from widgets.image_displayer import ImageDisplayer


class UiPlaylistCarousel(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.themeItems = {}
        self.buttonsWithDarkMode = []
        self.icons = AppIcons()
        self.cursors = AppCursors()
        self.isDarkMode = False

        self.iconButtonFormer = IconButtonFactory().getByType("default")
        labelFactory = LabelFactory()
        self.labelFormer = labelFactory.getByType("default")
        self.doubleClickedEditableLabel = labelFactory.getByType("doubleClickedEditable")
        self.emphasizedFont = FontBuilder().withSize(16).withWeight("bold").build()
        # =================UI=================
        self.setMinimumSize(QSize(1368, 608))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.inner = QWidget()
        self.inner.setGeometry(QRect(0, 0, 1359, 340))
        self.inner.setStyleSheet("border:none")
        self.setWidget(self.inner)

        self.main_layout = QHBoxLayout(self.inner)
        self.main_layout.setAlignment(Qt.AlignLeft)
        self.main_layout.setSpacing(32)

        # =================Library=================
        self.library_card = HoverableWidget()
        self.library_card.setFixedWidth(256)
        self.library_cover = ImageDisplayer(self.library_card)
        self.library_cover.setGeometry(QRect(0, 0, 256, 320))
        self.library_cover.setCursor(self.cursors.HAND)
        self.library_label = labelFactory.getByType("default").render(
            font=self.emphasizedFont, parent=self.library_card
        )
        self.defaultPlaylistCover = self.__getPixmapForPlaylistCover(ApplicationImage.defaultPlaylistCover)
        self.library_cover.setPixmap(self.defaultPlaylistCover)
        self.library_label.setFixedSize(160, 32)
        self.library_label.setText("Library")

        self.LABEL_LEFT_POSTION = 24
        self.LABEL_TOP_POSTION = self.__getPaddingPositionBotton(
            padding=16,
            parentHeight=self.library_cover.height(),
            itemHeight=self.library_label.height(),
        )
        self.library_label.move(self.LABEL_LEFT_POSTION, self.LABEL_TOP_POSTION)
        self.main_layout.addWidget(self.library_card)

        # =================Favourites=================
        self.favourite_card = HoverableWidget()
        self.favourite_card.setFixedWidth(256)
        self.favourite_cover = ImageDisplayer(self.favourite_card)
        self.favourite_cover.setGeometry(QRect(0, 0, 256, 320))
        self.favourite_cover.setCursor(self.cursors.HAND)
        self.favourite_label = self.labelFormer.render(font=self.emphasizedFont, parent=self.favourite_card)
        self.favourite_cover.setPixmap(self.__getPixmapForPlaylistCover(ApplicationImage.favouritesCover))
        self.favourite_label.setFixedSize(160, 32)
        self.favourite_label.setText("Favourite")
        self.favourite_label.move(self.LABEL_LEFT_POSTION, self.LABEL_TOP_POSTION)

        self.main_layout.addWidget(self.favourite_card)

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
        self.add_playlist_btn = self.iconButtonFormer.render(
            padding=Paddings.RELATIVE_67,
            size=self.icons.SIZES.LARGE,
            lightModeIcon=AppUI.paintIcon(self.icons.ADD, Colors.PRIMARY),
            darkModeIcon=AppUI.paintIcon(self.icons.ADD, Colors.WHITE),
            parent=self.add_playlist_card,
        )
        self.add_playlist_btn.setCursor(self.cursors.HAND)
        self.add_playlist_btn.move(self.add_playlist_card.rect().center() - self.add_playlist_btn.rect().center())
        self.__addButtonToList(self.add_playlist_btn)
        self.__addThemeForItem(
            self.add_playlist_btn,
            theme=(
                self.iconButtonFormer.getThemeBuilder()
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
        self.library_cover.clicked.connect(controller.handleSelectedLibrary)
        self.favourite_cover.clicked.connect(controller.handleSelectedFavourites)

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

    def __addThemeForItem(self, item, theme: ThemeData) -> None:
        self.themeItems[item] = theme

    def __addButtonToList(self, item) -> None:
        self.buttonsWithDarkMode.append(item)

    def __getPaddingPositionBotton(self, padding, parentHeight, itemHeight):
        return parentHeight - itemHeight - padding

    def __getPixmapForPlaylistCover(self, coverAsByte: bytes) -> QPixmap:
        if coverAsByte is None:
            return None
        pixmap = AppUI.getEditedPixmapFromBytes(
            coverAsByte,
            width=self.library_cover.width(),
            height=self.library_cover.height(),
            cropCenter=False,
            radius=24,
        )
        return pixmap

    def __applyThemeForItem(self, item):
        styleSheet = self.themeItems.get(item).darkMode if self.isDarkMode else self.themeItems.get(item).lightMode
        if styleSheet is None or styleSheet.strip() == "":
            return
        item.setStyleSheet(styleSheet)

    def addNewEmptyPlaylist(self, controller):
        appendPosition = self.main_layout.count() - 1
        self.addNewPlaylistAtIndex(appendPosition, controller)
        return self.getTotalPlaylistInLayout() - 1

    def showPlaylistAtIndex(self, index: int) -> None:
        self.getPlaylistFromLayoutAtIndex(index).show()

    def hidePlaylistAtIndex(self, index: int) -> None:
        self.getPlaylistFromLayoutAtIndex(index).hide()

    def displayPlaylistInfoAtIndex(self, index: int, name: str, cover: bytes):
        self.getAttribute("playlist_label", index).setText(name)
        self.getAttribute("playlist_cover", index).setPixmap(self.__getPixmapForPlaylistCover(cover))

    def addNewPlaylistAtIndex(self, index, controller):
        playlistIndex = self.getPlaylistIndexUsingPositionInLayout(index)
        self.setAttribute("playlist_card", playlistIndex, HoverableWidget())
        playlist_card = self.getAttribute("playlist_card", playlistIndex)
        playlist_card.setFixedWidth(256)
        self.setAttribute("playlist_card", playlistIndex, HoverableWidget())

        self.setAttribute("playlist_cover", playlistIndex, ImageDisplayer(playlist_card))
        playlist_cover = self.getAttribute("playlist_cover", playlistIndex)
        playlist_cover.setGeometry(QRect(0, 0, 256, 320))
        playlist_cover.setCursor(self.cursors.HAND)

        self.setAttribute(
            "playlist_label",
            playlistIndex,
            self.doubleClickedEditableLabel.render(font=self.emphasizedFont, parent=playlist_card),
        )
        playlist_label = self.getAttribute("playlist_label", playlistIndex)
        playlist_cover.setDefaultPixmap(self.defaultPlaylistCover)
        playlist_cover.setPixmap(None)
        playlist_label.setFixedSize(160, 32)
        playlist_label.setText("Unknown")
        playlist_label.move(self.LABEL_LEFT_POSTION, self.LABEL_TOP_POSTION)

        playlist_delelte_btn = self.iconButtonFormer.render(
            padding=Paddings.RELATIVE_50,
            size=self.icons.SIZES.MEDIUM,
            lightModeIcon=AppUI.paintIcon(self.icons.DELETE, Colors.PRIMARY),
            darkModeIcon=AppUI.paintIcon(self.icons.DELETE, Colors.WHITE),
            parent=playlist_card,
        )
        playlist_delelte_btn.setCursor(self.cursors.HAND)
        playlist_delelte_btn.move(210, 10)
        self.__addButtonToList(playlist_delelte_btn)
        self.__addThemeForItem(
            playlist_delelte_btn,
            theme=(
                self.iconButtonFormer.getThemeBuilder()
                .addLightModeBackground(
                    Background(
                        borderRadius=0.5,
                        color=ColorBoxes.PRIMARY_LIGHTEN_HOVERABLE_25,
                    )
                )
                .addDarkModeBackground(
                    Background(
                        borderRadius=0.5,
                        color=ColorBoxes.PRIMARY_LIGHTEN_HOVERABLE_25,
                    )
                )
                .build(itemSize=self.icons.SIZES.MEDIUM.height())
            ),
        )
        self.__applyThemeForItem(playlist_delelte_btn)

        self.main_layout.insertWidget(index, playlist_card)
        playlist_cover.clicked.connect(lambda: controller.handleSelectedPlaylist(playlistIndex))
        playlist_label.returnPressed.connect(
            lambda: controller.handleChangedPlaylistName(playlistIndex, playlist_label)
        )
        playlist_delelte_btn.clicked.connect(lambda: controller.handleDeletePlaylistAtIndex(playlistIndex))

    def getPlaylistByIndex(self, index: int):
        NUMBER_OF_DEFAULT_PLAYLIST_BEFORE_THIS_PLAYLIST_IN_LAYOUT = 2
        playlistPosition = index + NUMBER_OF_DEFAULT_PLAYLIST_BEFORE_THIS_PLAYLIST_IN_LAYOUT
        return self.main_layout.itemAt(playlistPosition)

    def displayPlaylistInRange(self, start: int, end: int):
        for index in range(start, end):
            self.getPlaylistFromLayoutAtIndex(index).show()
        for index in range(end, self.getTotalPlaylistInLayout()):
            self.getPlaylistFromLayoutAtIndex(index).hide()
        self.getAttribute("playlist_card", end).setParent(None)

    def getTotalPlaylistInLayout(self) -> int:
        return self.main_layout.count() - 3

    def getTotalPlaylistDisplayingInLayout(self) -> int:
        count: int = 0
        while True:
            playlist = self.getAttribute("playlist_card", count)
            if playlist is None:
                return count
            if not playlist.isVisible():
                return count
            count += 1

    def getPlaylistIndexUsingPositionInLayout(self, index) -> int:
        countOfItemsBeforeTheDisiredPlaylist = 2
        return index - countOfItemsBeforeTheDisiredPlaylist

    def getPlaylistPositionInLayout(self, index: int) -> int:
        countOfItemsBeforeTheDisiredPlaylist = 2
        return index + countOfItemsBeforeTheDisiredPlaylist

    def getPlaylistFromLayoutAtIndex(self, index: int):
        return self.main_layout.itemAt(self.getPlaylistPositionInLayout(index)).widget()

    def removePlaylistAtIndex(self, index: int) -> None:
        self.displayPlaylistInRange(0, index)
        # self.getPlaylistFromLayoutAtIndex(index).setParent(None)

    def setAttribute(self, object: str, index: int, value) -> None:
        setattr(self, "_".join([object, str(index)]), value)

    def getAttribute(self, object: str, index: int):
        return getattr(self, "_".join([object, str(index)]))
