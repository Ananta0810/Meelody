from typing import Optional

from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QWidget

from app.common.models import Song
from app.common.others import appCenter, musicPlayer
from app.components.scroll_areas import SmoothVerticalScrollArea
from app.helpers.base import Lists
from app.views.home.songs_table.song_row import SongRow

MAX_ITEMS_VISIBLE_ON_MENU = 6


class SongsMenu(SmoothVerticalScrollArea):
    keyPressed = pyqtSignal(QKeyEvent)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.__currentDisplayingChunk: int = 0
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
        appCenter.currentPlaylistChanged.connect(lambda playlist: self.__setSongs(playlist.getSongs().getSongs()))
        musicPlayer.songChanged.connect(self.__scrollToSong)
        self.keyPressed.connect(self.__onKeyPressed)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.keyPressed.emit(event)
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
        self.__titles = {song.getTitle(): index for index, song in enumerate(songs)}
        self.__titleKeys = self.__createTitleMap(songs)

        if len(self.__songRowDict) == 0:
            for song in songs:
                songRow = SongRow(song)
                songRow.applyTheme()
                self.addWidget(songRow)
                self.__songRowDict[song.getId()] = songRow
            return

        self.__displaySongs(songs)

    def __displaySongs(self, songs):
        for song in self.__songRowDict.values():
            song.hide()

        idsToShow = [song.getId() for song in songs]
        chunks = [idsToShow[x:x + MAX_ITEMS_VISIBLE_ON_MENU] for x in range(0, len(idsToShow), MAX_ITEMS_VISIBLE_ON_MENU)]

        self.__currentDisplayingChunk = 0

        timer = QTimer()
        timer.start(10)
        timer.timeout.connect(lambda: self.__displaySongsInChunks(timer, chunks))

    def __displaySongsInChunks(self, timer: QTimer, chunks: list[list[str]]) -> None:
        if self.__currentDisplayingChunk >= len(chunks):
            timer.stop()
            return

        idsToShow = chunks[self.__currentDisplayingChunk]

        for songId in idsToShow:
            self.__songRowDict[songId].show()

        self.__currentDisplayingChunk += 1
        timer.start(10)

    @staticmethod
    def __createTitleMap(songs: list[Song]) -> dict[str, list[int]]:
        titles = {}
        for index, song in enumerate(songs):
            firstChar = song.getTitle()[0]
            if firstChar not in titles:
                titles[firstChar] = []
            titles[firstChar].append(index)
        return titles
