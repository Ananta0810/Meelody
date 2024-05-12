from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from app.common.asyncs import ChunksConsumer
from app.common.models import Song
from app.common.others import appCenter, translator
from app.common.statics.qt import Images
from app.components.base import FontFactory
from app.components.buttons import ActionButton
from app.components.dialogs import BaseDialog
from app.components.images import Cover, CoverProps
from app.components.labels import Label
from app.helpers.base import Strings
from app.views.home.songs_table.dialogs.import_songs_dialog.import_song_item import ImportSongItem
from app.views.home.songs_table.dialogs.import_songs_dialog.import_songs_menu import ImportSongsMenu


class ImportSongsDialog(BaseDialog):
    importDone = pyqtSignal()

    def __init__(self, paths: list[str]):
        super().__init__()

        self.__importedItems: set[str] = set()
        self.__succeedSongPaths: set[str] = set()
        self.__paths: list[str] = paths
        self.__done: bool = False

        self._initComponent()

    def _createUI(self) -> None:
        super()._createUI()
        self._hideTitleBar()

        self._image = Cover()
        self._image.setAlignment(Qt.AlignHCenter)
        self._image.setFixedHeight(156)
        self._image.setCover(CoverProps.fromBytes(Images.importSongs, width=128))

        self._header = Label()
        self._header.setFont(FontFactory.create(family="Segoe UI Semibold", size=16, bold=True))
        self._header.setAlignment(Qt.AlignCenter)
        self._header.setClassName("text-black dark:text-white")

        self._menu = ImportSongsMenu()
        self._menu.setClassName("scroll/bg-primary-75 scroll/hover:bg-primary scroll/rounded-2")

        self._closeBtn = ActionButton()
        self._closeBtn.setFont(FontFactory.create(family="Segoe UI Semibold", size=10))
        self._closeBtn.setClassName("text-white rounded-4 bg-black-[w80] hover:bg-black py-8 dark:bg-primary dark:hover:bg-primary-[w120]")
        self._closeBtn.hide()

        self._mainView = QWidget()
        self._mainView.setFixedWidth(720)
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

    def _translateUI(self) -> None:
        self._header.setText(translator.translate("IMPORT_SONGS_DIALOG.LABEL"))
        self._closeBtn.setText(translator.translate("IMPORT_SONGS_DIALOG.CLOSE_BTN"))

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

        timer = QTimer(self)
        timer.timeout.connect(lambda: self._showImportFiles())
        timer.timeout.connect(lambda: timer.stop())
        timer.start(1000 // 30)

    def _showImportFiles(self) -> None:

        if len(self.__paths) <= 6:
            self._menu.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        displayer = ChunksConsumer(items=self.__paths, size=6, parent=self)
        displayer.forEach(lambda path, index: self._menu.addItem(path), delay=10)
        displayer.stopped.connect(lambda: self.__startImportAll())

    def __startImportAll(self):
        for item in self._menu.items():
            self.startImport(item)

    def startImport(self, item: ImportSongItem) -> None:
        item.succeed.connect(lambda songPath: self.__importSuccess(songPath))
        item.imported.connect(lambda: self.__markImported(item))
        item.reImported.connect(lambda songPath: self.__importUpdatedSongToLibrary(songPath))
        item.startImport()

    def __importSuccess(self, songPath: str) -> None:
        self.__succeedSongPaths.add(songPath)

    def __markImported(self, item: ImportSongItem) -> None:
        path = item.path()
        self.__importedItems.add(path)

        if len(self.__importedItems) == len(self.__paths) and not self.__done:
            self.__done = True
            self.importDone.emit()

    def __importSongsToLibrary(self) -> None:
        songs = [Song.fromFile(songPath, Strings.getFileBasename(songPath)) for songPath in self.__succeedSongPaths]
        appCenter.library.getSongs().insertAll(songs)

    @staticmethod
    def __importUpdatedSongToLibrary(songPath: str) -> None:
        song = Song.fromFile(songPath, Strings.getFileBasename(songPath))
        appCenter.library.getSongs().insertAll([song])
