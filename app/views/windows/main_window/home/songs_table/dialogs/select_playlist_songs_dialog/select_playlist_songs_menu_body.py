from typing import Optional

from PyQt5.QtCore import pyqtSignal, Qt, pyqtBoundSignal
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QWidget

from app.common.models import Song
from app.common.others import appCenter
from app.components.scroll_areas import SmoothVerticalScrollArea
from app.utils.base import Lists, Dicts
from app.views.windows.main_window.home.songs_table.dialogs.select_playlist_songs_dialog.select_playlist_song_row import SongRow


class MenuBody(SmoothVerticalScrollArea):
    __keyPressed: pyqtBoundSignal = pyqtSignal(QKeyEvent)

    songSelected: pyqtBoundSignal = pyqtSignal(Song)
    songUnSelected: pyqtBoundSignal = pyqtSignal(Song)
    songsLoaded: pyqtBoundSignal = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        self.__rowDict: dict[str, SongRow] = {}
        self.__titles: dict[str, int] = {}

        super().__init__(parent)
        self._initComponent()

    def _createUI(self) -> None:
        super()._createUI()
        self._menu.setContentsMargins(0, 0, 0, 0)

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()
        self.__keyPressed.connect(lambda e: self.__onKeyPressed(e))

    def applyLightMode(self) -> None:
        group = Dicts.group(self._lightModeStyle.split("\n"), lambda props: "QScrollArea" in props)
        scrollAreaStyle = "\n".join(group.get(False))
        scrollbarStyle = "\n".join(group.get(True))

        self.setStyleSheet(scrollAreaStyle)
        self.verticalScrollBar().setStyleSheet(scrollbarStyle)

    def applyDarkMode(self) -> None:
        group = Dicts.group(self._darkModeStyle.split("\n"), lambda props: "QScrollArea" in props)
        scrollAreaStyle = "\n".join(group.get(False))
        scrollbarStyle = "\n".join(group.get(True))

        self.setStyleSheet(scrollAreaStyle)
        self.verticalScrollBar().setStyleSheet(scrollbarStyle)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        super().keyPressEvent(event)
        self.__keyPressed.emit(event)

    def showSongs(self) -> None:
        songs = appCenter.library.getSongs().toList()
        for index, song in enumerate(songs):
            songRow = SongRow(song)
            songRow.checked.connect(lambda _song: self.songSelected.emit(_song))
            songRow.unchecked.connect(lambda _song: self.songUnSelected.emit(_song))

            if index < 6 or index != len(songs) - 1:
                songRow.setClassName(
                    "hover:bg-gray-8 border-l border-b border-gray-12 bg-white",
                    "dark:bg-white-[b12] dark:hover:bg-white-[b16] dark:border-white-[b20]"
                )
            else:
                songRow.setClassName(
                    "hover:bg-gray-8 border-l border-gray-12 bg-white",
                    "dark:bg-white-[b12] dark:hover:bg-white-[b16] dark:border-white-[b20]"
                )

            songRow.applyTheme()

            self.addWidget(songRow)
            self.__rowDict[song.getId()] = songRow

        self.__updateTitleMaps(songs)
        self.songsLoaded.emit()

    def deleteLater(self) -> None:
        super().deleteLater()

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
