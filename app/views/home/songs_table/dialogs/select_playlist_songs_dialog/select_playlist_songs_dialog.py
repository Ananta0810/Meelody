from PyQt5.QtCore import Qt

from app.common.models import Playlist, Song
from app.components.base import ActionButton, Factory
from app.components.dialogs import BaseDialog
from app.components.widgets import StyleWidget, FlexBox
from app.views.home.songs_table.dialogs.select_playlist_songs_dialog.select_playlist_songs_menu_body import MenuBody
from app.views.home.songs_table.dialogs.select_playlist_songs_dialog.select_playlist_songs_menu_header import MenuHeader


class SelectPlaylistSongsDialog(BaseDialog):

    def __init__(self, playlist: Playlist) -> None:
        self.__playlist: Playlist = playlist
        self.__selectedSongs: Playlist.Songs = playlist.getSongs().clone()
        self.__playlistSongIds: list[str] = self.__songIdsOf(playlist.getSongs().getSongs())

        super().__init__()
        super()._initComponent()

        self._menuBody.setSelectedSongs(playlist.getSongs().getSongs())

    def _createUI(self) -> None:
        super()._createUI()
        self.setContentsMargins(32, 20, 32, 20)

        self._menuHeader = MenuHeader()
        self._menuHeader.setFixedWidth(640)
        self._menuHeader.setContentsMargins(0, 16, 0, 16)
        self._menuHeader.setClassName("bg-gray-4 border border-gray-12 rounded-t-8")

        self._menuBody = MenuBody()
        self._menuBody.setFixedSize(640, 480)
        self._menuBody.setContentsMargins(0, 0, 0, 0)
        self._menuBody.setClassName("scroll/bg-primary-50 scroll/hover:bg-primary scroll/rounded-2 bg-gray-4")

        self._footer = StyleWidget()
        self._footer.setFixedWidth(640)
        self._footer.setClassName("rounded-b-8 border border-gray-12")

        self._footerLayout = FlexBox()
        self._footerLayout.setContentsMargins(8, 8, 8, 8)
        self._footerLayout.setAlignment(Qt.AlignRight)

        self._footer.setLayout(self._footerLayout)

        self._applyBtn = ActionButton()
        self._applyBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=10))
        self._applyBtn.setClassName("text-white rounded-4 bg-black-90 hover:bg-black py-8 px-24 disabled:bg-gray-10 disabled:text-gray")
        self._applyBtn.setMinimumWidth(64)
        self._applyBtn.setText("Save")
        self._applyBtn.setDisabled(True)

        self._footerLayout.addWidget(self._applyBtn)

        self.addWidget(self._menuHeader)
        self.addWidget(self._menuBody)
        self.addWidget(self._footer)

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()
        self._menuBody.songSelected.connect(self._selectSong)
        self._menuBody.songUnSelected.connect(self._unSelectSong)
        self._applyBtn.clicked.connect(self._savePlaylist)

    def applyLightMode(self) -> None:
        super().applyLightMode()
        self.applyThemeToChildren()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        self.applyThemeToChildren()

    def show(self) -> None:
        self.moveToCenter()
        self.applyTheme()
        super().show()

    def _selectSong(self, song: Song) -> None:
        if not self.__selectedSongs.hasSong(song):
            self.__selectedSongs.insert(song)
            self._checkCanSave()

    def _unSelectSong(self, song: Song) -> None:
        if self.__selectedSongs.hasSong(song):
            self.__selectedSongs.removeSong(song)
            self._checkCanSave()

    def _checkCanSave(self) -> None:
        canSave = self.__playlistSongIds != self.__songIdsOf(self.__selectedSongs.getSongs())
        self._applyBtn.setDisabled(not canSave)

    def _savePlaylist(self) -> None:
        songs = self.__selectedSongs.getSongs()
        print(self.__selectedSongs)
        self.__playlist.getSongs().setSongs(songs)
        self.close()

    @staticmethod
    def __songIdsOf(songs: list[Song]) -> list[str]:
        return sorted([song.getId() for song in songs])
