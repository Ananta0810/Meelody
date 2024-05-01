from typing import Optional

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QWidget

from app.common.asyncs import ChunksConsumer
from app.common.models import Song
from app.common.others import appCenter, musicPlayer
from app.components.events import VisibleObserver
from app.components.scroll_areas import SmoothVerticalScrollArea
from app.helpers.base import Lists
from app.views.home.songs_table.song_row import SongRow

MAX_ITEMS_VISIBLE_ON_MENU = 6


class SongsMenu(SmoothVerticalScrollArea):
    __keyPressed = pyqtSignal(QKeyEvent)
    __menuReset = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.__coverLoadedSongIds: set[str] = set()
        self.__songRowDict: dict[str, SongRow] = {}
        self.__titles: dict[str, int] = {}
        self.__titleKeys: dict[str, list[int]] = {}

        self._initComponent()

    def _createUI(self) -> None:
        super()._createUI()
        self.setClassName("scroll/bg-primary-50 scroll/hover:bg-primary scroll/rounded-2")
        self.setContentsMargins(8, 0, 8, 8)

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()
        self.__keyPressed.connect(self.__onKeyPressed)
        VisibleObserver(self).visible.connect(lambda visible: self.__showLibrary())

        appCenter.currentPlaylistChanged.connect(lambda playlist: self.__setSongs(playlist.getSongs().getSongs()))
        musicPlayer.songChanged.connect(self.__scrollToSong)

    def __showLibrary(self) -> None:
        rows = [row for row in self.__songRowDict.values()]
        self.__showSongs(rows)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.__keyPressed.emit(event)
        return super().keyPressEvent(event)

    def __onKeyPressed(self, event: QKeyEvent) -> None:
        isHoldingAlt = int(event.modifiers()) == Qt.AltModifier
        if not isHoldingAlt:
            return
        try:
            key = chr(event.key())
            index = self.__findSongPositionToScroll(key)
            if index == -1:
                return
            self.scrollToItemAt(index)
        except ValueError:
            pass

    def __findSongPositionToScroll(self, key: str) -> int:
        if key not in self.__titleKeys:
            return -1
        indexes = self.__titleKeys[key]
        if len(indexes) == 0:
            return -1

        currentIndex = self.getCurrentItemIndex()
        nextIndex = Lists.nearestLinearSearch(indexes, currentIndex) + 1
        try:
            return indexes[nextIndex]
        except IndexError:
            return indexes[0]

    def __scrollToSong(self, song: Song) -> None:
        if song.getTitle() in self.__titles:
            self.scrollToItemAt(self.__titles[song.getTitle()])

    def __setSongs(self, songs: list[Song]) -> None:
        self.__menuReset.emit()

        self.__titles = {song.getTitle(): index for index, song in enumerate(songs)}
        self.__titleKeys = self.__createTitleMap(songs)

        if len(self.__songRowDict) == 0:
            for song in songs:
                songRow = SongRow(song)
                songRow.hide()
                songRow.applyTheme()
                self.addWidget(songRow)
                self.__songRowDict[song.getId()] = songRow
            return

        rows = [self.__songRowDict.get(song.getId()) for song in songs]
        self.__showSongs(rows)

    def __showSongs(self, rows: list[SongRow]) -> None:
        for songRow in self.__songRowDict.values():
            songRow.hide()

        displayer = ChunksConsumer(items=rows, size=MAX_ITEMS_VISIBLE_ON_MENU)
        displayer.forEach(lambda row: row.show(), delay=10)
        self.__menuReset.connect(displayer.stop)
        displayer.stopped.connect(self.__menuReset.disconnect)
        displayer.stopped.connect(self.__loadCovers)

    def __loadCovers(self) -> None:
        allCoversAreLoaded = len(self.__coverLoadedSongIds) == len(self.__songRowDict)
        if allCoversAreLoaded:
            return

        rows = [song for songId, song in self.__songRowDict.items() if songId not in self.__coverLoadedSongIds]

        displayer = ChunksConsumer(items=rows, size=1)
        displayer.forEach(lambda row: self.__loadCoverFor(row))

    def __loadCoverFor(self, row: SongRow) -> None:
        row.loadCover()
        self.__coverLoadedSongIds.add(row.content().getId())

    @staticmethod
    def __createTitleMap(songs: list[Song]) -> dict[str, list[int]]:
        titles = {}
        for index, song in enumerate(songs):
            firstChar = song.getTitle()[0]
            if firstChar not in titles:
                titles[firstChar] = []
            titles[firstChar].append(index)
        return titles
