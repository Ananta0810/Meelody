import os
from contextlib import suppress
from typing import Optional

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QMouseEvent, QResizeEvent
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFileDialog

from app.common.exceptions import ResourceException
from app.common.models import Song
from app.common.others import musicPlayer, appCenter, translator
from app.common.statics.enums import FileType
from app.common.statics.qt import Icons, Images
from app.common.statics.styles import Colors
from app.common.statics.styles import Paddings
from app.components.base import FontFactory
from app.components.buttons import ButtonFactory
from app.components.dialogs import Dialogs
from app.components.images.cover import CoverWithPlaceHolder, Cover
from app.components.labels import LabelWithPlaceHolder
from app.components.others import DotPage
from app.components.widgets import ExtendableStyleWidget, FlexBox
from app.helpers.files import ImageEditor
from app.utils.base import silence, Strings
from app.utils.others import Times, Logger, Files
from app.utils.qt import Widgets
from app.utils.reflections import suppressException
from app.views.windows.main_window.home.songs_table.dialogs.update_song_dialog import UpdateSongDialog


class SongRow(ExtendableStyleWidget):
    def __init__(self, song: Song):
        self.__song = song
        self.__isEditable = True

        super().__init__()
        super()._initComponent()

        self.__displaySongInfo()
        self.translateUI()

    def _createUI(self) -> None:
        self.setClassName("bg-none hover:bg-gray-12 rounded-12")

        self._mainLayout = QHBoxLayout()
        self._mainLayout.setContentsMargins(20, 4, 4, 4)
        self._mainLayout.setSpacing(0)
        self._mainLayout.setAlignment(Qt.AlignLeft)
        self.setLayout(self._mainLayout)

        # ================================================= INFO  =================================================

        self._cover = CoverWithPlaceHolder(self)
        self._cover.setFixedSize(64, 64)
        self._cover.setPlaceHolderCover(Cover.Props.fromBytes(Images.defaultSongCover, width=64, height=64, radius=12))

        self._titleLabel = LabelWithPlaceHolder()
        self._titleLabel.enableEllipsis()
        self._titleLabel.setFixedWidth(188)
        self._titleLabel.setFont(FontFactory.create(size=10))
        self._titleLabel.setClassName("text-black dark:text-white")

        self._artistLabel = LabelWithPlaceHolder()
        self._artistLabel.enableEllipsis()
        self._artistLabel.setFixedWidth(128)
        self._artistLabel.setFont(FontFactory.create(size=10))
        self._artistLabel.setClassName("text-gray")

        self._lengthLabel = LabelWithPlaceHolder()
        self._lengthLabel.enableEllipsis()
        self._lengthLabel.setFixedWidth(64)
        self._lengthLabel.setFont(FontFactory.create(size=10))
        self._lengthLabel.setClassName("text-gray")

        self._info = QHBoxLayout()
        self._info.setSpacing(24)
        self._info.setContentsMargins(0, 8, 0, 8)
        self._info.addWidget(self._cover)
        self._info.addWidget(self._titleLabel, 1)
        self._info.addWidget(self._artistLabel, 1)
        self._info.addWidget(self._lengthLabel)
        self._mainLayout.addLayout(self._info)

        # ============================================ REACT BUTTONS # ============================================
        self._moreBtn = ButtonFactory.createIconButton(size=Icons.large, padding=Paddings.relative50)
        self._moreBtn.setLightModeIcon(Icons.more.withColor(Colors.gray))
        self._moreBtn.setDarkModeIcon(Icons.more.withColor(Colors.white))
        self._moreBtn.setClassName("hover:bg-black-10 rounded-full", "dark:hover:bg-white-20")

        self._loveBtn = ButtonFactory.createToggleButton(Icons.large, Paddings.relative50)
        self._loveBtn.setActiveIcon(Icons.loved.withColor(Colors.danger))
        self._loveBtn.setInactiveIcon(Icons.love.withColor(Colors.gray))
        self._loveBtn.setClassName(
            "rounded-full bg-none active/hover:bg-danger-12 inactive/hover:bg-gray-12",
            "dark:active/hover:bg-danger-20 dark:inactive/hover:bg-white-20"
        )

        self._playBtn = ButtonFactory.createToggleButton(size=Icons.large, padding=Paddings.relative50)
        self._playBtn.setActiveIcon(Icons.pause.withColor(Colors.primary), Icons.pause.withColor(Colors.white))
        self._playBtn.setInactiveIcon(Icons.play.withColor(Colors.primary), Icons.play.withColor(Colors.white))
        self._playBtn.setClassName("hover:bg-primary-25 bg-primary-10 rounded-full", "dark:bg-white-20 dark:hover:bg-primary")
        self._playBtn.setActive(False)

        self._mainButtons = QWidget()
        self._mainButtonsLayout = FlexBox(self._mainButtons)
        self._mainButtonsLayout.setContentsMargins(8, 8, 8, 8)
        self._mainButtonsLayout.setSpacing(8)
        self._mainButtonsLayout.addWidget(self._moreBtn)
        self._mainButtonsLayout.addWidget(self._loveBtn)
        self._mainButtonsLayout.addWidget(self._playBtn)

        self._moreMenu = None

        self._mainLayout.addWidget(self._mainButtons)

    def __createMoreMenu(self) -> None:
        # ============================================ MORE BUTTONS # ============================================
        self._moreMenu = _MoreMenu()
        self._moreMenu.setFixedWidth(236)
        self._moreMenu.setClassName("bg-black-4 rounded-12 dark:bg-white-4")
        self._moreMenu.applyTheme()
        self._moreMenu.translateUI()
        self.setEditable(self.__isEditable)

        self._moreMenu.editCoverBtn.clicked.connect(lambda: self.__changeCover())
        self._moreMenu.editSongBtn.clicked.connect(lambda: self.__changeSongInfo())
        self._moreMenu.deleteBtn.clicked.connect(lambda: self.__confirmToDeleteSong())
        self._moreMenu.exportBtn.clicked.connect(lambda: self.__exportSong())

        self._mainLayout.addWidget(self._moreMenu)

    def mousePressEvent(self, a0: Optional[QMouseEvent]) -> None:
        super().mousePressEvent(a0)
        if self._moreMenu is not None:
            clickedOutsideMoreMenu = not self._moreMenu.geometry().contains(a0.pos())
            if clickedOutsideMoreMenu:
                self.__showMoreMenu(False)

    @suppressException
    def translateUI(self) -> None:
        self._moreBtn.setToolTip(translator.translate("SONG_ROW.MORE_BTN"))
        self._loveBtn.setToolTips([translator.translate("SONG_ROW.UNLOVE_BTN"), translator.translate("SONG_ROW.LOVE_BTN")])
        self._playBtn.setToolTips([translator.translate("SONG_ROW.PAUSE_BTN"), translator.translate("SONG_ROW.PLAY_BTN")])

    def _connectSignalSlots(self) -> None:
        self._moreBtn.clicked.connect(lambda: silence(lambda: self.__showMoreMenu(True)))
        self._loveBtn.clicked.connect(lambda: silence(lambda: self.__song.updateLoveState(self._loveBtn.isActive())))
        self._playBtn.clicked.connect(lambda: self.__playOrPauseCurrentSong())

        self.__song.loved.connect(lambda loved: silence(lambda: self._loveBtn.setActive(loved)))
        self.__song.coverChanged.connect(lambda cover: self.__setCover(cover))
        self.__song.updated.connect(lambda updatedField: self.__updateSongField(updatedField))

        musicPlayer.songChanged.connect(lambda song: self.__checkEditable(song))
        musicPlayer.played.connect(self.__updatePlayBtn)
        musicPlayer.paused.connect(self.__onMusicPlayerPaused)

    @suppressException
    def applyLightMode(self) -> None:
        super().applyLightMode()
        self.applyThemeToChildren()

    @suppressException
    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        self.applyThemeToChildren()

    @suppressException
    def setEditable(self, editable: bool) -> None:
        self.__isEditable = editable
        if self._moreMenu is not None:
            self._moreMenu.setEditable(editable and musicPlayer.getCurrentSong() != self.__song)

    @suppressException
    def __checkEditable(self, currentPlayingSong: Song) -> None:
        if self.__isEditable:
            editable = currentPlayingSong != self.__song
            if self._moreMenu is not None:
                self._moreMenu.setEditable(editable)

    @suppressException
    def __updatePlayBtn(self) -> None:
        self._playBtn.setActive(musicPlayer.getCurrentSong() == self.__song)

    @suppressException
    def __onMusicPlayerPaused(self) -> None:
        self._playBtn.setActive(False)

    def content(self) -> Song:
        return self.__song

    @suppressException
    def deleteLater(self) -> None:
        with suppress(TypeError):
            musicPlayer.played.disconnect(self.__checkEditable)
            musicPlayer.played.disconnect(self.__updatePlayBtn)
            musicPlayer.paused.disconnect(self.__onMusicPlayerPaused)

        super().deleteLater()

    @suppressException
    def show(self) -> None:
        self.__showMoreMenu(False)
        super().show()

        if not self.__song.isCoverLoaded():
            self.__song.loadCover()

    @suppressException
    def hide(self) -> None:
        super().hide()
        self.__showMoreMenu(False)

    @suppressException
    def __showMoreMenu(self, show: bool) -> None:
        if not show and self._moreMenu is None:
            return

        if self._moreMenu is None:
            self.__createMoreMenu()

        self._mainButtons.setVisible(not show)
        self._moreMenu.setVisible(show)

    @suppressException
    def __playOrPauseCurrentSong(self) -> None:
        if self._playBtn.isActive():
            musicPlayer.loadPlaylist(appCenter.currentPlaylist.getSongs())
            musicPlayer.playSong(self.__song)
        else:
            musicPlayer.pause()

    @suppressException
    def __displaySongInfo(self) -> None:
        if self.__song.isCoverLoaded() and Widgets.isInView(self):
            self.__setCover(self.__song.getCover())

        self._titleLabel.setText(self.__song.getTitle())
        self._artistLabel.setText(self.__song.getArtist())
        self._lengthLabel.setText(Times.toString(self.__song.getLength()))
        self._loveBtn.setActive(self.__song.isLoved())

    @suppressException
    def __setCover(self, cover: bytes) -> None:
        self._cover.setCover(Cover.Props.fromBytes(cover, width=64, height=64, radius=12))

    @suppressException
    def __updateSongField(self, field: str) -> None:
        if field == "title":
            self._titleLabel.setText(self.__song.getTitle())

        if field == "artist":
            self._artistLabel.setText(self.__song.getArtist())

        if field == "love":
            self._loveBtn.setActive(self.__song.isLoved())

    def __changeCover(self) -> None:
        path = QFileDialog.getOpenFileName(self, filter=FileType.image)[0]
        if path is None or path == '':
            return
        try:
            imageEditor = ImageEditor.ofFile(path)
            cover = imageEditor.square().resize(512, 512).toBytes()
            self.__song.updateCover(cover)
            Logger.info("Update song cover succeed.")
        except ResourceException as e:
            if e.isNotFound():
                Dialogs.alert(message=translator.translate("SONG_ROW.EDIT_FAILED_NOT_FOUND"))
            if e.isBeingUsed():
                Dialogs.alert(message=translator.translate("SONG_ROW.EDIT_FAILED_SONG_PLAYING"))
        except Exception as e:
            Logger.error(e)
            Logger.error("Update song cover failed.")
            Dialogs.alert(message=translator.translate("SONG_ROW.EDIT_COVER_FAILED"))

    def __changeSongInfo(self) -> None:
        dialog = UpdateSongDialog(self.__song)
        dialog.show()

    def __confirmToDeleteSong(self) -> None:
        Dialogs.confirm(
            message=translator.translate("SONG_ROW.DELETE_SONG_MSG"),
            acceptText=translator.translate("SONG_ROW.DELETE_SONG_BTN"),
            onAccept=lambda: self.__deleteCurrentSong()
        )

    def __deleteCurrentSong(self) -> None:
        try:
            self.__song.delete()
            Logger.info("Delete song succeed.")
        except ResourceException as e:
            if e.isBeingUsed():
                Dialogs.alert(message=translator.translate("SONG_ROW.DELETE_FAILED_PLAYING"))
        except Exception as e:
            Logger.error(e)
            Logger.error("Delete song failed.")
            Dialogs.alert(message=translator.translate("SONG_ROW.DELETE_FAILED"))

    def __exportSong(self) -> None:
        directory = QFileDialog.getExistingDirectory(self, 'Select folder to export')
        if Strings.isBlank(directory):
            return

        try:
            destiny = Strings.joinPath(directory, f"{self.__song.getTitle()}.mp3")

            if os.path.exists(destiny):
                Dialogs.alert(message=translator.translate("SONG_ROW.EXPORT_FAILED_EXISTED"))
                return

            Files.copyFile(self.__song.getLocation(), destiny)

            Dialogs.confirm(
                header=translator.translate("SONG_ROW.EXPORT_HEADER"),
                message=translator.translate("SONG_ROW.EXPORT_MESSAGE"),
                acceptText=translator.translate("SONG_ROW.EXPORT_ACCEPT_BTN"),
                cancelText=translator.translate("SONG_ROW.EXPORT_CANCEL_BTN"),
                onAccept=lambda: os.startfile(directory),
                variant="info"
            )
            Logger.error(f"Export song '{self.__song.getTitle()}' to '{directory}' successfully")
        except Exception as e:
            print(e)
            Logger.error(f"Failed to export song '{self.__song.getTitle()}' to '{directory}'")
            Dialogs.alert(message=translator.translate("SONG_ROW.EXPORT_FAILED"))


class LoadCoverThread(QThread):

    def __init__(self, song: Song) -> None:
        super().__init__()
        self.__song = song

    def run(self) -> None:
        self.__song.loadCover()


class _MoreMenu(ExtendableStyleWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        super()._initComponent()

    def _createUI(self) -> None:
        super()._createUI()
        self.editSongBtn = ButtonFactory.createIconButton(size=Icons.large, padding=Paddings.relative50)
        self.editSongBtn.setLightModeIcon(Icons.edit.withColor(Colors.primary))
        self.editSongBtn.setDarkModeIcon(Icons.edit.withColor(Colors.white))
        self.editSongBtn.setClassName("hover:bg-primary-12 rounded-full", "dark:hover:bg-white-20")

        self.editCoverBtn = ButtonFactory.createIconButton(size=Icons.large, padding=Paddings.relative50)
        self.editCoverBtn.setLightModeIcon(Icons.image.withColor(Colors.primary))
        self.editCoverBtn.setDarkModeIcon(Icons.image.withColor(Colors.white))
        self.editCoverBtn.setClassName("hover:bg-primary-12 rounded-full", "dark:hover:bg-white-20")

        self.deleteBtn = ButtonFactory.createIconButton(size=Icons.large, padding=Paddings.relative50)
        self.deleteBtn.setLightModeIcon(Icons.delete.withColor(Colors.primary))
        self.deleteBtn.setDarkModeIcon(Icons.delete.withColor(Colors.white))
        self.deleteBtn.setClassName("hover:bg-primary-12 rounded-full", "dark:hover:bg-white-20")

        self.exportBtn = ButtonFactory.createIconButton(size=Icons.large, padding=Paddings.relative50)
        self.exportBtn.setLightModeIcon(Icons.export.withColor(Colors.primary))
        self.exportBtn.setDarkModeIcon(Icons.export.withColor(Colors.white))
        self.exportBtn.setClassName("hover:bg-primary-12 rounded-full", "dark:hover:bg-white-20")
        self.exportBtn.hide()

        self._dotPage = DotPage(self)
        self._dotPage.setTotalPages(2)
        self._dotPage.setAlignment(Qt.AlignRight)
        self._dotPage.setContentsMargins(8, 8, 8, 8)
        self._dotPage.setActivePage(0)

        self._layout = FlexBox(self)
        self._layout.setAlignment(Qt.AlignLeft)
        self._layout.setContentsMargins(23, 4, 23, 4)
        self._layout.setSpacing(27)

        self._layout.addWidget(self.editSongBtn)
        self._layout.addWidget(self.editCoverBtn)
        self._layout.addWidget(self.deleteBtn)
        self._layout.addWidget(self.exportBtn)

        self.applyTheme()
        self.applyThemeToChildren()
        self.translateUI()

    def translateUI(self) -> None:
        self.editSongBtn.setToolTip(translator.translate("SONG_ROW.EDIT_BTN"))
        self.editCoverBtn.setToolTip(translator.translate("SONG_ROW.EDIT_COVER_BTN"))
        self.deleteBtn.setToolTip(translator.translate("SONG_ROW.DELETE_BTN"))
        self.exportBtn.setToolTip(translator.translate("SONG_ROW.EXPORT_BTN"))
        self._dotPage.setToolTip(translator.translate("SONG_ROW.NEXT_PAGE"))

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()
        self._dotPage.pageChanged.connect(lambda page: self.__showPageItems(page))

    def resizeEvent(self, a0: Optional[QResizeEvent]) -> None:
        super().resizeEvent(a0)
        self._dotPage.setFixedWidth(self.width())

    def setEditable(self, editable: bool) -> None:
        self.editSongBtn.setVisible(editable)
        self.editCoverBtn.setVisible(editable)
        self.deleteBtn.setVisible(editable)
        self._dotPage.setVisible(editable)

        self.exportBtn.hide()
        if editable:
            self._dotPage.setActivePage(0)

    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self._layout.setContentsMargins(left, top, right, bottom)

    def __showPageItems(self, page: int) -> None:
        self.editSongBtn.setVisible(page == 0)
        self.editCoverBtn.setVisible(page == 0)
        self.deleteBtn.setVisible(page == 0)
        self.exportBtn.setVisible(page == 1)

    def mousePressEvent(self, a0: Optional[QMouseEvent]) -> None:
        super().mousePressEvent(a0)
        if a0.button() == Qt.RightButton:
            self._dotPage.nextPage()
