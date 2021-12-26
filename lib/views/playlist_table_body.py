from functools import cached_property

from constants.ui.base import ApplicationImage
from constants.ui.qss import ColorBoxes, Colors
from constants.ui.qt import AppCursors, AppIcons
from modules.screens.components.confirm_message import ConfirmMessage
from modules.screens.components.font_builder import FontBuilder
from modules.screens.components.icon_buttons import IconButton
from modules.screens.components.labels import StandardLabel
from modules.screens.components.song_item import SongItem
from modules.screens.qss.qss_elements import Background
from modules.screens.themes.theme_builders import ThemeData
from PyQt5.QtCore import QEvent, Qt, pyqtSignal
from PyQt5.QtGui import QKeyEvent, QPixmap
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QWidget
from utils.ui.application_utils import UiUtils
from widgets.image_displayer import ImageDisplayer
from widgets.smooth_scroll_area import SmoothVerticalScrollArea


class PlaylistTableBody(SmoothVerticalScrollArea):
    keyPressed = pyqtSignal(QEvent)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.themeItems = {}
        self.buttonsWithDarkMode = []
        self.isDarkMode = False
        self.setupUi()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.keyPressed.emit(event)
        return super().keyPressEvent(event)

    def setupUi(self):
        self.icons = AppIcons()
        self.setStyleSheet(
            "QScrollBar:vertical {border:none;background:TRANSPARENT;width:4px}\n"
            "QScrollBar::handle:vertical {background:rgba(160,160,160, 0.5);border-radius:2px}\n"
            "QScrollBar::handle:vertical:hover{background:#8040ff}\n"
            "QScrollBar::sub-line:vertical{border: none}\n"
            "QScrollBar::add-line:vertical{border: none}\n"
            "QScrollBar::up-arrow:vertical,QScrollBar::down-arrow:vertical{background: none}\n"
            "QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{background: none}"
        )
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.inner = QWidget(self)
        self.setWidget(self.inner)

        self.menu = QVBoxLayout(self.inner)
        self.menu.setAlignment(Qt.AlignTop)
        self.menu.setSpacing(0)
        self.menu.setContentsMargins(8, 8, 8, 8)
        self.setItemHeight(104)

    def getKeyFromEvent(self, event: QKeyEvent, controller=None) -> None:
        isHoldingALT = int(event.modifiers()) == Qt.AltModifier
        if not isHoldingALT:
            return
        try:
            index = controller.playlist.findSongInsertPosition(chr(event.key()))
            self.scrollToItem(index)
        except ValueError:
            pass

    def connectSignalsToController(self, controller):
        self.keyPressed.connect(lambda event: self.getKeyFromEvent(event, controller))

    def lightMode(self) -> None:
        self.isDarkMode = False
        songCount = self.getTotalSongAvailable()
        for index in range(0, songCount):
            self.__getSongByIndex(index).lightMode()
        for button in self.buttonsWithDarkMode:
            button.setDarkMode(False)
        for item in self.themeItems:
            lightModeStyleSheet = self.themeItems.get(item).lightMode
            if lightModeStyleSheet is None or lightModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(lightModeStyleSheet)

    def darkMode(self) -> None:
        self.isDarkMode = True
        songCount = self.getTotalSongAvailable()
        for index in range(0, songCount):
            self.__getSongByIndex(index).darkMode()
        for button in self.buttonsWithDarkMode:
            button.setDarkMode(True)
        for item in self.themeItems:
            darkModeStyleSheet = self.themeItems.get(item).darkMode
            if darkModeStyleSheet is None or darkModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(darkModeStyleSheet)

    def updateLayout(self, totalPlaylistAvailable: int, controller) -> None:
        totalPlaylistDisplaying = self.getTotalSongAvailable()

        if totalPlaylistAvailable == 0:
            self.__showPlaylistEmptyNotification()
            self.__removePlaylistsInRange(totalPlaylistAvailable, totalPlaylistDisplaying)
            return

        totalPlaylistLacking = totalPlaylistAvailable - totalPlaylistDisplaying
        if totalPlaylistLacking == 0:
            return

        isDisplayingMoreThanNumberOfPlaylists = totalPlaylistLacking < 0
        if isDisplayingMoreThanNumberOfPlaylists:
            self.__removePlaylistsInRange(totalPlaylistAvailable, totalPlaylistDisplaying)
            return

        isDisplayingLessThanNumberOfPlaylists = totalPlaylistLacking > 0
        if isDisplayingLessThanNumberOfPlaylists:
            self.__addLackingPlaylists(totalPlaylistLacking, controller)

    def __showPlaylistEmptyNotification(self):
        self.emptyNotification = ImageDisplayer(self.inner)
        edge: int = 256
        self.emptyNotification.setFixedSize(edge, edge)
        self.emptyNotification.setPixmap(
            UiUtils.getEditedPixmapFromBytes(ApplicationImage.errorPlaylist, width=edge, height=edge)
        )

    def displaySongInfoAtIndex(self, index: int, cover: bytes, title: str, artist: str, length: float) -> None:
        song = self.__getSongByIndex(index)
        song.show()
        song.showLess()
        song.setCover(self.__getPixmapForSongCover(cover))
        song.setTitle(title)
        song.setArtist(artist)
        song.setLength(length)

    def setSongCoverAtIndex(self, index: int, cover: bytes) -> None:
        self.__getSongByIndex(index).setCover(self.__getPixmapForSongCover(cover))

    def setSongTitleAtIndex(self, index: int, title: str) -> None:
        self.__getSongByIndex(index).setTitle(title)

    def setSongArtistAtIndex(self, index: int, artist: str) -> None:
        self.__getSongByIndex(index).setArtist(artist)

    def setSongLengthAtIndex(self, index: int, length: float) -> None:
        self.__getSongByIndex(index).setLength(length)

    def setSongLoveStateAtIndex(self, index: int, state: bool) -> None:
        self.__getSongByIndex(index).setLoveState(state)

    def getTotalSongAvailable(self) -> int:
        return self.menu.count()

    def __addLackingPlaylists(self, numberOfPlaylist: int, controller) -> None:
        defaultValues: dict = {
            "cover": self.__getPixmapForSongCover(ApplicationImage.defaultSongCover),
            "title": "title",
            "artist": "",
            "length": 0,
            "theme": ThemeData(
                lightMode="QWidget{background-color:rgba(0, 0, 0, 0.1);border-radius:16px}QWidget:hover{background-color:rgba(0, 0, 0, 0.15)}",
                darkMode="QWidget{background-color:rgba(255, 255, 255, 0.1);border-radius:16px}QWidget:hover{background-color:rgba(255, 255, 255, 0.15)}",
            ),
            "labels": {
                "font": FontBuilder().withSize(10).withWeight("normal").build(),
                "themes": {
                    "PRIMARY": (
                        StandardLabel.getThemeBuilder()
                        .addLightModeTextColor(ColorBoxes.BLACK)
                        .addDarkModeTextColor(ColorBoxes.WHITE)
                        .build(itemSize=self.icons.SIZES.LARGE.height())
                    ),
                    "secondary": (
                        StandardLabel.getThemeBuilder()
                        .addLightModeTextColor(ColorBoxes.GRAY)
                        .addDarkModeTextColor(ColorBoxes.GRAY)
                        .build(itemSize=self.icons.SIZES.LARGE.height())
                    ),
                },
            },
            "buttons": {
                "cursors": AppCursors(),
                "themes": {
                    "PRIMARY": (
                        IconButton.getThemeBuilder()
                        .addLightModeBackground(
                            Background(
                                borderRadius=0.5,
                                color=ColorBoxes.HOVERABLE_HIDDEN_PRIMARY,
                            )
                        )
                        .addDarkModeBackground(
                            Background(
                                borderRadius=0.5,
                                color=ColorBoxes.HOVERABLE_HIDDEN_WHITE,
                            )
                        )
                        .build(itemSize=self.icons.SIZES.LARGE.height())
                    ),
                    "secondary": (
                        IconButton.getThemeBuilder()
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
                        .build(itemSize=self.icons.SIZES.LARGE.height())
                    ),
                    "DANGER": (
                        IconButton.getThemeBuilder()
                        .addLightModeBackground(
                            Background(
                                borderRadius=0.5,
                                color=ColorBoxes.HOVERABLE_DANGER,
                            )
                        )
                        .addDarkModeBackground(None)
                        .build(itemSize=self.icons.SIZES.MEDIUM.height())
                    ),
                },
            },
        }
        for index in range(0, numberOfPlaylist):
            self.__addNewEmptyPlaylist(defaultValues, controller)

    def __addNewEmptyPlaylist(self, defaultValues: dict, controller) -> None:
        index = self.getTotalSongAvailable()
        song = self.__addSong(index, defaultValues)

        song.title.returnPressed.connect(lambda: controller.handleChangedSongTitle(index, song.title.text()))
        song.artist.returnPressed.connect(lambda: controller.handleChangedSongArtist(index, song.artist.text()))
        song.coverObserver.doubleClicked.connect(lambda: self.__openChoosingCoverDialog(index, controller))
        song.loveBtn.clicked.connect(
            lambda: controller.handleChangedLoveStateOfSongAtIndex(index, song.loveBtn.isChecked())
        )
        song.playBtn.clicked.connect(lambda: self.scrollToItem(index))
        song.playBtn.clicked.connect(lambda: controller.handlePlayedSongAtIndex(index))
        song.addToPlaylistBtn.clicked.connect(lambda: controller.handleAddSongToPlaylistAtIndex(index))
        song.editBtn.clicked.connect(lambda: controller.handleEditSongAtIndex(index))
        song.deleteBtn.clicked.connect(lambda: self.__confirmDeleteSongAtIndex(index, controller))

    def __removePlaylistsInRange(self, start: int, end: int):
        for index in range(start, end):
            self.menu.itemAt(index).widget().deleteLater()

    def __addSong(self, index: int, values: dict):
        song = SongItem(
            theme=values.get("theme"),
            font=values.get("labels").get("font"),
            labelThemes=values.get("labels").get("themes"),
            buttonThemes=values.get("buttons").get("themes"),
        )
        song.setDefaultCover(values.get("cover"))
        song.setDefaultTitle(values.get("title"))
        song.setDefaultArtist(values.get("artist"))
        song.setDefaultLength(values.get("length"))
        self.menu.addWidget(song)
        UiUtils.setAttribute(self, "song", index, song)
        return song

    def __confirmDeleteSongAtIndex(self, index: int, controller) -> None:
        message_box = ConfirmMessage(
            header="Delete song", msg="Are you sure want to delete the song? This action can not be reversed."
        )
        confirmDelete = message_box.exec()
        if not confirmDelete:
            return
        controller.handleDeleteSongAtIndex(index)

    def __openChoosingCoverDialog(self, index: int, controller) -> None:
        path = QFileDialog.getOpenFileName(self, filter="JPEG, PNG (*.JPEG *.jpeg *.JPG *.jpg *.JPE *.jpe)")[0]
        controller.handleChangedSongCover(index, path)

    def __getSongByIndex(self, index: int) -> SongItem:
        return UiUtils.getAttribute(self, "song", index)

    # @cached_property
    def __getPixmapForSongCover(self, coverAsByte: bytes) -> QPixmap:
        if coverAsByte is None:
            return None
        return UiUtils.getEditedPixmapFromBytes(coverAsByte, width=64, height=64, radius=12)
