from typing import Optional

from constants.ui.base import ApplicationImage
from constants.ui.qss import Backgrounds
from constants.ui.qt import IconSizes
from constants.ui.theme_builders import IconButtonThemeBuilders, TextThemeBuilders
from modules.screens.themes.theme_builders import ScrollThemeBuilder, ThemeData
from PyQt5.QtCore import QEvent, QPoint, Qt, pyqtSignal
from PyQt5.QtGui import QKeyEvent, QShowEvent, QWheelEvent
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QWidget
from utils.ui.application_utils import UiUtils
from views.dialogs.confirm_dialog import ConfirmDialog
from views.view import View
from widgets.smooth_scroll_area import SmoothVerticalScrollArea

from .empty_table_notification import EmptySongTableNotification
from .song_row import SongItem, getSongCoverPixmap


class SongTableBody(SmoothVerticalScrollArea, View):
    keyPressed = pyqtSignal(QEvent)

    def __init__(self, parent: Optional["QWidget"] = None):
        super(SongTableBody, self).__init__(parent)
        self.covers = []
        self.start = 0
        self.last = 6
        self.setupUi()
        self.verticalScrollBar().valueChanged.connect(self.setLaterLoading)

    # def wheelEvent(self, event: QWheelEvent) -> None:
    #     self.laterLoading()
    #     return super().wheelEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.keyPressed.emit(event)
        return super().keyPressEvent(event)

    def setLaterLoading(self) -> None:
        currentPos = self.__getCurrentIndex()

        self.setStart(currentPos - 6)
        self.setLastItem(currentPos + 6)
        self.laterLoading()

    def laterLoading(self) -> None:
        for index in range(self.start, self.last):
            if self.covers[index] is None:
                continue
            self.__getSongByIndex(index).setCover(self.covers[index])
            self.covers[index] = None

    def setupUi(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setItemHeight(104)
        self._addThemeForItem(
            self, theme=ScrollThemeBuilder().addLightModeBackground(Backgrounds.CIRCLE_PRIMARY).build()
        )

        self.inner = QWidget(self)
        self.setWidget(self.inner)
        self.menu = QVBoxLayout(self.inner)
        self.menu.setAlignment(Qt.AlignTop)
        self.menu.setSpacing(0)
        self.menu.setContentsMargins(8, 0, 8, 8)

        self.emptyNotification = EmptySongTableNotification(self.inner)
        self.emptyNotification.setMessage("Oh no! You don't have any song yet", "Add Now")

    def __getCurrentIndex(self) -> int:
        return self.verticalScrollBar().value() // self._itemHeight

    def getKeyFromEvent(self, event: QKeyEvent, controller=None) -> None:
        isHoldingALT = int(event.modifiers()) == Qt.AltModifier
        if not isHoldingALT:
            return
        try:
            key = chr(event.key())
            index = controller.handleFindSongInsertIndexWithTitle(key)
            self.setStart(index - 6)
            self.setLastItem(index + 6)
            self.laterLoading()
            self.scrollToItem(index)
        except ValueError:
            pass

    def setStart(self, index: int) -> None:
        self.start = index if index >= 0 else 0

    def setLastItem(self, index: int) -> None:
        max = len(self.covers) - 1
        self.last = index if index <= max else max

    def connectToController(self, controller):
        self.keyPressed.connect(lambda event: self.getKeyFromEvent(event, controller))

    def lightMode(self) -> None:
        self.emptyNotification.lightMode()
        songCount = self.getTotalSongAvailable()
        for index in range(0, songCount):
            self.__getSongByIndex(index).lightMode()
        return super().lightMode()

    def darkMode(self) -> None:
        self.emptyNotification.darkMode()
        songCount = self.getTotalSongAvailable()
        for index in range(0, songCount):
            self.__getSongByIndex(index).darkMode()
        return super().darkMode()

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
        self.covers.append(cover)
        song = self.__getSongByIndex(index)
        song.show()
        song.showLess()
        if self.start < index <= self.last:
            song.setCover(cover)
        song.setTitle(title)
        song.setArtist(artist)
        song.setLength(length)

    def showEvent(self, a0: QShowEvent) -> None:
        offsetToTopForTheBalanceOfNotification = QPoint(0, 48)
        self.emptyNotification.move(
            self.inner.rect().center() - self.emptyNotification.rect().center() - offsetToTopForTheBalanceOfNotification
        )
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
        for index in range(0, numberOfPlaylist):
            self.__addNewEmptyPlaylist(controller)

    def __addNewEmptyPlaylist(self, controller) -> None:
        index = self.getTotalSongAvailable()
        song = self.__addSong(index)

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

    def __addSong(self, index: int):
        song = SongItem()
        song.setWidgetThemes(
            ThemeData(
                lightMode="SongItem{background-color:TRANSPARENT;border-radius:24px}SongItem:hover{background-color:rgba(0, 0, 0, 0.1)}",
                darkMode="SongItem{background-color:TRANSPARENT;border-radius:24px}SongItem:hover{background-color:rgba(255, 255, 255, 0.1)}",
            )
        )
        song.setButtonThemes(
            primary=IconButtonThemeBuilders.CIRCLE_HIDDEN_PRIMARY_25.build(itemSize=IconSizes.LARGE.height()),
            secondary=IconButtonThemeBuilders.CIRCLE_PRIMARY_25.build(itemSize=IconSizes.LARGE.height()),
            danger=IconButtonThemeBuilders.CIRCLE_DANGER.build(itemSize=IconSizes.MEDIUM.height()),
        )
        song.setTextThemes(
            primary=TextThemeBuilders.DEFAULT.build(),
            secondary=TextThemeBuilders.GRAY.build(),
        )
        song.setDefaultCover(getSongCoverPixmap(ApplicationImage.defaultSongCover))
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
