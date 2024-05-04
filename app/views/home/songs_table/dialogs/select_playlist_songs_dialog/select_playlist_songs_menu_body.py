from typing import Optional

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QWidget

from app.common.models import Song
from app.common.others import appCenter
from app.components.scroll_areas import SmoothVerticalScrollArea
from app.helpers.base import Lists
from app.views.home.songs_table.dialogs.select_playlist_songs_dialog.select_playlist_song_row import SongRow


class MenuBody(SmoothVerticalScrollArea):
    __keyPressed = pyqtSignal(QKeyEvent)

    songSelected = pyqtSignal(Song)
    songUnSelected = pyqtSignal(Song)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        self.__rowDict: dict[str, SongRow] = {}
        self.__titles: dict[str, int] = {}

        super().__init__(parent)
        self._initComponent()
        self.__setSongs()

    def _createUI(self) -> None:
        super()._createUI()
        self._menu.setContentsMargins(0, 0, 0, 0)

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()
        self.__keyPressed.connect(self.__onKeyPressed)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        super().keyPressEvent(event)
        self.__keyPressed.emit(event)

    def __setSongs(self) -> None:
        songs = appCenter.library.getSongs().getSongs()
        for song in songs:
            songRow = SongRow(song)
            songRow.applyTheme()
            songRow.checked.connect(lambda _song: self.songSelected.emit(_song))
            songRow.unchecked.connect(lambda _song: self.songUnSelected.emit(_song))
            self.addWidget(songRow)
            self.__rowDict[song.getId()] = songRow

        self.__updateTitleMaps(songs)

    def __updateTitleMaps(self, songs: list[Song]) -> None:
        self.__titleKeys = {}
        for index, song in enumerate(songs):
            firstChar = song.getTitle()[0]
            if firstChar not in self.__titleKeys:
                self.__titleKeys[firstChar] = []
            self.__titleKeys[firstChar].append(index)

    def setSelectedSongs(self, songs: list[Song]) -> None:
        for song in songs:
            self.__rowDict[song.getId()].select()

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
