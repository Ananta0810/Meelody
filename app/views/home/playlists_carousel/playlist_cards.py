import io
from typing import Optional

from PIL import Image
from PyQt5.QtCore import QEvent, QRect
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFileDialog

from app.common.models import Playlist
from app.common.others import appCenter
from app.components.base import Cover, LabelWithDefaultText, Factory, CoverProps
from app.components.dialogs import Dialogs
from app.components.widgets import ExtendableStyleWidget
from app.helpers.base import Bytes
from app.helpers.others import Files, Logger
from app.helpers.qt import Pixmaps
from app.helpers.stylesheets import Paddings, Colors
from app.resource.others import FileType
from app.resource.qt import Cursors, Images, Icons
from app.views.home.playlists_carousel.update_playlist_dialog import UpdatePlaylistDialog


class PlaylistCard(ExtendableStyleWidget):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

    def _createUI(self) -> None:
        self.setFixedSize(256, 320)
        self.setCursor(Cursors.HAND)

        self._mainLayout = QVBoxLayout(self)
        self._mainLayout.setContentsMargins(20, 20, 20, 20)
        self._cover = Cover(self)
        self._cover.setDefaultCover(self._toCoverProps(Images.DEFAULT_PLAYLIST_COVER))
        self._cover.setAnimation(duration=250, start=1.0, end=1.1, onValueChanged=self._cover.zoom)

        self._title = LabelWithDefaultText(autoChangeTheme=False)
        self._title.enableEllipsis()
        self._title.setFixedWidth(320)
        self._title.setFont(Factory.createFont(size=16, bold=True))
        self._title.setClassName("text-black dark:text-white")

        self._mainLayout.addStretch()
        self._mainLayout.addWidget(self._title)

    def setInfo(self, info: Playlist.Info) -> None:
        self._title.setText(info.getName())
        self.setCover(info.getCover())

    def setCover(self, data: bytes) -> None:
        cover = self._toCoverProps(data)
        self._cover.setCover(self._toCoverProps(data))

        if cover is None:
            return

        self._adaptTitleColorToCover()

    def _adaptTitleColorToCover(self):
        coverRect = QRect(self._cover.pos().x(), self._cover.pos().y(), self._cover.rect().width() // 2, self._cover.rect().height())
        mainColor = Pixmaps.getDominantColorAt(coverRect, of=self._cover.currentCover().content())
        if mainColor.isDarkColor():
            self._title.applyDarkMode()
        else:
            self._title.applyLightMode()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self._cover.setFixedSize(self.size())
        return super().resizeEvent(event)

    def enterEvent(self, event: QEvent) -> None:
        super().enterEvent(event)
        self._cover.animationOnEnteredHover()

    def leaveEvent(self, event: QEvent) -> None:
        super().leaveEvent(event)
        self._cover.animationOnLeftHover()

    @staticmethod
    def _toCoverProps(cover: bytes) -> CoverProps:
        return CoverProps.fromBytes(cover, width=256, height=320, radius=24)


class LibraryPlaylistCard(PlaylistCard):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        super()._initComponent()
        self._title.setText("Library")
        super().setCover(Images.DEFAULT_PLAYLIST_COVER)


class FavouritePlaylistCard(PlaylistCard):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        super()._initComponent()

        self.__coverPath = "configuration/playlists/favourite-cover.png"
        super().setCover(Bytes.fromFile(self.__coverPath))

    def _createUI(self) -> None:
        super()._createUI()

        self._title.setText("Favourite")

        self._editCoverBtn = Factory.createIconButton(size=Icons.MEDIUM, padding=Paddings.RELATIVE_50)
        self._editCoverBtn.setLightModeIcon(Icons.IMAGE.withColor(Colors.WHITE))
        self._editCoverBtn.setClassName("rounded-full bg-primary-75 hover:bg-primary-100")

        self._topLayout = QHBoxLayout()
        self._topLayout.addStretch(1)
        self._topLayout.setContentsMargins(0, 0, 0, 0)
        self._topLayout.addWidget(self._editCoverBtn)

        self._mainLayout.insertLayout(0, self._topLayout)

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()
        self._editCoverBtn.clicked.connect(self.__chooseCover)

    def __chooseCover(self) -> None:
        path = QFileDialog.getOpenFileName(self, filter=FileType.IMAGE)[0]
        if path is None or path == '':
            return

        try:
            coverData = Bytes.fromFile(path)

            Files.createDirectoryIfNotExisted("configuration/playlists")
            image = Image.open(io.BytesIO(coverData))
            image.save(self.__coverPath)

            super().setCover(coverData)
        except Exception as e:
            Logger.error(e)
            Dialogs.alert(
                header="Change cover failed",
                message='Something wrong while changing cover. Please try again.',
                acceptText="Ok",
            )


class UserPlaylistCard(PlaylistCard):

    def __init__(self, playlist: Playlist):
        super().__init__()
        super()._initComponent()

        self.__playlist = playlist
        self.setInfo(playlist.getInfo())
        self.applyLightMode()

    def _createUI(self) -> None:
        super()._createUI()
        self._title.setDefaultText("New Playlist")

        self._editBtn = Factory.createIconButton(size=Icons.MEDIUM, padding=Paddings.RELATIVE_50)
        self._editBtn.setLightModeIcon(Icons.EDIT.withColor(Colors.WHITE))
        self._editBtn.setClassName("rounded-full bg-primary-75 hover:bg-primary-100")
        self._editBtn.applyLightMode()

        self._deleteBtn = Factory.createIconButton(size=Icons.MEDIUM, padding=Paddings.RELATIVE_50)
        self._deleteBtn.setLightModeIcon(Icons.DELETE.withColor(Colors.WHITE))
        self._deleteBtn.setClassName("rounded-full bg-danger-75 hover:bg-danger-100")
        self._deleteBtn.applyLightMode()

        self._buttonsLayout = QVBoxLayout()
        self._buttonsLayout.setContentsMargins(0, 0, 0, 0)
        self._buttonsLayout.addWidget(self._editBtn)
        self._buttonsLayout.addWidget(self._deleteBtn)

        self._topLayout = QHBoxLayout()
        self._topLayout.setContentsMargins(0, 0, 0, 0)
        self._topLayout.addStretch(1)
        self._topLayout.addLayout(self._buttonsLayout)
        self._mainLayout.insertLayout(0, self._topLayout)

    def _connectSignalSlots(self) -> None:
        self._editBtn.clicked.connect(lambda: UpdatePlaylistDialog(self.__playlist).show())
        self._deleteBtn.clicked.connect(self.__openDeletePlaylistConfirm)

    def applyLightMode(self) -> None:
        pass

    def applyDarkMode(self) -> None:
        pass

    def __openDeletePlaylistConfirm(self) -> None:
        Dialogs.confirm(
            message="Are you sure want to delete this playlist. This action can not be reverted.",
            onAccept=self.__deletePlaylist
        )

    def __deletePlaylist(self) -> None:
        appCenter.playlists.remove(self.__playlist)
        path = self.__playlist.getInfo().getCoverPath()
        if path is not None:
            Files.removeFile(path)
