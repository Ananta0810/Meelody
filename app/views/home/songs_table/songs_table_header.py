from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFileDialog

from app.components.base import Factory, EllipsisLabel, Component
from app.helpers.stylesheets import Paddings, Colors
from app.resource.qt import Icons
from app.views.home.songs_table.dialogs.download_songs_dialog import DownloadSongsDialog
from app.views.threads import ImportSongsToLibraryThread


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

        self._addSongsToLibraryBtn = Factory.createIconButton(Icons.LARGE, Paddings.RELATIVE_67)
        self._addSongsToLibraryBtn.setLightModeIcon(Icons.ADD.withColor(Colors.PRIMARY))
        self._addSongsToLibraryBtn.setDarkModeIcon(Icons.ADD.withColor(Colors.WHITE))
        self._addSongsToLibraryBtn.setToolTip("Import songs from computer.")
        self._addSongsToLibraryBtn.setClassName("rounded-full bg-primary-12 hover:bg-primary-25 dark:bg-white-20 dark:hover:bg-white-33")

        self._selectSongsBtn = Factory.createIconButton(Icons.LARGE, Paddings.RELATIVE_67)
        self._selectSongsBtn.setLightModeIcon(Icons.EDIT.withColor(Colors.PRIMARY))
        self._selectSongsBtn.setDarkModeIcon(Icons.EDIT.withColor(Colors.WHITE))
        self._selectSongsBtn.setToolTip("Select playlist songs.")
        self._selectSongsBtn.setClassName("rounded-full bg-primary-12 hover:bg-primary-25 dark:bg-white-20 dark:hover:bg-white-33")
        self._selectSongsBtn.hide()

        self._applyAddSongsBtn = Factory.createIconButton(Icons.LARGE, Paddings.RELATIVE_50)
        self._applyAddSongsBtn.setLightModeIcon(Icons.APPLY.withColor(Colors.PRIMARY))
        self._applyAddSongsBtn.setDarkModeIcon(Icons.APPLY.withColor(Colors.WHITE))
        self._applyAddSongsBtn.setToolTip("Apply selecting playlist songs.")
        self._applyAddSongsBtn.setClassName("rounded-full bg-primary-12 hover:bg-primary-25 dark:bg-white-20 dark:hover:bg-white-33")
        self._applyAddSongsBtn.hide()

        self._buttonsLayout.addWidget(self._downloadSongsToLibraryBtn)
        self._buttonsLayout.addWidget(self._addSongsToLibraryBtn)
        self._buttonsLayout.addWidget(self._selectSongsBtn)
        self._buttonsLayout.addWidget(self._applyAddSongsBtn)

        self._mainLayout.addWidget(self._trackLabel)
        self._mainLayout.addSpacing(237)
        self._mainLayout.addWidget(self._artistLabel)
        self._mainLayout.addSpacing(114)
        self._mainLayout.addWidget(self._lengthLabel)
        self._mainLayout.addStretch()
        self._mainLayout.addWidget(self._buttons)

    def _connectSignalSlots(self) -> None:
        self._addSongsToLibraryBtn.clicked.connect(lambda: self._addSongToLibrary())
        self._downloadSongsToLibraryBtn.clicked.connect(lambda: self._openDownloadSongDialogs())

    def _addSongToLibrary(self) -> None:
        paths = QFileDialog.getOpenFileNames(self, filter="MP3 (*.MP3 *.mp3)")[0]
        if paths is not None and len(paths) > 0:
            ImportSongsToLibraryThread(paths).start()

    def _openDownloadSongDialogs(self) -> None:
        downloadDialog = DownloadSongsDialog()
        downloadDialog.show()
