from PyQt5.QtCore import Qt

from app.common.models import Playlist, Song
from app.common.others import translator
from app.components.base import FontFactory
from app.components.buttons import ActionButton
from app.components.dialogs import BaseDialog
from app.components.events import VisibleObserver
from app.components.widgets import StyleWidget, FlexBox, Box
from .select_playlist_songs_menu_body import MenuBody
from .select_playlist_songs_menu_header import MenuHeader


class SelectPlaylistSongsDialog(BaseDialog):

    def __init__(self, playlist: Playlist) -> None:
        self.__playlist: Playlist = playlist
        self.__selectedSongs: Playlist.Songs = playlist.getSongs().clone()
        self.__playlistSongIds: list[str] = self.__songIdsOf(playlist.getSongs().toList())

        super().__init__()
        super()._initComponent()

    def _createUI(self) -> None:
        super()._createUI()
        self.setContentsMargins(20, 20, 20, 20)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self._menuHeader = MenuHeader()
        self._menuHeader.setFixedWidth(640)
        self._menuHeader.setContentsMargins(0, 16, 0, 16)
        self._menuHeader.setClassName("bg-gray-4 border border-gray-12 rounded-t-8 dark:border-white-[b20]")

        self._menuBodyWrapper = StyleWidget()
        self._menuBodyWrapper.setClassName("border-r border-gray-12")
        self._menuBodyWrapperLayout = Box(self._menuBodyWrapper)

        self._menuBody = MenuBody()
        self._menuBody.setFixedSize(640, 480)
        self._menuBody.setContentsMargins(0, 0, 0, 0)
        self._menuBody.setClassName("scroll/bg-primary-75 scroll/hover:bg-primary scroll/rounded-2")
        self._menuBody.widget().setClassName("bg-white border-l border-gray-12 dark:border-white-[b20]")

        self._menuBodyWrapperLayout.addWidget(self._menuBody)

        self._footer = StyleWidget()
        self._footer.setFixedWidth(640)
        self._footer.setClassName("rounded-b-8 border border-gray-12 dark:border-white-[b20]")

        self._footerLayout = FlexBox()
        self._footerLayout.setContentsMargins(8, 8, 8, 8)
        self._footerLayout.setAlignment(Qt.AlignRight)

        self._footer.setLayout(self._footerLayout)

        self._applyBtn = ActionButton()
        self._applyBtn.setMinimumWidth(64)
        self._applyBtn.setFont(FontFactory.create(family="Segoe UI Semibold", size=10))
        self._applyBtn.setClassName(
            "text-white rounded-4 bg-black-90 hover:bg-black py-8 px-24 disabled:bg-gray-10 disabled:text-gray",
            "dark:bg-primary dark:bg-primary-[w120]"
        )
        self._applyBtn.setDisabled(True)

        self._footerLayout.addWidget(self._applyBtn)

        self.addWidget(self._menuHeader)
        self.addWidget(self._menuBodyWrapper)
        self.addWidget(self._footer)

    def translateUI(self) -> None:
        super().translateUI()
        self._applyBtn.setText(translator.translate("SELECT_PLAYLIST_SONGS_DIALOG.SAVE_BTN"))

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()
        self._menuBody.songSelected.connect(lambda song: self._selectSong(song))
        self._menuBody.songUnSelected.connect(lambda song: self._unSelectSong(song))
        self._applyBtn.clicked.connect(lambda: self._savePlaylist())
        VisibleObserver(self, delay=10).visible.connect(lambda: self._menuBody.showSongs())
        self._menuBody.songsLoaded.connect(lambda: self._menuBody.setSelectedSongs(self.__playlist.getSongs().toList()))

    def _selectSong(self, song: Song) -> None:
        if not self.__selectedSongs.hasSong(song):
            self.__selectedSongs.insert(song)
            self._checkCanSave()

    def _unSelectSong(self, song: Song) -> None:
        if self.__selectedSongs.hasSong(song):
            self.__selectedSongs.remove(song)
            self._checkCanSave()

    def _checkCanSave(self) -> None:
        canSave = self.__playlistSongIds != self.__songIdsOf(self.__selectedSongs.toList())
        self._applyBtn.setDisabled(not canSave)

    def _savePlaylist(self) -> None:
        songs = self.__selectedSongs.toList()
        self.__playlist.getSongs().setSongs(songs)
        self.closeWithAnimation()

    @staticmethod
    def __songIdsOf(songs: list[Song]) -> list[str]:
        return sorted([song.getId() for song in songs])
