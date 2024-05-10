from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from app.components.base import ActionButton, Factory, Cover, CoverProps, Label
from app.components.dialogs import BaseDialog
from app.resource.qt import Images
from app.views.home.songs_table.dialogs.import_songs_dialog.import_song_item import ImportSongItem
from app.views.home.songs_table.dialogs.import_songs_dialog.import_songs_menu import ImportSongsMenu


class ImportSongsDialog(BaseDialog):
    importDone = pyqtSignal()

    def __init__(self, paths: list[str]):
        super().__init__()

        self.__importedItems: set[str] = set()
        self.__paths: list[str] = paths

        self._initComponent()

    def _createUI(self) -> None:
        super()._createUI()
        self._hideTitleBar()

        self._image = Cover()
        self._image.setAlignment(Qt.AlignHCenter)
        self._image.setFixedHeight(156)
        self._image.setCover(CoverProps.fromBytes(Images.IMPORT_SONGS, width=128))

        self._header = Label()
        self._header.setFont(Factory.createFont(family="Segoe UI Semibold", size=16, bold=True))
        self._header.setAlignment(Qt.AlignCenter)
        self._header.setText("Import Songs")
        self._header.setClassName("text-black dark:text-white")

        self._menu = ImportSongsMenu()
        self._menu.setClassName("scroll/bg-primary-75 scroll/hover:bg-primary scroll/rounded-2")

        self._closeBtn = ActionButton()
        self._closeBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=10))
        self._closeBtn.setClassName("text-white rounded-4 bg-black-[w80] hover:bg-black py-8")
        self._closeBtn.setText("Close")
        self._closeBtn.hide()

        self._mainView = QWidget()
        self._mainView.setFixedWidth(640)
        self._mainView.setContentsMargins(12, 4, 12, 8)

        self._viewLayout = QVBoxLayout(self._mainView)
        self._viewLayout.setSpacing(0)
        self._viewLayout.setContentsMargins(0, 0, 0, 0)

        self._viewLayout.addSpacing(32)
        self._viewLayout.addWidget(self._image)
        self._viewLayout.addWidget(self._header)
        self._viewLayout.addSpacing(12)
        self._viewLayout.addWidget(self._menu)
        self._viewLayout.addSpacing(12)
        self._viewLayout.addWidget(self._closeBtn)

        self.addWidget(self._mainView)

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()

        self._closeBtn.clicked.connect(lambda: self.close())

        self.importDone.connect(lambda: self._closeBtn.show())
        self.importDone.connect(lambda: self.__importSongsToLibrary())

    def _assignShortcuts(self) -> None:
        pass

    def show(self) -> None:
        super().show()
        self.applyTheme()
        self._showImportFiles()

    def _showImportFiles(self) -> None:
        self._menu.addItems(self.__paths)
        #
        # timer = QTimer(self)
        # timer.timeout.connect(lambda: self.__startImportAll())
        # timer.start(10)

    def __startImportAll(self):
        for item in self._menu.items():
            self.startImport(item)

    def startImport(self, item: ImportSongItem) -> None:
        item.songImportedSucceed.connect(lambda songPath: self.__addSong(songPath))
        item.songImportedFailed.connect(lambda: self.__markImported(item))
        item.startImport()

    def __markImported(self, item: ImportSongItem) -> None:
        path = item.path()
        self.__importedItems.add(path)

        # if len(self.__importedItems) >= len(self.__paths):
        #     self.importDone.emit()

    def __importSongsToLibrary(self) -> None:
        pass
        # songs = [Song.fromFile(songPath, Strings.getFileBasename(songPath)) for songPath in self.__importedItems]
        # appCenter.library.getSongs().insertAll(songs)
