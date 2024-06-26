from contextlib import suppress
from typing import Optional

from PyQt5.QtCore import Qt, pyqtSignal, QObject, QEvent, pyqtBoundSignal
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QWidget, qApp

from app.common.models import Song, Playlist
from app.common.others import appCenter, musicPlayer
from app.components.asyncs import ChunksConsumer
from app.components.dialogs import Dialogs
from app.components.scroll_areas import SmoothVerticalScrollArea
from app.utils.base import Lists, Strings, silence
from app.utils.qt import Widgets
from app.utils.reflections import suppressException
from app.views.windows.main_window.home.songs_table.song_row import SongRow

MAX_ITEMS_VISIBLE_ON_MENU = 6


class SongsMenu(SmoothVerticalScrollArea):
    __playlistUpdated: pyqtBoundSignal = pyqtSignal()
    __rowMoved: pyqtBoundSignal = pyqtSignal(int)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.__songRowDict: dict[str, SongRow] = {}

        self.__currentPlaylist: Optional[Playlist] = None

        # This map is used to find the index of the playing song in the playlist to navigate to.
        self.__songMap: dict[str, int] = {}

        # This map is used to navigate to songs by key.
        self.__titleKeys: dict[str, list[int]] = {}

        self._initComponent()

        self.__loadLibrarySongs(appCenter.library.getSongs())
        qApp.installEventFilter(self)

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()

        self.__playlistUpdated.connect(lambda: self.__showSongsOfPlaylist(self.__currentPlaylist))
        self.__rowMoved.connect(lambda index: self.__askToScrollToSongAt(index))

        appCenter.library.getSongs().updated.connect(lambda: self.__updateLayoutBasedOnLibrary(appCenter.library.getSongs()))
        appCenter.library.getSongs().moved.connect(lambda fromIndex, toIndex: self.__moveRow(fromIndex, toIndex))
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
            itemIndex = self.__songMap[song.getId()]
            self.scrollToItemAt(itemIndex)

    def __askToScrollToSongAt(self, index: int) -> None:
        Dialogs.confirm(
            header=self.translate("UPDATE_SONG.SUCCESS"),
            message=self.translate("UPDATE_SONG.MOVED_MSG"),
            acceptText=self.translate("UPDATE_SONG.MOVED_ACCEPT_BTN"),
            cancelText=self.translate("UPDATE_SONG.MOVED_CANCEL_BTN"),
            onAccept=lambda: self.scrollToItemAt(index),
            variant="info"
        )

    def __loadLibrarySongs(self, songs: Playlist.Songs) -> None:
        """
            This function is used to create rows on song menu on startup. Those rows will be re-used later to shown as items on menu.
        """
        if not appCenter.isLoaded:
            appCenter.loaded.connect(lambda: self.__loadLibrarySongs(songs))
            return

        self.__updateLayoutBasedOnLibrary(songs)
        self.__playlistUpdated.emit()

    def __updateLayoutBasedOnLibrary(self, songs: Playlist.Songs) -> None:
        """
            This function is used to create rows on song menu on realtime. Those rows will be re-used later to shown as items on menu.
        """
        currentSongs = [row.content() for row in self.__songRowDict.values()]

        songList = songs.toList()

        addedSongs = Lists.itemsInRightOnly(currentSongs, songList)
        removedSongs = Lists.itemsInLeftOnly(currentSongs, songList)

        currentPosition = self.verticalScrollBar().value()

        for song in addedSongs:
            index = songs.indexOf(song)
            self.__insertRow(index, song)

        for song in removedSongs:
            row = self.__songRowDict[song.getId()]
            self.__removeRow(row)

        maxHeight = sum([row.sizeHint().height() for row in self.__songRowDict.values()])
        self._menu.setMaximumHeight(maxHeight)

        self.verticalScrollBar().setValue(currentPosition)

    def __insertRow(self, index: int, song: Song) -> None:
        songRow = SongRow(song)
        songRow.applyTheme()
        songRow.setMinimumSize(songRow.sizeHint())
        songRow.hide()

        self.insertWidget(index, songRow)
        self.__songRowDict[song.getId()] = songRow

    def __removeRow(self, row: SongRow) -> None:
        self.removeWidget(row)
        row.deleteLater()

        self.__songRowDict.pop(row.content().getId())

    def __moveRow(self, oldIndex: int, newIndex: int) -> None:
        if oldIndex < 0 or newIndex < 0:
            return
        currentPosition = self.verticalScrollBar().value()
        rowToMove = self.widgets()[oldIndex]
        self.moveWidget(rowToMove, newIndex)
        self.verticalScrollBar().setValue(currentPosition)

        if self.__currentPlaylist.getInfo().getId() == appCenter.library.getInfo().getId():
            self.__rowMoved.emit(newIndex)

    def __showSongsOfPlaylist(self, playlist: Playlist) -> None:
        if not appCenter.isLoaded:
            self.__currentPlaylist = playlist
            self.__currentPlaylist.getSongs().updated.connect(self.__playlistUpdated.emit)
            return

        isPlaylistChanged = self.__currentPlaylist != playlist

        if isPlaylistChanged:
            if self.__currentPlaylist is not None:
                with suppress(TypeError):
                    self.__currentPlaylist.getSongs().updated.disconnect(self.__playlistUpdated.emit)

            self.__currentPlaylist = playlist
            self.__currentPlaylist.getSongs().updated.connect(self.__playlistUpdated.emit)

        self.__updateTitleMaps(playlist.getSongs().toList())

        songIdSet = set([song.getId() for song in playlist.getSongs().toList()])
        songRows: list[SongRow] = self.widgets()

        visibleRowIdSet = {row.content().getId() for row in songRows if row.isVisible()}

        needUpdateVisible = visibleRowIdSet != songIdSet

        if not needUpdateVisible:
            return

        currentPosition = self.verticalScrollBar().value()

        isLibrary = playlist.getInfo().getId() == appCenter.library.getInfo().getId()

        for songRow in songRows:
            songRow.setEditable(isLibrary)
            songRow.hide()

        self.__showRows([row for row in songRows if row.content().getId() in songIdSet])

        if not isPlaylistChanged:
            self.verticalScrollBar().setValue(currentPosition)

    def __showRows(self, rows: list[SongRow]) -> None:
        displayer = ChunksConsumer(items=rows, size=MAX_ITEMS_VISIBLE_ON_MENU, parent=self)
        displayer.stopped.connect(lambda: silence(lambda: self.__playlistUpdated.disconnect(displayer.stop)))
        self.__playlistUpdated.connect(displayer.stop)

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
            try:
                firstChar = Strings.unaccent(song.getTitle()[0].upper())
                if firstChar not in self.__titleKeys:
                    self.__titleKeys[firstChar] = []
                self.__titleKeys[firstChar].append(index)
            except TypeError:
                pass
