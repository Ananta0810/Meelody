from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFileDialog

from app.common.models import Playlist
from app.common.models.database import Library
from app.common.models.playlists import FavouritesPlaylist
from app.common.others import appCenter
from app.common.statics.enums import FileType
from app.common.statics.qt import Icons, Cursors
from app.common.statics.styles import Colors
from app.common.statics.styles import Paddings
from app.components.base import Component, FontFactory
from app.components.buttons import ButtonFactory
from app.components.labels import Label
from app.views.windows.main_window.home.songs_table.dialogs.download_songs_dialog import DownloadSongsDialog
from app.views.windows.main_window.home.songs_table.dialogs.import_songs_dialog import ImportSongsDialog
from app.views.windows.main_window.home.songs_table.dialogs.select_playlist_songs_dialog import SelectPlaylistSongsDialog


class SongsTableHeader(QWidget, Component):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._scrollBarWidth = 4
        self._initComponent()

    def _createUI(self) -> None:
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._mainLayout = QHBoxLayout(self)
        self._mainLayout.setContentsMargins(28, 0, 28 + self._scrollBarWidth, 0)
        self._mainLayout.setSpacing(0)

        self._trackLabel = Label()
        self._trackLabel.setFont(FontFactory.create(size=9))
        self._trackLabel.setFixedWidth(64)
        self._trackLabel.setAlignment(Qt.AlignCenter)
        self._trackLabel.setClassName("text-black dark:text-white")

        self._artistLabel = Label()
        self._artistLabel.setFont(FontFactory.create(size=9))
        self._artistLabel.setClassName("text-black dark:text-white")

        self._lengthLabel = Label()
        self._lengthLabel.setAlignment(Qt.AlignCenter)
        self._lengthLabel.setFont(FontFactory.create(size=9))
        self._lengthLabel.setClassName("text-black dark:text-white")

        self._buttons = QWidget()
        self._buttonsLayout = QHBoxLayout(self._buttons)
        self._buttonsLayout.setAlignment(Qt.AlignLeft)
        self._buttonsLayout.setSpacing(8)
        self._buttonsLayout.setContentsMargins(8, 0, 8, 0)

        self._downloadSongsToLibraryBtn = ButtonFactory.createIconButton(Icons.large, Paddings.relative50)
        self._downloadSongsToLibraryBtn.setLightModeIcon(Icons.download.withColor(Colors.primary))
        self._downloadSongsToLibraryBtn.setDarkModeIcon(Icons.download.withColor(Colors.white))
        self._downloadSongsToLibraryBtn.setToolTip("Download songs from Youtube.")
        self._downloadSongsToLibraryBtn.setClassName("rounded-full bg-primary-12 hover:bg-primary-25 dark:bg-white-20 dark:hover:bg-white-33")

        self._importSongsToLibraryBtn = ButtonFactory.createIconButton(Icons.large, Paddings.relative67)
        self._importSongsToLibraryBtn.setLightModeIcon(Icons.add.withColor(Colors.primary))
        self._importSongsToLibraryBtn.setDarkModeIcon(Icons.add.withColor(Colors.white))
        self._importSongsToLibraryBtn.setToolTip("Import songs from computer.")
        self._importSongsToLibraryBtn.setClassName("rounded-full bg-primary-12 hover:bg-primary-25 dark:bg-white-20 dark:hover:bg-white-33")

        self._selectSongsToPlaylistBtn = ButtonFactory.createIconButton(Icons.large, Paddings.relative67)
        self._selectSongsToPlaylistBtn.setLightModeIcon(Icons.edit.withColor(Colors.primary))
        self._selectSongsToPlaylistBtn.setDarkModeIcon(Icons.edit.withColor(Colors.white))
        self._selectSongsToPlaylistBtn.setToolTip("Select playlist songs.")
        self._selectSongsToPlaylistBtn.setClassName("rounded-full bg-primary-12 hover:bg-primary-25 dark:bg-white-20 dark:hover:bg-white-33")
        self._selectSongsToPlaylistBtn.hide()

        self._buttonsLayout.addWidget(self._downloadSongsToLibraryBtn)
        self._buttonsLayout.addWidget(self._importSongsToLibraryBtn)
        self._buttonsLayout.addWidget(self._selectSongsToPlaylistBtn)

        self._mainLayout.addWidget(self._trackLabel)
        self._mainLayout.addSpacing(237)
        self._mainLayout.addWidget(self._artistLabel)
        self._mainLayout.addSpacing(114)
        self._mainLayout.addWidget(self._lengthLabel)
        self._mainLayout.addStretch()
        self._mainLayout.addWidget(self._buttons)

        self._downloadDialog = None

    def translateUI(self) -> None:
        self._trackLabel.setText(self.translate("SONGS_MENU.HEADER.TRACK"))
        self._artistLabel.setText(self.translate("SONGS_MENU.HEADER.ARTIST"))
        self._lengthLabel.setText(self.translate("SONGS_MENU.HEADER.LENGTH"))
        self._downloadSongsToLibraryBtn.setToolTip(self.translate("SONGS_MENU.HEADER.DOWNLOAD_BTN"))
        self._importSongsToLibraryBtn.setToolTip(self.translate("SONGS_MENU.HEADER.IMPORT_BTN"))
        self._selectSongsToPlaylistBtn.setToolTip(self.translate("SONGS_MENU.HEADER.UPDATE_PLAYLIST_BTN"))

    def _connectSignalSlots(self) -> None:
        appCenter.currentPlaylistChanged.connect(lambda playlist: self.__showActionsToPlaylist(playlist))

        self._importSongsToLibraryBtn.clicked.connect(lambda: self._importSongsFromExplorer())
        self._downloadSongsToLibraryBtn.clicked.connect(lambda: self._openDownloadSongDialogs())
        self._selectSongsToPlaylistBtn.clicked.connect(lambda: self._openSelectPlaylistSongsDialog())

    def __showActionsToPlaylist(self, playlist: Playlist) -> None:
        libraryId = Library().getInfo().getId()
        favouriteId = FavouritesPlaylist.Info().getId()

        playlistId = playlist.getInfo().getId()
        self._downloadSongsToLibraryBtn.setVisible(playlistId == libraryId)
        self._importSongsToLibraryBtn.setVisible(playlistId == libraryId)

        self._selectSongsToPlaylistBtn.setVisible(playlistId not in {libraryId, favouriteId})

    def _importSongsFromExplorer(self) -> None:
        paths = QFileDialog.getOpenFileNames(self, filter=FileType.audio)[0]
        if paths is not None and len(paths) > 0:
            dialog = ImportSongsDialog(paths)
            dialog.show()

    def _openDownloadSongDialogs(self) -> None:
        if self._downloadDialog is None:
            self._downloadDialog = DownloadSongsDialog()
        self._downloadDialog.show()

    def _openSelectPlaylistSongsDialog(self) -> None:
        self._selectSongsToPlaylistBtn.setCursor(Cursors.waiting)
        dialog = SelectPlaylistSongsDialog(appCenter.currentPlaylist)
        dialog.show()
        self._selectSongsToPlaylistBtn.setCursor(Cursors.pointer)
