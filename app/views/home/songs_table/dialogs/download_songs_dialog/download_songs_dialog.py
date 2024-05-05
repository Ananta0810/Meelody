from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut, QWidget, QVBoxLayout
from pytube import YouTube
from pytube.exceptions import RegexMatchError

from app.common.models import Song
from app.common.others import appCenter
from app.components.base import Cover, LabelWithDefaultText, Factory, Input, ActionButton, CoverProps, Label
from app.components.dialogs import BaseDialog, Dialogs
from app.helpers.base import Strings
from app.resource.qt import Images, Cursors
from app.views.home.songs_table.dialogs.download_songs_dialog.download_songs_menu import DownloadSongsMenu


class DownloadSongsDialog(BaseDialog):

    def __init__(self):
        super().__init__()
        super()._initComponent()

    def _createUI(self) -> None:
        super()._createUI()
        self.setFixedWidth(640)
        self.setContentsMargins(24, 24, 24, 12)

        self._image = Cover()
        self._image.setAlignment(Qt.AlignHCenter)
        self._image.setFixedHeight(156)
        self._image.setCover(CoverProps.fromBytes(Images.DOWNLOAD, width=128))

        self._header = LabelWithDefaultText()
        self._header.setFont(Factory.createFont(family="Segoe UI Semibold", size=16, bold=True))
        self._header.setAlignment(Qt.AlignCenter)
        self._header.setText("Download Youtube Song")
        self._header.setClassName("text-black dark:text-white")

        self._input = Input()
        self._input.setFont(Factory.createFont(size=12))
        self._input.setFixedHeight(48)
        self._input.setPlaceholderText("Enter youtube url...")
        self._input.setClassName("px-12 rounded-4 border border-primary-12 bg-primary-4")

        self._searchBtn = ActionButton()
        self._searchBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=10))
        self._searchBtn.setClassName("text-white rounded-4 bg-primary hover:bg-primary-[w125] py-8")
        self._searchBtn.setText("Search")

        self._menu = DownloadSongsMenu()
        self._menu.setClassName("scroll/bg-primary-50 scroll/hover:bg-primary scroll/rounded-2")
        self._menu.applyTheme()

        self.addWidget(self._image)
        self.addWidget(self._header)
        self.addSpacing(12)
        self.addWidget(self._input)
        self.addSpacing(8)
        self.addWidget(self._searchBtn)
        self.addSpacing(12)
        self.addWidget(self._menu)

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()
        self._searchBtn.clicked.connect(lambda: self.__searchSong())

    def show(self) -> None:
        self.applyTheme()
        self._input.clear()
        self._searchBtn.setCursor(Cursors.HAND)
        super().show()

    def applyLightMode(self) -> None:
        super().applyLightMode()
        super().applyThemeToChildren()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        super().applyThemeToChildren()

    def __searchSong(self) -> None:
        self._searchBtn.setCursor(Cursors.WAITING)

        try:
            ytb = YouTube(self._input.text().strip())
            dialog = SongInfoDialog(ytb)
            dialog.acceptDownload.connect(lambda yt, title, artist: self.__downloadSong(yt, title, artist))
            dialog.show()
        except RegexMatchError as e:
            Dialogs.alert(header="Warning", message="Invalid youtube video url.")
        except Exception as e:
            print(e)
            Dialogs.alert(header="Warning", message="Youtube video is not found.")

        self._searchBtn.setCursor(Cursors.HAND)

    def __downloadSong(self, ytb: YouTube, title: str, artist: str) -> None:
        item = self._menu.addItem()
        item.download(ytb, title, artist)
        item.songDownloaded.connect(lambda song: self.__insertSongToLibrary(song))

    @staticmethod
    def __insertSongToLibrary(song: Song) -> None:
        appCenter.library.getSongs().insert(song)


class SongInfoDialog(BaseDialog):
    acceptDownload = pyqtSignal(YouTube, str, str)

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
        self._image.setCover(CoverProps.fromBytes(Images.DOWNLOAD, width=128))

        self._header = Label()
        self._header.setFont(Factory.createFont(family="Segoe UI Semibold", size=16, bold=True))
        self._header.setClassName("text-black dark:text-white bg-none")
        self._header.setAlignment(Qt.AlignCenter)
        self._header.setText("Download Song")

        self._titleLabel = Label()
        self._titleLabel.setFont(Factory.createFont(size=11))
        self._titleLabel.setClassName("text-black dark:text-white bg-none")
        self._titleLabel.setText("Title")

        self._titleInput = Input()
        self._titleInput.setFont(Factory.createFont(size=12))
        self._titleInput.setClassName("px-12 py-8 rounded-4 border border-primary-12 bg-primary-4")

        self._artistLabel = Label()
        self._artistLabel.setFont(Factory.createFont(size=11))
        self._artistLabel.setClassName("text-black dark:text-white bg-none")
        self._artistLabel.setText("Artist")

        self._artistInput = Input()
        self._artistInput.setFont(Factory.createFont(size=12))
        self._artistInput.setClassName("px-12 py-8 rounded-4 border border-primary-12 bg-primary-4")

        self._acceptBtn = ActionButton()
        self._acceptBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=11))
        self._acceptBtn.setClassName("text-white rounded-4 bg-primary-75 bg-primary py-8 disabled:bg-gray-10 disabled:text-gray")
        self._acceptBtn.setText("Download")

        self._mainView = QWidget()
        self._mainView.setContentsMargins(12, 4, 12, 12)

        self._viewLayout = QVBoxLayout(self._mainView)
        self._viewLayout.setSpacing(8)
        self._viewLayout.setContentsMargins(0, 0, 0, 0)
        self._viewLayout.setAlignment(Qt.AlignVCenter)
        self._viewLayout.addWidget(self._image)
        self._viewLayout.addWidget(self._header)
        self._viewLayout.addWidget(self._titleLabel)
        self._viewLayout.addWidget(self._titleInput)
        self._viewLayout.addWidget(self._artistLabel)
        self._viewLayout.addWidget(self._artistInput)
        self._viewLayout.addWidget(self._acceptBtn)

        self.addWidget(self._mainView)
        self.setFixedWidth(480 + 24 * 2)

    def applyLightMode(self) -> None:
        super().applyLightMode()
        super().applyThemeToChildren()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        super().applyThemeToChildren()

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
        title = self._titleInput.text().strip()
        artist = self._artistInput.text().strip()

        if Strings.isBlank(title) or len(title) > 128 or len(artist) > 64:
            self.__canUpdate = False
            self._acceptBtn.setDisabled(True)
            return

        self.__canUpdate = True
        self._acceptBtn.setDisabled(False)

    def _download(self) -> None:
        self.__checkValid()
        if not self.__canUpdate:
            return

        title = self._titleInput.text().strip()
        artist = self._artistInput.text().strip()

        self.acceptDownload.emit(self.__ytb, title, artist)
        self.close()

    def show(self) -> None:
        self.moveToCenter()
        self.applyTheme()
        super().show()
