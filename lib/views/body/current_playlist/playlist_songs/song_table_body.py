from typing import Optional

from constants.ui.base import ApplicationImage
from constants.ui.qss import Backgrounds, ColorBoxes
from constants.ui.qt import IconSizes
from modules.screens.themes.theme_builders import ButtonThemeBuilder, LabelThemeBuilder, ThemeData
from PyQt5.QtCore import QEvent, QPoint, QRect, Qt, pyqtSignal
from PyQt5.QtGui import QKeyEvent, QShowEvent
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QWidget
from utils.ui.application_utils import UiUtils
from views.dialogs.confirm_dialog import ConfirmDialog
from views.view import View
from widgets.smooth_scroll_area import SmoothVerticalScrollArea

from .empty_table_notification import EmptySongTableNotification
from .song_row import SongItem


class SongTableBody(SmoothVerticalScrollArea, View):
    keyPressed = pyqtSignal(QEvent)

    def __init__(self, parent: Optional["QWidget"] = None):
        super(SongTableBody, self).__init__(parent)
        self.setupUi()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.keyPressed.emit(event)
        return super().keyPressEvent(event)

    def setupUi(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setItemHeight(104)
        self.setStyleSheet(
            "QScrollBar:vertical{border:none;background:TRANSPARENT;width:4px}"
            "QScrollBar::handle:vertical{background:rgba(160,160,160,0.5);border-radius:2px}"
            "QScrollBar::handle:vertical:hover{background:#8040ff}"
            "QScrollBar::sub-line:vertical{border:none}"
            "QScrollBar::add-line:vertical{border:none}"
            "QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{background:none}"
            "QScrollBar::up-arrow:vertical,QScrollBar::down-arrow:vertical{background:none}"
        )

        self.inner = QWidget(self)
        self.setWidget(self.inner)
        self.menu = QVBoxLayout(self.inner)
        self.menu.setAlignment(Qt.AlignTop)
        self.menu.setSpacing(0)
        self.menu.setContentsMargins(8, 0, 8, 8)
        self.emptyNotification = EmptySongTableNotification(self.inner)
        self.emptyNotification.setMessage("Oh no, you don't have any song yet", "Add Now")
        self.emptyNotification.setFixedSize(256, 400)

    def getKeyFromEvent(self, event: QKeyEvent, controller=None) -> None:
        isHoldingALT = int(event.modifiers()) == Qt.AltModifier
        if not isHoldingALT:
            return
        try:
            key = chr(event.key())
            index = controller.handleFindSongInsertIndexWithTitle(key)
            self.scrollToItem(index)
        except ValueError:
            pass

    def connectToController(self, controller):
        self.keyPressed.connect(lambda event: self.getKeyFromEvent(event, controller))

    def lightMode(self) -> None:
        super().lightMode()
        songCount = self.getTotalSongAvailable()
        for index in range(0, songCount):
            self.__getSongByIndex(index).lightMode()

    def darkMode(self) -> None:
        super().darkMode()
        songCount = self.getTotalSongAvailable()
        for index in range(0, songCount):
            self.__getSongByIndex(index).darkMode()

    def updateLayout(self, totalItem: int, controller) -> None:
        itemsDisplaying = self.getTotalSongAvailable()

        if totalItem == 0:
            self.emptyNotification.show()
            self.__removePlaylistsInRange(totalItem, itemsDisplaying)
            return

        self.__hidePlaylistEmptyNotification()
        totalPlaylistLacking = totalItem - itemsDisplaying
        if totalPlaylistLacking == 0:
            return

        isDisplayingMoreThanNumberOfPlaylists = totalPlaylistLacking < 0
        if isDisplayingMoreThanNumberOfPlaylists:
            self.__removePlaylistsInRange(totalItem, itemsDisplaying)
            return

        isDisplayingLessThanNumberOfPlaylists = totalPlaylistLacking > 0
        if isDisplayingLessThanNumberOfPlaylists:
            self.__addLackingPlaylists(totalPlaylistLacking, controller)

    def displaySongInfoAtIndex(self, index: int, cover: bytes, title: str, artist: str, length: float) -> None:
        song = self.__getSongByIndex(index)
        song.show()
        song.showLess()
        song.setCover(cover)
        song.setTitle(title)
        song.setArtist(artist)
        song.setLength(length)

    def showEvent(self, a0: QShowEvent) -> None:
        self.emptyNotification.move(self.inner.rect().center() - self.emptyNotification.rect().center())
        return super().showEvent(a0)

    def setSongCoverAtIndex(self, index: int, cover: bytes) -> None:
        self.__getSongByIndex(index).setCover(cover)

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

    def __hidePlaylistEmptyNotification(self):
        if self.emptyNotification is None:
            return
        self.emptyNotification.hide()

    def __addLackingPlaylists(self, numberOfPlaylist: int, controller) -> None:
        defaultValues: dict = {
            "theme": ThemeData(
                lightMode="QWidget{background-color:rgba(0, 0, 0, 0.1);border-radius:16px}QWidget:hover{background-color:rgba(0, 0, 0, 0.15)}",
                darkMode="QWidget{background-color:rgba(255, 255, 255, 0.1);border-radius:16px}QWidget:hover{background-color:rgba(255, 255, 255, 0.15)}",
            ),
            "labels": {
                "themes": {
                    "PRIMARY": (
                        LabelThemeBuilder()
                        .addLightModeTextColor(ColorBoxes.BLACK)
                        .addDarkModeTextColor(ColorBoxes.WHITE)
                        .build(itemSize=IconSizes.LARGE.height())
                    ),
                    "secondary": (
                        LabelThemeBuilder()
                        .addLightModeTextColor(ColorBoxes.GRAY)
                        .addDarkModeTextColor(ColorBoxes.GRAY)
                        .build(itemSize=IconSizes.LARGE.height())
                    ),
                },
            },
            "buttons": {
                "themes": {
                    "PRIMARY": (
                        ButtonThemeBuilder()
                        .addLightModeBackground(Backgrounds.CIRCLE_HIDDEN_PRIMARY_25)
                        .addDarkModeBackground(Backgrounds.CIRCLE_HIDDEN_WHITE_25)
                        .build(itemSize=IconSizes.LARGE.height())
                    ),
                    "secondary": (
                        ButtonThemeBuilder()
                        .addLightModeBackground(Backgrounds.CIRCLE_PRIMARY_25)
                        .addDarkModeBackground(Backgrounds.CIRCLE_WHITE_25)
                        .build(itemSize=IconSizes.LARGE.height())
                    ),
                    "DANGER": (
                        ButtonThemeBuilder()
                        .addLightModeBackground(Backgrounds.CIRCLE_DANGER)
                        .addDarkModeBackground(None)
                        .build(itemSize=IconSizes.MEDIUM.height())
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
            labelThemes=values.get("labels").get("themes"),
            buttonThemes=values.get("buttons").get("themes"),
        )
        song.setDefaultCover(ApplicationImage.defaultSongCover)
        song.setDefaultArtist("")
        song.setTitle("Title")
        song.setLength(0)
        self.menu.addWidget(song)
        UiUtils.setAttribute(self, "song", index, song)
        return song

    def __confirmDeleteSongAtIndex(self, index: int, controller) -> None:
        message_box = ConfirmDialog(
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
