from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QShortcut

from app.common.exceptions import ResourceException
from app.common.models import Song
from app.components.base import Cover, CoverProps, Factory, ActionButton, Label, Input
from app.components.dialogs import BaseDialog, Dialogs
from app.components.widgets import Box
from app.helpers.base import Strings
from app.helpers.others import Logger
from app.resource.qt import Images


class UpdateSongDialog(BaseDialog):

    def __init__(self, song: Song) -> None:
        self.__canUpdate = False
        self.__song = song

        super().__init__()
        super()._initComponent()

        self._titleInput.setText(song.getTitle())
        self._artistInput.setText(song.getArtist())

    def _createUI(self) -> None:
        super()._createUI()

        self._image = Cover()
        self._image.setAlignment(Qt.AlignHCenter)
        self._image.setDefaultCover(CoverProps.fromBytes(Images.EDIT, width=128))

        self._header = Label()
        self._header.setFont(Factory.createFont(family="Segoe UI Semibold", size=16, bold=True))
        self._header.setClassName("text-black dark:text-white bg-none")
        self._header.setAlignment(Qt.AlignCenter)
        self._header.setText("Update Song")

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
        self._acceptBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=10))
        self._acceptBtn.setClassName("text-white rounded-4 bg-primary-75 bg-primary py-8 disabled:bg-gray-10 disabled:text-gray")
        self._acceptBtn.setText("Apply")
        self._acceptBtn.setDisabled(True)

        self._mainView = QWidget()
        self._mainView.setContentsMargins(12, 4, 12, 12)

        self._viewLayout = Box(self._mainView)
        self._viewLayout.setSpacing(8)
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

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()

        self._titleInput.changed.connect(lambda text: self.__checkValid())
        self._artistInput.changed.connect(lambda text: self.__checkValid())
        self._acceptBtn.clicked.connect(lambda: self._updateSong())

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

        if Strings.equals(self.__song.getTitle(), title) and Strings.equals(self.__song.getArtist(), artist):
            self.__canUpdate = False
            self._acceptBtn.setDisabled(True)
            return

        self.__canUpdate = True
        self._acceptBtn.setDisabled(False)

    def _updateSong(self) -> None:
        self.__checkValid()
        if not self.__canUpdate:
            return

        title = self._titleInput.text().strip()
        artist = self._artistInput.text().strip()

        try:
            self.__song.updateInfo(title, artist)
            Dialogs.success(message="Update song information successfully.")
            Logger.info("Update song info succeed.")
            self.close()
        except ResourceException as e:
            if e.isNotFound():
                Dialogs.alert(message="Song is not found in library, you might have deleted it while open our application.")
                self.close()
            if e.isBeingUsed():
                Dialogs.alert(message="You can not change info of the playing song. Please try again after you played other song.")
                self.close()
            if e.isExisted():
                Dialogs.alert(message="Song file have already existed. Please try with other title.")
        except Exception as e:
            Logger.error(e)
            Logger.error("Update song infor failed.")
            Dialogs.alert(message="Something is wrong when saving the song. Please try again.")
            self.close()
