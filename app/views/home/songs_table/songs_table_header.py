from typing import Optional

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFileDialog

from app.common.models import Playlist, Song
from app.common.others import appCenter
from app.components.base import Factory, EllipsisLabel, Component
from app.components.dialogs import Dialogs
from app.helpers.others import Files, Logger
from app.helpers.stylesheets import Paddings, Colors
from app.resource.others import FileType
from app.resource.qt import Icons
from app.views.home.songs_table.dialogs.download_songs_dialog import DownloadSongsDialog
from app.views.home.songs_table.dialogs.select_playlist_songs_dialog import SelectPlaylistSongsDialog


class SongsTableHeader(QWidget, Component):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._scrollBarWidth = 4
        self._initComponent()

        self._trackLabel.setText("TRACK")
        self._artistLabel.setText("ARTIST")
        self._lengthLabel.setText("LENGTH")

    def _createUI(self) -> None:
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._mainLayout = QHBoxLayout(self)
        self._mainLayout.setContentsMargins(28, 0, 28 + self._scrollBarWidth, 0)
        self._mainLayout.setSpacing(0)

        self._trackLabel = EllipsisLabel()
        self._trackLabel.setFont(Factory.createFont(size=9))
        self._trackLabel.setFixedWidth(64)
        self._trackLabel.setAlignment(Qt.AlignCenter)
        self._trackLabel.setClassName("text-black dark:text-white")

        self._artistLabel = EllipsisLabel()
        self._artistLabel.setFont(Factory.createFont(size=9))
        self._artistLabel.setClassName("text-black dark:text-white")

        self._lengthLabel = EllipsisLabel()
        self._lengthLabel.setAlignment(Qt.AlignCenter)
        self._lengthLabel.setFont(Factory.createFont(size=9))
        self._lengthLabel.setClassName("text-black dark:text-white")

        self._buttons = QWidget()
        self._buttonsLayout = QHBoxLayout(self._buttons)
        self._buttonsLayout.setAlignment(Qt.AlignLeft)
        self._buttonsLayout.setSpacing(8)
        self._buttonsLayout.setContentsMargins(8, 0, 8, 0)

        self._downloadSongsToLibraryBtn = Factory.createIconButton(Icons.LARGE, Paddings.RELATIVE_50)
        self._downloadSongsToLibraryBtn.setLightModeIcon(Icons.DOWNLOAD.withColor(Colors.PRIMARY))
        self._downloadSongsToLibraryBtn.setDarkModeIcon(Icons.DOWNLOAD.withColor(Colors.WHITE))
        self._downloadSongsToLibraryBtn.setToolTip("Download songs from Youtube.")
        self._downloadSongsToLibraryBtn.setClassName("rounded-full bg-primary-12 hover:bg-primary-25 dark:bg-white-20 dark:hover:bg-white-33")

        self._importSongsToLibraryBtn = Factory.createIconButton(Icons.LARGE, Paddings.RELATIVE_67)
        self._importSongsToLibraryBtn.setLightModeIcon(Icons.ADD.withColor(Colors.PRIMARY))
        self._importSongsToLibraryBtn.setDarkModeIcon(Icons.ADD.withColor(Colors.WHITE))
        self._importSongsToLibraryBtn.setToolTip("Import songs from computer.")
        self._importSongsToLibraryBtn.setClassName("rounded-full bg-primary-12 hover:bg-primary-25 dark:bg-white-20 dark:hover:bg-white-33")

        self._selectSongsToPlaylistBtn = Factory.createIconButton(Icons.LARGE, Paddings.RELATIVE_67)
        self._selectSongsToPlaylistBtn.setLightModeIcon(Icons.EDIT.withColor(Colors.PRIMARY))
        self._selectSongsToPlaylistBtn.setDarkModeIcon(Icons.EDIT.withColor(Colors.WHITE))
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

        self._downloadDialog = DownloadSongsDialog()

    def _connectSignalSlots(self) -> None:
        appCenter.currentPlaylistChanged.connect(lambda playlist: self.__showActionsToPlaylist(playlist))

        self._importSongsToLibraryBtn.clicked.connect(lambda: self._importSongsFromExplorer())
        self._downloadSongsToLibraryBtn.clicked.connect(lambda: self._openDownloadSongDialogs())
        self._selectSongsToPlaylistBtn.clicked.connect(lambda: self._openSelectPlaylistSongsDialog())

    def __showActionsToPlaylist(self, playlist: Playlist) -> None:
        playlistId = playlist.getInfo().getId()
        self._downloadSongsToLibraryBtn.setVisible(playlistId == "library")
        self._importSongsToLibraryBtn.setVisible(playlistId == "library")
        self._selectSongsToPlaylistBtn.setVisible(playlistId not in {"library", "favourites"})

    def _importSongsFromExplorer(self) -> None:
        paths = QFileDialog.getOpenFileNames(self, filter=FileType.AUDIO)[0]
        if paths is not None and len(paths) > 0:
            thread = ImportSongsToLibraryThread(paths)
            thread.finished.connect(lambda result: self.__displayImportSongsResult(result[0], result[1]))
            thread.start()

    @staticmethod
    def __displayImportSongsResult(succeed: bool, totalSongs: int) -> None:
        if succeed:
            if totalSongs > 0:
                Dialogs.info(header="Import successfully", message=f"You have imported {totalSongs} songs\n from explorer successfully.")
            else:
                Dialogs.alert(header="Import failed", message=f"The songs that you are trying to import\n have already been existed.")
        else:
            Dialogs.alert(header="Import failed", message=f"You have imported songs from explorer failed.")

    def _openDownloadSongDialogs(self) -> None:
        self._downloadDialog.show()

    @staticmethod
    def _openSelectPlaylistSongsDialog() -> None:
        dialog = SelectPlaylistSongsDialog(appCenter.currentPlaylist)
        dialog.show()


class ImportSongsToLibraryThread(QThread):
    finished = pyqtSignal(list)

    def __init__(self, songPaths: list[str]) -> None:
        super().__init__()
        self.__songPaths = songPaths

    def run(self) -> None:
        try:
            paths = self.__copySongsToLibrary()
            songs = [Song.fromFile(path) for path in paths]
            appCenter.library.getSongs().insertAll(songs)

            self.finished.emit([True, len(songs)])
        except Exception as e:
            Logger.error(e)
            self.finished.emit([False, 0])

    def __copySongsToLibrary(self) -> list[str]:
        newPaths: list[str] = []
        for path in self.__songPaths:
            try:
                songPath = Files.copyFileToDirectory("library/", path)
                print(f"Import song from '{path}' to library")
                newPaths.append(songPath)
            except FileExistsError:
                Logger.error(f"Copy failed for {path}")
                pass

        return newPaths
