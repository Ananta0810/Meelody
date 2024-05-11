import io
from typing import Optional

from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QResizeEvent
from PyQt5.QtWidgets import QWidget, QShortcut, QFileDialog

from app.common.exceptions import StorageException
from app.common.models import Playlist
from app.common.others import appCenter
from app.components.base import Cover, CoverProps, Factory, Input, ActionButton
from app.components.dialogs import BaseDialog, Dialogs
from app.components.widgets import Box
from app.helpers.base import Strings
from app.helpers.builders import ImageEditor
from app.helpers.others import Files
from app.resource.others import FileType
from app.resource.qt import Images


class UpdatePlaylistDialog(BaseDialog):

    def __init__(self, playlist: Playlist):
        self.__playlist = playlist
        self.__coverData: Optional[bytes] = None

        super().__init__()
        super()._initComponent()

        self._setInfo(playlist.getInfo())
        self.applyTheme()

    def _createUI(self) -> None:
        super()._createUI()

        self._cover = Cover()
        self._cover.setFixedSize(320, 320)
        self._cover.setDefaultCover(CoverProps.fromBytes(Images.DEFAULT_PLAYLIST_COVER, 320, 320, radius=16))

        self._titleInput = Input()
        self._titleInput.setFont(Factory.createFont(size=12))
        self._titleInput.setFixedSize(320, 48)
        self._titleInput.setClassName("px-12 rounded-4 border border-primary-12 bg-primary-4")
        self._titleInput.setPlaceholderText("Name...")

        self._acceptBtn = ActionButton()
        self._acceptBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=10))
        self._acceptBtn.setClassName("text-white rounded-4 bg-primary-75 bg-primary py-8 disabled:bg-gray-10 disabled:text-gray")
        self._acceptBtn.setText("Update Playlist")
        self._acceptBtn.setDisabled(True)

        self._mainView = QWidget()
        self._mainView.setContentsMargins(12, 4, 12, 12)

        self._viewLayout = Box(self._mainView)
        self._viewLayout.setAlignment(Qt.AlignVCenter)
        self._viewLayout.addWidget(self._cover)
        self._viewLayout.addSpacing(8)
        self._viewLayout.addWidget(self._titleInput)
        self._viewLayout.addSpacing(8)
        self._viewLayout.addWidget(self._acceptBtn)

        self.addWidget(self._mainView)

        self._editCoverBtn = ActionButton(self._mainView)
        self._editCoverBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=9))
        self._editCoverBtn.setClassName("text-white rounded-4 bg-primary-75 bg-primary py-8")
        self._editCoverBtn.setText("Choose cover")

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        margin = self._mainView.contentsMargins()
        self._editCoverBtn.move(
            self._cover.x() + self._cover.width() - self._editCoverBtn.width() - 8 + margin.right(),
            self._cover.y() + 8 + margin.top(),
        )

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()
        self._acceptBtn.clicked.connect(lambda: self._savePlaylist())
        self._editCoverBtn.clicked.connect(lambda: self.__selectCover())
        self._titleInput.changed.connect(lambda title: self.__checkValid())

    def _assignShortcuts(self) -> None:
        super()._assignShortcuts()
        acceptShortcut = QShortcut(QKeySequence(Qt.Key_Return), self._acceptBtn)
        acceptShortcut.activated.connect(lambda: self._acceptBtn.click())

    def __checkValid(self) -> None:
        self._acceptBtn.setDisabled(not self.__canUpdate())

    def __canUpdate(self):
        title = self._titleInput.text().strip()
        coverUpdated = self.__coverData is not None
        titleLengthValid = 3 <= len(title) <= 64

        if coverUpdated:
            return titleLengthValid
        else:
            return titleLengthValid and title != self.__playlist.getInfo().getName()

    def __selectCover(self) -> None:
        path = QFileDialog.getOpenFileName(self, filter=FileType.IMAGE)[0]
        if Strings.isBlank(path):
            return

        imageEditor = ImageEditor.ofFile(path)
        cover = imageEditor.square().resize(320, 320).toBytes()

        self.__coverData = cover
        self._cover.setCover(CoverProps.fromBytes(cover, 320, 320, radius=16))
        self.__checkValid()

    def _setInfo(self, info: Playlist.Info) -> None:
        self._titleInput.setText(info.getName())
        self._cover.setCover(CoverProps.fromBytes(info.getCover(), 320, 320, radius=16))

    def _savePlaylist(self) -> None:
        name = self._titleInput.text().strip()
        cover = self.__coverData

        tempPlaylist = self.__playlist.clone()

        try:
            if cover is not None:
                Files.createDirectoryIfNotExisted("configuration/playlists")
                image = Image.open(io.BytesIO(cover))
                image.save(tempPlaylist.getInfo().getCoverPath())
                tempPlaylist.getInfo().setCover(cover)

            if name != self.__playlist.getInfo().getName():
                tempPlaylist.getInfo().setName(name)

            appCenter.playlists.replace(tempPlaylist)
            self.close()
        except StorageException:
            Dialogs.alert(
                header="Save playlist failed",
                message='Something wrong while updating your playlist. Please try to update playlist again.',
                acceptText="Ok",
                onAccept=lambda: self.close()
            )
