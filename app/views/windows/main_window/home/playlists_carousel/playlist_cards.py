from typing import Optional

from PyQt5 import QtGui
from PyQt5.QtCore import QEvent, QRect, pyqtSignal, Qt, pyqtBoundSignal
from PyQt5.QtGui import QResizeEvent, QShowEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFileDialog

from app.common.models import Playlist
from app.common.models.playlists import FavouritesPlaylist
from app.common.others import appCenter, translator
from app.common.statics.enums import FileType
from app.common.statics.qt import Cursors, Images, Icons
from app.common.statics.styles import Colors
from app.common.statics.styles import Paddings
from app.components.base import FontFactory
from app.components.buttons import ButtonFactory
from app.components.dialogs import Dialogs
from app.components.images.cover import ZoomCover, Cover
from app.components.labels.ellipsis_label import EllipsisLabel
from app.components.widgets import ExtendableStyleWidget
from app.helpers.builders import ImageEditor
from app.utils.base import Bytes, Lists
from app.utils.others import Files, Logger
from app.utils.qt import Pixmaps, Widgets
from app.views.windows.main_window.home.playlists_carousel.update_playlist_dialog import UpdatePlaylistDialog


class PlaylistCard(ExtendableStyleWidget):
    clicked: pyqtBoundSignal = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

    def _createUI(self) -> None:
        self.setFixedSize(256, 320)
        self.setCursor(Cursors.pointer)

        self._mainLayout = QVBoxLayout(self)
        self._mainLayout.setContentsMargins(20, 20, 20, 20)

        self._cover = ZoomCover(self)
        self._cover.setCover(self._toCoverProps(Images.defaultPlaylistCover))
        self._cover.setAnimation(duration=250, start=1.0, end=1.1)

        self._title = EllipsisLabel(autoChangeTheme=False)
        self._title.setFont(FontFactory.create(size=16, bold=True))
        self._title.setFixedWidth(self.width() - self._mainLayout.contentsMargins().left() - self._mainLayout.contentsMargins().right())
        self._title.setClassName("text-black dark:text-white")

        self._mainLayout.addStretch()
        self._mainLayout.addWidget(self._title)

    def setInfo(self, info: Playlist.Info) -> None:
        self._title.setText(info.getName())
        self.setCover(info.getCover())

    def setCover(self, data: bytes) -> None:
        data = data or Images.defaultPlaylistCover

        cover = self._toCoverProps(data)
        self._cover.setCover(self._toCoverProps(data))

        if cover is None:
            self._title.applyLightMode()
            return

        if Widgets.isInView(self):
            self.adaptTitleColorToCover()

    def adaptTitleColorToCover(self):
        width = self._title.fontMetrics().boundingRect(self._title.ellipsisText()).width()
        labelRect = QRect(self._title.pos().x(), self._title.pos().y(), width, self._title.rect().height())

        pixmap = self._cover.currentCover().content().copy(labelRect)
        colors = Pixmaps.getDominantColors(pixmap, maxColors=10)
        isDarkMode = Lists.findMostFrequency([color.isDarkColor() for color in colors])

        self._title.applyDarkMode() if isDarkMode else self._title.applyLightMode()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self._cover.setFixedSize(self.size())
        return super().resizeEvent(event)

    def enterEvent(self, event: QEvent) -> None:
        super().enterEvent(event)
        self._cover.animationOnEnteredHover()

    def leaveEvent(self, event: QEvent) -> None:
        super().leaveEvent(event)
        self._cover.animationOnLeftHover()

    def mousePressEvent(self, event: Optional[QtGui.QMouseEvent]) -> None:
        super().mousePressEvent(event)
        if event is not None and event.button() == Qt.LeftButton:
            self.clicked.emit()

    @staticmethod
    def _toCoverProps(cover: bytes) -> Cover.Props:
        return Cover.Props.fromBytes(cover, width=256, height=320, radius=24)


class LibraryPlaylistCard(PlaylistCard):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        super()._initComponent()
        super().setCover(Images.defaultPlaylistCover)

    def translateUI(self) -> None:
        self._title.setText(translator.translate("PLAYLIST_CAROUSEL.LIBRARY"))
        super().translateUI()

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()
        self.clicked.connect(lambda: self.__selectLibraryPlaylist())

    @staticmethod
    def __selectLibraryPlaylist():
        if appCenter.currentPlaylist.getInfo().getId() != appCenter.library.getInfo().getId():
            appCenter.setActivePlaylist(appCenter.library)

    def showEvent(self, a0: Optional[QShowEvent]) -> None:
        super().showEvent(a0)
        self.adaptTitleColorToCover()


class FavouritePlaylistCard(PlaylistCard):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        super()._initComponent()

        self.__coverPath = "configuration/playlists/favourite-cover.png"
        super().setCover(Bytes.fromFile(self.__coverPath))

    def _createUI(self) -> None:
        super()._createUI()

        self._editCoverBtn = ButtonFactory.createIconButton(size=Icons.medium, padding=Paddings.RELATIVE_50)
        self._editCoverBtn.setLightModeIcon(Icons.image.withColor(Colors.white))
        self._editCoverBtn.setClassName("rounded-full bg-primary hover:bg-primary-[w120]")

        self._topLayout = QHBoxLayout()
        self._topLayout.addStretch(1)
        self._topLayout.setContentsMargins(0, 0, 0, 0)
        self._topLayout.addWidget(self._editCoverBtn)

        self._mainLayout.insertLayout(0, self._topLayout)

    def translateUI(self) -> None:
        self._title.setText(translator.translate("PLAYLIST_CAROUSEL.FAVOURITES"))
        self._editCoverBtn.setToolTip(translator.translate("PLAYLIST_CAROUSEL.FAVOURITES.EDIT_COVER_BTN"))

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()
        self.clicked.connect(lambda: self.__selectFavouritesPlaylist())
        self._editCoverBtn.clicked.connect(lambda: self.__chooseCover())

    def showEvent(self, a0: Optional[QShowEvent]) -> None:
        super().showEvent(a0)
        self.adaptTitleColorToCover()

    @staticmethod
    def __selectFavouritesPlaylist() -> None:
        if appCenter.currentPlaylist.getInfo().getId() == FavouritesPlaylist.Info().getId():
            return

        favouritePlaylist = FavouritesPlaylist(appCenter.library)
        favouritePlaylist.load()

        appCenter.setActivePlaylist(favouritePlaylist)

    def __chooseCover(self) -> None:
        path = QFileDialog.getOpenFileName(self, filter=FileType.image)[0]
        if path is None or path == '':
            return

        try:
            imageEditor = ImageEditor.ofFile(path)
            cover = imageEditor.square().resize(320, 320).toBytes()
            Files.saveImageFile(cover, self.__coverPath)

            super().setCover(cover)
        except Exception as e:
            Logger.error(e)
            Dialogs.alert(
                header=translator.translate("PLAYLIST_CAROUSEL.PLAYLIST.UPDATED_COVER_FAILED_HEADER"),
                message=translator.translate("PLAYLIST_CAROUSEL.PLAYLIST.UPDATED_COVER_FAILED_MSG"),
            )


class UserPlaylistCard(PlaylistCard):

    def __init__(self, playlist: Playlist):
        super().__init__()
        super()._initComponent()

        self.__playlist = playlist
        self.setInfo(playlist.getInfo())
        self.applyLightMode()
        self.translateUI()

    def _createUI(self) -> None:
        super()._createUI()
        self._editBtn = ButtonFactory.createIconButton(size=Icons.medium, padding=Paddings.RELATIVE_50)
        self._editBtn.setLightModeIcon(Icons.edit.withColor(Colors.white))
        self._editBtn.setClassName("rounded-full bg-primary hover:bg-primary-[w120]")
        self._editBtn.applyLightMode()

        self._deleteBtn = ButtonFactory.createIconButton(size=Icons.medium, padding=Paddings.RELATIVE_50)
        self._deleteBtn.setLightModeIcon(Icons.delete.withColor(Colors.white))
        self._deleteBtn.setClassName("rounded-full bg-danger hover:bg-danger-[w120]")
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

    def translateUI(self) -> None:
        self._editBtn.setToolTip(translator.translate("PLAYLIST_CAROUSEL.PLAYLIST.EDIT_BTN"))
        self._deleteBtn.setToolTip(translator.translate("PLAYLIST_CAROUSEL.PLAYLIST.DELETE_BTN"))

    def _connectSignalSlots(self) -> None:
        self.clicked.connect(lambda: self.__selectCurrentPlaylist())
        self._editBtn.clicked.connect(lambda: UpdatePlaylistDialog(self.__playlist).show())
        self._deleteBtn.clicked.connect(lambda: self.__openDeletePlaylistConfirm())

    def applyLightMode(self) -> None:
        pass

    def applyDarkMode(self) -> None:
        pass

    def __selectCurrentPlaylist(self) -> None:
        if appCenter.currentPlaylist.getInfo().getId() == self.__playlist.getInfo().getId():
            return

        appCenter.setActivePlaylist(self.__playlist)

    def __openDeletePlaylistConfirm(self) -> None:
        if appCenter.currentPlaylist.getInfo().getId() == self.__playlist.getInfo().getId():
            Dialogs.alert(message=translator.translate("PLAYLIST_CAROUSEL.PLAYLIST.DELETE_CURRENT_PLAYLIST"))
            return

        Dialogs.confirm(
            message=translator.translate("PLAYLIST_CAROUSEL.PLAYLIST.DELETE_CONFIRM_MESSAGE"),
            acceptText=translator.translate("PLAYLIST_CAROUSEL.PLAYLIST.DELETE_CONFIRM_OK"),
            onAccept=self.__deletePlaylist
        )

    def __deletePlaylist(self) -> None:
        appCenter.playlists.remove(self.__playlist)
        path = self.__playlist.getInfo().getCoverPath()
        if path is not None:
            Files.removeFile(path)
