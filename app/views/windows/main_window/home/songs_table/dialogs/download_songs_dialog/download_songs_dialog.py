import os
from urllib.error import URLError

from PyQt5.QtCore import Qt, pyqtSignal, pyqtBoundSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut, QWidget, QVBoxLayout
from pytube import YouTube
from pytube.exceptions import RegexMatchError

from app.common.models import Song
from app.common.others import appCenter, translator
from app.common.statics.qt import Images, Cursors
from app.components.base import FontFactory
from app.components.buttons import ActionButton
from app.components.dialogs import BaseDialog, Dialogs
from app.components.images import Cover
from app.components.inputs import Input
from app.components.labels import Label
from app.utils.base import Strings
from app.utils.others import Logger
from app.views.windows.main_window.home.songs_table.dialogs.download_songs_dialog.download_songs_menu import DownloadSongsMenu


class DownloadSongsDialog(BaseDialog):

    def __init__(self):
        super().__init__()
        super()._initComponent()

    def _createUI(self) -> None:
        super()._createUI()

        self._image = Cover()
        self._image.setAlignment(Qt.AlignHCenter)
        self._image.setFixedHeight(156)
        self._image.setCover(Cover.Props.fromBytes(Images.download, width=128))

        self._header = Label()
        self._header.setFont(FontFactory.create(family="Segoe UI Semibold", size=16, bold=True))
        self._header.setAlignment(Qt.AlignCenter)
        self._header.setClassName("text-black dark:text-white")

        self._input = Input()
        self._input.setFont(FontFactory.create(size=12))
        self._input.setFixedHeight(48)
        self._input.setClassName(
            "px-12 rounded-4 border border-primary-12 bg-primary-4 disabled:bg-none disabled:border-none disabled:text-black",
            "dark:border-white-[b33] dark:bg-white-12 dark:text-white dark:disabled:text-white",
        )

        self._searchBtn = ActionButton()
        self._searchBtn.setFont(FontFactory.create(family="Segoe UI Semibold", size=10))
        self._searchBtn.setClassName("text-white rounded-4 bg-primary hover:bg-primary-[w125] py-8")

        self._menu = DownloadSongsMenu()
        self._menu.setClassName("scroll/bg-primary-75 scroll/hover:bg-primary scroll/rounded-2")

        self._mainView = QWidget()
        self._mainView.setFixedWidth(640)
        self._mainView.setContentsMargins(12, 4, 12, 0)

        self._viewLayout = QVBoxLayout(self._mainView)
        self._viewLayout.setSpacing(0)
        self._viewLayout.setContentsMargins(0, 0, 0, 0)

        self._viewLayout.addWidget(self._image)
        self._viewLayout.addWidget(self._header)
        self._viewLayout.addSpacing(12)
        self._viewLayout.addWidget(self._input)
        self._viewLayout.addSpacing(8)
        self._viewLayout.addWidget(self._searchBtn)
        self._viewLayout.addSpacing(12)
        self._viewLayout.addWidget(self._menu)

        self.addWidget(self._mainView)

    def translateUI(self) -> None:
        super().translateUI()
        self._searchBtn.setToolTip("(Enter)")
        self._header.setText(translator.translate("DOWNLOAD_DIALOG.LABEL"))
        self._input.setPlaceholderText(translator.translate("DOWNLOAD_DIALOG.PLACE_HOLDER"))
        self._searchBtn.setText(translator.translate("DOWNLOAD_DIALOG.SEARCH_BTN"))

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()
        self._searchBtn.clicked.connect(lambda: self.__searchSong())

    def _assignShortcuts(self) -> None:
        super()._assignShortcuts()
        acceptShortcut = QShortcut(QKeySequence(Qt.Key_Return), self._searchBtn)
        acceptShortcut.activated.connect(lambda: self._searchBtn.click())

    def show(self) -> None:
        self._input.clear()
        self._searchBtn.setCursor(Cursors.pointer)
        super().show()
        self.applyTheme()

    def __searchSong(self) -> None:
        self._searchBtn.setCursor(Cursors.waiting)

        try:
            ytb = YouTube(self._input.text().strip())
            dialog = _SongInfoDialog(ytb)
            dialog.acceptDownload.connect(lambda yt, title, artist: self.__downloadSong(yt, title, artist))
            dialog.show()
        except RegexMatchError:
            Dialogs.alert(message=translator.translate("DOWNLOAD_DIALOG.INVALID_URL"))
        except URLError:
            Dialogs.alert(message=translator.translate("DOWNLOAD_DIALOG.NO_INTERNET"))
        except Exception as e:
            Logger.error(e)
            Dialogs.alert(message=translator.translate("DOWNLOAD_DIALOG.VIDEO_NOT_FOUND"))

        self._searchBtn.setCursor(Cursors.pointer)

    def __downloadSong(self, ytb: YouTube, title: str, artist: str) -> None:
        try:
            item = self._menu.addItem()
            item.download(ytb, title, artist)
            item.songDownloaded.connect(lambda songLocation: self.__insertSongToLibrary(songLocation))
        except Exception as e:
            print(e)

    @staticmethod
    def __insertSongToLibrary(path: str) -> None:
        try:
            appCenter.library.getSongs().insert(Song.fromFile(path, Strings.getFileBasename(path)))
        except:
            Dialogs.alert(message=translator.translate("DOWNLOAD_DIALOG.INSERT_FAILED"))


class _SongInfoDialog(BaseDialog):
    acceptDownload: pyqtBoundSignal = pyqtSignal(YouTube, str, str)

    def __init__(self, youtube: YouTube) -> None:
        self.__ytb = youtube
        self.__canUpdate: bool = False

        super().__init__()
        super()._initComponent()

        self._titleInput.setText(youtube.title)
        self._artistInput.setText(youtube.author)
        self.__checkValid()

    def _createUI(self) -> None:
        super()._createUI()

        self._image = Cover()
        self._image.setAlignment(Qt.AlignHCenter)
        self._image.setCover(Cover.Props.fromBytes(Images.download, width=128))

        self._header = Label()
        self._header.setFont(FontFactory.create(family="Segoe UI Semibold", size=16, bold=True))
        self._header.setClassName("text-black dark:text-white bg-none")
        self._header.setAlignment(Qt.AlignCenter)

        self._titleLabel = Label()
        self._titleLabel.setFont(FontFactory.create(size=11))
        self._titleLabel.setClassName("text-black dark:text-white bg-none")

        self._titleErrorLabel = Label()
        self._titleErrorLabel.setFont(FontFactory.create(size=11))
        self._titleErrorLabel.setClassName("text-danger bg-none")
        self._titleErrorLabel.hide()

        self._titleInput = Input()
        self._titleInput.setFont(FontFactory.create(size=12))
        self._titleInput.setClassName(
            "px-12 py-8 rounded-4 border border-primary-12 bg-primary-4 disabled:bg-none disabled:border-none disabled:text-black",
            "dark:border-white-[b33] dark:bg-white-12 dark:text-white dark:disabled:text-white",
        )

        self._artistLabel = Label()
        self._artistLabel.setFont(FontFactory.create(size=11))
        self._artistLabel.setClassName("text-black dark:text-white bg-none")

        self._artistInput = Input()
        self._artistInput.setFont(FontFactory.create(size=12))
        self._artistInput.setClassName(
            "px-12 py-8 rounded-4 border border-primary-12 bg-primary-4 disabled:bg-none disabled:border-none disabled:text-black",
            "dark:border-white-[b33] dark:bg-white-12 dark:text-white dark:disabled:text-white",
        )

        self._artistErrorLabel = Label()
        self._artistErrorLabel.setFont(FontFactory.create(size=11))
        self._artistErrorLabel.setClassName("text-danger bg-none")
        self._artistErrorLabel.hide()

        self._acceptBtn = ActionButton()
        self._acceptBtn.setFont(FontFactory.create(family="Segoe UI Semibold", size=11))
        self._acceptBtn.setClassName("text-white rounded-4 bg-primary-75 bg-primary py-8 disabled:bg-gray-10 disabled:text-gray")

        self._mainView = QWidget()
        self._mainView.setFixedWidth(480)
        self._mainView.setContentsMargins(12, 4, 12, 12)

        self._viewLayout = QVBoxLayout(self._mainView)
        self._viewLayout.setSpacing(8)
        self._viewLayout.setContentsMargins(0, 0, 0, 0)
        self._viewLayout.addWidget(self._image)
        self._viewLayout.addWidget(self._header)
        self._viewLayout.addWidget(self._titleLabel)
        self._viewLayout.addWidget(self._titleInput)
        self._viewLayout.addWidget(self._titleErrorLabel)
        self._viewLayout.addWidget(self._artistLabel)
        self._viewLayout.addWidget(self._artistInput)
        self._viewLayout.addWidget(self._artistErrorLabel)
        self._viewLayout.addWidget(self._acceptBtn)

        self.addWidget(self._mainView)

    def translateUI(self) -> None:
        super().translateUI()
        self._acceptBtn.setToolTip("(Enter)")
        self._header.setText(translator.translate("DOWNLOAD_DIALOG.LABEL"))
        self._acceptBtn.setText(translator.translate("DOWNLOAD_DIALOG.DOWNLOAD_BTN"))
        self._artistLabel.setText(translator.translate("SONG.TITLE"))
        self._titleLabel.setText(translator.translate("SONG.ARTIST"))

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()

        self._titleInput.changed.connect(lambda text: self.__checkValid())
        self._artistInput.changed.connect(lambda text: self.__checkValid())
        self._acceptBtn.clicked.connect(lambda: self._download())

    def _assignShortcuts(self) -> None:
        super()._assignShortcuts()
        acceptShortcut = QShortcut(QKeySequence(Qt.Key_Return), self._acceptBtn)
        acceptShortcut.activated.connect(lambda: self._acceptBtn.click())

    def __checkValid(self) -> None:
        self.__canUpdate = self.__validateTitle() and self.__validateArtist()
        self._acceptBtn.setDisabled(not self.__canUpdate)

    def __validateTitle(self) -> bool:
        title = self._titleInput.text().strip()

        if Strings.isBlank(title):
            self._titleErrorLabel.show()
            self._titleErrorLabel.setText(translator.translate("SONG.VALIDATE.TITLE_BLANK"))
            return False

        if len(title) > 128:
            self._titleErrorLabel.show()
            self._titleErrorLabel.setText(translator.translate("SONG.VALIDATE.TITLE_LENGTH"))
            return False

        if os.path.exists(f"library/{Strings.sanitizeFileName(title)}.mp3"):
            self._titleErrorLabel.show()
            self._titleErrorLabel.setText(translator.translate("SONG.VALIDATE.TITLE_EXISTED"))
            return False

        self._titleErrorLabel.hide()
        return True

    def __validateArtist(self) -> bool:
        artist = self._artistInput.text().strip()
        if len(artist) > 64:
            self._artistErrorLabel.show()
            self._artistErrorLabel.setText(translator.translate("SONG.VALIDATE.ARTIST_LENGTH"))
            return False

        self._artistErrorLabel.hide()
        return True

    def _download(self) -> None:
        self.__checkValid()
        if not self.__canUpdate:
            return

        title = self._titleInput.text().strip()
        artist = self._artistInput.text().strip()

        self.acceptDownload.emit(self.__ytb, title, artist)
        self.closeWithAnimation()

    def show(self) -> None:
        self.moveToCenter()
        self.applyTheme()
        super().show()
