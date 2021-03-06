from constants.ui.base import ApplicationImage
from constants.ui.qss import Backgrounds, Colors, Paddings
from constants.ui.qt import AppCursors, AppIcons
from constants.ui.theme_builders import IconButtonThemeBuilders
from modules.screens.components.font_builder import FontBuilder
from modules.screens.components.icon_buttons import IconButton
from modules.screens.others.animation import Animation
from modules.screens.themes.theme_builders import ButtonThemeBuilder, ThemeData
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QScrollArea, QWidget
from utils.ui.application_utils import UiUtils
from views.dialogs.confirm_dialog import ConfirmDialog
from views.view import View

from .custom_playlist_card import CustomPlaylistCard
from .default_playlist_card import DefaultPlaylistCard


class UIPlaylistCarousel(QScrollArea, View):
    def __init__(self, parent=None):
        super(UIPlaylistCarousel, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        icons = AppIcons()
        self.cursors = AppCursors()

        self.playlistLabelFont = FontBuilder().withSize(16).withWeight("bold").build()
        self.buttonTheme = (
            ButtonThemeBuilder()
            .addLightModeBackground(Backgrounds.CIRCLE_PRIMARY_25)
            .addDarkModeBackground(None)
            .build(itemSize=icons.SIZES.MEDIUM.height())
        )
        self.buttonIcons: dict[str, QIcon] = {
            "lightModeEditBtn": UiUtils.paintIcon(icons.EDIT, Colors.WHITE),
            "lightModeDeleteBtn": UiUtils.paintIcon(icons.DELETE, Colors.WHITE),
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

        self.mainLayout = QHBoxLayout(self.inner)
        self.mainLayout.setAlignment(Qt.AlignLeft)
        self.mainLayout.setSpacing(32)

        # =================Library=================
        self.defaultPlaylistCover = self.__getPixmapForPlaylistCover(ApplicationImage.defaultPlaylistCover)

        self.library = DefaultPlaylistCard(self.playlistLabelFont)
        self.library.setAnimation(self.hoverAnimation)
        self.library.setFixedSize(256, 320)
        self.library.setCursor(self.cursors.HAND)
        self.library.setCover(self.defaultPlaylistCover)
        self.library.setLabelText("Library")

        self.favourites = DefaultPlaylistCard(self.playlistLabelFont)
        self.favourites.setAnimation(self.hoverAnimation)
        self.favourites.setFixedSize(256, 320)
        self.favourites.setCursor(self.cursors.HAND)
        self.favourites.setCover(self.__getPixmapForPlaylistCover(ApplicationImage.favouritesCover))
        self.favourites.setLabelText("Favourites")

        self.defautl_playlists = QHBoxLayout()
        self.defautl_playlists.setAlignment(Qt.AlignLeft)
        self.defautl_playlists.addWidget(self.library)
        self.defautl_playlists.addWidget(self.favourites)

        self.user_playlists = QHBoxLayout()
        self.user_playlists.setAlignment(Qt.AlignLeft)

        self.mainLayout.addLayout(self.defautl_playlists)
        self.mainLayout.addLayout(self.user_playlists)

        # =================New playlist=================
        self.addPlaylistCard = QWidget()
        self.addPlaylistCard.setFixedSize(256, 320)
        self._addThemeForItem(
            self.addPlaylistCard,
            theme=ThemeData(
                lightMode="QWidget{background:rgba(0,0,0,0.1);border-radius:24px}",
                darkMode="QWidget{background:rgba(255,255,255,0.25);border-radius:24px}",
            ),
        )
        self.add_playlist_btn = IconButton.render(
            padding=Paddings.RELATIVE_67,
            size=icons.SIZES.LARGE,
            lightModeIcon=UiUtils.paintIcon(icons.ADD, Colors.PRIMARY),
            darkModeIcon=UiUtils.paintIcon(icons.ADD, Colors.WHITE),
            parent=self.addPlaylistCard,
        )
        self.add_playlist_btn.setCursor(self.cursors.HAND)
        self.add_playlist_btn.move(self.addPlaylistCard.rect().center() - self.add_playlist_btn.rect().center())
        self._addButtonToList(self.add_playlist_btn)
        self._addThemeForItem(
            self.add_playlist_btn,
            theme=IconButtonThemeBuilders.CIRCLE_HIDDEN_PRIMARY_25.build(itemSize=icons.SIZES.LARGE.height()),
        )
        self.mainLayout.addWidget(self.addPlaylistCard)
        self.mainLayout.addStretch()

    def connectToController(self, controller):
        self.add_playlist_btn.clicked.connect(controller.handleAddNewPlaylist)
        self.library.clicked.connect(controller.handleSelectedLibrary)
        self.favourites.clicked.connect(controller.handleSelectedFavourites)

    def updateLayout(self, totalPlaylistAvailable: int, controller) -> None:
        totalPlaylistDisplaying = self.__getTotalPlaylistInLayout()
        totalPlaylistLacking = totalPlaylistAvailable - totalPlaylistDisplaying
        if totalPlaylistLacking == 0:
            return

        isDisplayingMoreThanNumberOfPlaylists = totalPlaylistLacking < 0
        if isDisplayingMoreThanNumberOfPlaylists:
            self.removePlaylistsInRange(totalPlaylistAvailable, totalPlaylistDisplaying)
            return

        isDisplayingLessThanNumberOfPlaylists = totalPlaylistLacking > 0
        if isDisplayingLessThanNumberOfPlaylists:
            self.addLackingPlaylists(totalPlaylistLacking, controller)

    def addLackingPlaylists(self, numberOfPlaylist: int, controller) -> None:
        for index in range(0, numberOfPlaylist):
            self.addNewEmptyPlaylist(controller)

    def addNewEmptyPlaylist(self, controller) -> None:
        index = self.__getTotalPlaylistInLayout()
        playlist = self.__addPlaylist(index)
        playlist.clicked.connect(lambda: controller.handleSelectedPlaylist(index))
        playlist.label.returnPressed.connect(lambda: controller.handleChangedPlaylistName(index, playlist.label.text()))
        playlist.deleteBtn.clicked.connect(lambda: self.__confirmDeletePlaylist(index, controller))
        playlist.editBtn.clicked.connect(lambda: self.__openChoosingPlaylistCoverDialog(index, controller))

    def removePlaylistsInRange(self, start: int, end: int):
        for index in range(start, end):
            self.user_playlists.itemAt(index).widget().deleteLater()

    def displayPlaylistInfoAtIndex(self, index: int, name: str, cover: bytes) -> None:
        self.getPlaylistByIndex(index).show()
        self.changePlaylistNameAtIndex(index, name)
        self.changePlaylistCoverAtIndex(index, cover)

    def getPlaylistByIndex(self, index: int) -> CustomPlaylistCard:
        return UiUtils.getAttribute(self, "playlistCard", index)

    def changePlaylistCoverAtIndex(self, index: int, cover: bytes) -> None:
        self.getPlaylistByIndex(index).setCover(self.__getPixmapForPlaylistCover(cover))

    def changePlaylistNameAtIndex(self, index: int, name: str) -> None:
        self.getPlaylistByIndex(index).setText(name)

    def __addPlaylist(self, index: int):
        playlist = CustomPlaylistCard(
            labelFont=self.playlistLabelFont,
            buttonTheme=self.buttonTheme,
            icons=self.buttonIcons,
            iconSize=AppIcons().SIZES.MEDIUM,
        )
        playlist.setAnimation(self.hoverAnimation)
        playlist.setFixedSize(256, 320)
        playlist.setDefaultCover(self.defaultPlaylistCover)
        playlist.setDefaultText("Unknown")
        playlist.setCursor(AppCursors.hand())

        self.user_playlists.addWidget(playlist)
        UiUtils.setAttribute(self, "playlistCard", index, playlist)
        return playlist

    def __confirmDeletePlaylist(self, index: int, controller) -> None:
        message_box = ConfirmDialog(
            header="Delete playlist", msg="Are you sure want to delete the playlist? This action can not be reversed."
        )
        confirmDelete = message_box.exec()
        if not confirmDelete:
            return
        controller.handleDeletePlaylistAtIndex(index)

    def __openChoosingPlaylistCoverDialog(self, index: int, controller) -> None:
        path = QFileDialog.getOpenFileName(self, filter="JPEG, PNG (*.JPEG *.jpeg *.JPG *.jpg *.JPE *.jpe)")[0]
        controller.handleChangedPlaylistCover(index, path)

    def __getTotalPlaylistInLayout(self) -> int:
        return self.user_playlists.count()

    def __getPixmapForPlaylistCover(self, coverAsByte: bytes) -> QPixmap:
        if coverAsByte is None:
            return None
        return UiUtils.getEditedPixmapFromBytes(coverAsByte, width=256, height=320, radius=24)
