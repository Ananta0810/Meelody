import io
import uuid
from typing import Optional

from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QResizeEvent
from PyQt5.QtWidgets import QWidget, QShortcut, QFileDialog

from app.common.exceptions import StorageException
from app.common.models.playlists import UserPlaylist
from app.common.others import appCenter, translator
from app.components.base import Cover, CoverProps, Factory, Input, ActionButton
from app.components.dialogs import BaseDialog, Dialogs
from app.components.widgets import Box
from app.helpers.base import Strings
from app.helpers.builders import ImageEditor
from app.helpers.others import Files
from app.resource.others import FileType
from app.resource.qt import Images


class NewPlaylistDialog(BaseDialog):

    def __init__(self):
        self.__coverData: Optional[bytes] = None

        super().__init__()
        super()._initComponent()
        self.applyTheme()

    def _createUI(self) -> None:
        super()._createUI()

        self._cover = Cover()
        self._cover.setFixedSize(320, 320)
        self._cover.setCover(CoverProps.fromBytes(Images.DEFAULT_PLAYLIST_COVER, 320, 320, radius=16))

        self._titleInput = Input()
        self._titleInput.setFont(Factory.createFont(size=12))
        self._titleInput.setFixedSize(320, 48)
        self._titleInput.setClassName(
            "px-12 rounded-4 border border-primary-12 bg-primary-4 text-black",
            "dark:border dark:border-white-[b33] dark:bg-white-12 dark:text-white"
        )
        self._titleInput.setPlaceholderText("Name...")

        self._acceptBtn = ActionButton()
        self._acceptBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=10))
        self._acceptBtn.setClassName("text-white rounded-4 bg-primary-75 bg-primary py-8 disabled:bg-gray-10 disabled:text-gray")
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

    def _translateUI(self) -> None:
        self._acceptBtn.setText(translator.translate("PLAYLIST_CAROUSEL.NEW_PLAYLIST.ACCEPT_BTN"))
        self._editCoverBtn.setText(translator.translate("PLAYLIST_CAROUSEL.NEW_PLAYLIST.CHOOSE_COVER_BTN"))

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()
        self._acceptBtn.clicked.connect(lambda: self._addPlaylist())
        self._editCoverBtn.clicked.connect(lambda: self.__onclickSelectCover())
        self._titleInput.changed.connect(lambda title: self.__checkValid())

    def _assignShortcuts(self) -> None:
        super()._assignShortcuts()
        acceptShortcut = QShortcut(QKeySequence(Qt.Key_Return), self._acceptBtn)
        acceptShortcut.activated.connect(self._acceptBtn.click)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        margin = self._mainView.contentsMargins()
        self._editCoverBtn.move(
            self._cover.x() + self._cover.width() - self._editCoverBtn.width() - 8 + margin.right(),
            self._cover.y() + 8 + margin.top(),
        )

    def __checkValid(self) -> None:
        titleValid = 3 <= len(self._titleInput.text().strip()) <= 64

        self._acceptBtn.setDisabled(not titleValid)

    def __onclickSelectCover(self) -> None:
        path = QFileDialog.getOpenFileName(self, filter=FileType.IMAGE)[0]

        if Strings.isBlank(path):
            return

        imageEditor = ImageEditor.ofFile(path)
        cover = imageEditor.square().resize(320, 320).toBytes()

        self.__coverData = cover
        self._cover.setCover(CoverProps.fromBytes(cover, 320, 320, radius=16))

    def _addPlaylist(self) -> None:
        id = str(uuid.uuid4())
        name = self._titleInput.text().strip()
        path = f"configuration/playlists/{id}.png"
        cover = self.__coverData

        try:
            if cover is not None:
                Files.createDirectoryIfNotExisted("configuration/playlists")
                image = Image.open(io.BytesIO(cover))
                image.save(f"configuration/playlists/{id}.png")

            playlist = UserPlaylist(UserPlaylist.Info(name=name, cover=cover, id=id, coverPath=path), UserPlaylist.Songs())
            appCenter.playlists.append(playlist)
            self.close()
        except StorageException:
            if cover is not None:
                Files.removeFile(path)

            Dialogs.alert(
                header="Save playlist failed",
                message='Something wrong while creating your playlist. Please try to create playlist again.',
                acceptText="Ok",
                onAccept=lambda: self.close()
            )
