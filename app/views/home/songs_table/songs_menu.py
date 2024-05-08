from contextlib import suppress
from typing import Optional

from PyQt5.QtCore import Qt, pyqtSignal, QObject, QEvent
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QWidget, qApp

from app.common.asyncs import ChunksConsumer
from app.common.models import Song, Playlist
from app.common.models.playlists import Library
from app.common.others import appCenter, musicPlayer
from app.components.events import VisibleObserver
from app.components.scroll_areas import SmoothVerticalScrollArea
from app.helpers.base import Lists, Strings, silence, suppressException
from app.helpers.qt import Widgets
from app.views.home.songs_table.song_row import SongRow

MAX_ITEMS_VISIBLE_ON_MENU = 6


class SongsMenu(SmoothVerticalScrollArea):
    __menuReset = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.__coverLoadedSongIds: set[str] = set()
        self.__songRowDict: dict[str, SongRow] = {}

        self.__currentPlaylist: Optional[Playlist.Songs] = None

        # This map is used to find the index of the playing song in the playlist to navigate to.
        self.__songMap: dict[str, str] = {}

        # This map is used to navigate to songs by key.
        self.__titleKeys: dict[str, list[int]] = {}

        self._initComponent()
        qApp.installEventFilter(self)

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()

        appCenter.library.getSongs().updated.connect(lambda: self.__createSongRows(appCenter.library.getSongs().getSongs()))
        appCenter.currentPlaylistChanged.connect(lambda playlist: self.__showSongsOfPlaylist(playlist))

        musicPlayer.songChanged.connect(lambda song: self.__scrollToSong(song))

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.KeyPress:
            if Widgets.isDescendantOf(self.window(), obj):
                self.__onKeyPressed(event)
        return super().eventFilter(obj, event)

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
        if song.getId() in self.__songMap:
            self.scrollToItemAt(self.__songMap[song.getId()])

    def __createSongRows(self, songs: list[Song]) -> None:
        """
        This function is used to create rows on song menu. Those rows will be re-used later to shown as items on menu.
        """
        onStartup = len(self.__songRowDict) == 0

        if onStartup:
            for song in songs:
                self.__addRow(song)

            self.__menuReset.emit()
            return

        currentSongs = [row.content() for row in self.__songRowDict.values()]

        addedSongs = Lists.itemsInRightOnly(currentSongs, songs)
        removedSongs = Lists.itemsInLeftOnly(currentSongs, songs)

        maxHeight = sum([row.minimumHeight() for row in self.__songRowDict.values()])
        self._menu.setMaximumHeight(maxHeight)

        currentPosition = self.verticalScrollBar().value()

        for song in addedSongs:
            self.__addRow(song)

        for song in removedSongs:
            row = self.__songRowDict[song.getId()]
            self.__removeRow(row)

        self.__moveRows(songs)

        self.verticalScrollBar().setValue(currentPosition)

        self.__menuReset.emit()

    def __moveRows(self, newSongs: list[Song]) -> None:
        oldSongs = [row.content() for row in self.widgets()]
        oldIndex, newIndex = Lists.findMoved(oldSongs, newSongs)
        if oldIndex >= 0:
            rowToMove = self.widgets()[oldIndex]
            self.moveWidget(rowToMove, newIndex)
            rowToMove.showMoreButtons(False)

    def __addRow(self, song):
        songRow = SongRow(song)
        songRow.applyTheme()
        songRow.setMinimumSize(songRow.sizeHint())
        songRow.hide()
        self.addWidget(songRow)
        self.__songRowDict[song.getId()] = songRow

    def __removeRow(self, row: SongRow) -> None:
        self.removeWidget(row)
        row.deleteLater()

        self.__songRowDict.pop(row.content().getId())

    def __showSongsOfPlaylist(self, playlist: Playlist) -> None:
        if not Widgets.isInView(self):
            VisibleObserver(self).visible.connect(lambda visible: self.__showSongsOfPlaylist(playlist) if visible else None)
            return

        isUpdatedPlaylist = self.__currentPlaylist != playlist

        if isUpdatedPlaylist:
            with suppress(Exception):
                self.__currentPlaylist.updated.disconnect(lambda: self.__showSongsOfPlaylist(playlist))

            playlist.getSongs().updated.connect(lambda: self.__showSongsOfPlaylist(playlist))

        self.__currentPlaylist = playlist
        self.__updateTitleMaps(playlist.getSongs().getSongs())

        isLibrary = playlist.getInfo().getId() == Library.Info().getId()
        songIdSet = set([song.getId() for song in playlist.getSongs().getSongs()])
        songRows: list[SongRow] = self.widgets()

        needUpdateVisible = any([row.isVisible() != (row.content().getId() in songIdSet) for row in songRows])
        if not needUpdateVisible:
            return

        currentPosition = self.verticalScrollBar().value()

        for songRow in songRows:
            songRow.setEditable(isLibrary)
            songRow.showMoreButtons(False)
            songRow.hide()

        self.__showRows([row for row in songRows if row.content().getId() in songIdSet])

        self.verticalScrollBar().setValue(currentPosition)

    def __showRows(self, rows: list[SongRow]) -> None:

        displayer = ChunksConsumer(items=rows, size=MAX_ITEMS_VISIBLE_ON_MENU, parent=self)
        displayer.stopped.connect(lambda: silence(lambda: self.__menuReset.disconnect(displayer.stop)))
        displayer.stopped.connect(lambda: self.__loadCovers())
        self.__menuReset.connect(displayer.stop)

        self._menu.setMinimumHeight(0)
        displayer.forEach(lambda row, index: self.__showRow(row, index), delay=10)

    @suppressException
    def __showRow(self, row: SongRow, index: int) -> None:
        self._menu.setMinimumHeight(min((index + 1) * row.minimumHeight(), self._menu.maximumHeight()))
        row.show()

    def __updateTitleMaps(self, songs: list[Song]) -> None:
        self.__songMap = {song.getId(): index for index, song in enumerate(songs)}

        self.__titleKeys = {}
        for index, song in enumerate(songs):
            firstChar = Strings.unaccent(song.getTitle()[0].upper())
            if firstChar not in self.__titleKeys:
                self.__titleKeys[firstChar] = []
            self.__titleKeys[firstChar].append(index)

    def __loadCovers(self) -> None:
        allCoversAreLoaded = len(self.__coverLoadedSongIds) == len(self.__songRowDict)
        if allCoversAreLoaded:
            return

        rows = [song for songId, song in self.__songRowDict.items() if songId not in self.__coverLoadedSongIds]

        displayer = ChunksConsumer(items=rows, size=1, parent=self)
        displayer.forEach(lambda row, index: self.__loadCoverFor(row))

    def __loadCoverFor(self, row: SongRow) -> None:
        row.loadCover()
        self.__coverLoadedSongIds.add(row.content().getId())
