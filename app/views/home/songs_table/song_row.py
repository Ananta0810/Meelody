from contextlib import suppress

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFileDialog

from app.common.exceptions import ResourceException
from app.common.models import Song
from app.common.others import musicPlayer, appCenter, translator
from app.common.statics.enums import FileType
from app.common.statics.qt import Icons, Images
from app.common.statics.styles import Colors
from app.common.statics.styles import Paddings
from app.components.base import Factory, LabelWithDefaultText, CoverProps, CoverWithPlaceHolder
from app.components.dialogs import Dialogs
from app.components.widgets import ExtendableStyleWidget, StyleWidget, FlexBox
from app.helpers.base import silence, suppressException
from app.helpers.builders import ImageEditor
from app.helpers.others import Times, Logger
from app.helpers.qt import Widgets
from app.views.home.songs_table.dialogs.update_song_dialog import UpdateSongDialog


class SongRow(ExtendableStyleWidget):
    def __init__(self, song: Song):
        self.__song = song
        self.__editable = True

        super().__init__()
        super()._initComponent()

        self.__displaySongInfo()
        self._translateUI()

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
        self._cover.setPlaceHolderCover(CoverProps.fromBytes(Images.defaultSongCover, width=64, height=64, radius=12))

        self._titleLabel = LabelWithDefaultText()
        self._titleLabel.enableEllipsis()
        self._titleLabel.setFixedWidth(188)
        self._titleLabel.setFont(Factory.createFont(size=10))
        self._titleLabel.setClassName("text-black dark:text-white")

        self._artistLabel = LabelWithDefaultText()
        self._artistLabel.enableEllipsis()
        self._artistLabel.setFixedWidth(128)
        self._artistLabel.setFont(Factory.createFont(size=10))
        self._artistLabel.setClassName("text-gray")

        self._lengthLabel = LabelWithDefaultText()
        self._lengthLabel.enableEllipsis()
        self._lengthLabel.setFixedWidth(64)
        self._lengthLabel.setFont(Factory.createFont(size=10))
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
        self._moreBtn = Factory.createIconButton(size=Icons.large, padding=Paddings.RELATIVE_50)
        self._moreBtn.setLightModeIcon(Icons.more.withColor(Colors.gray))
        self._moreBtn.setDarkModeIcon(Icons.more.withColor(Colors.white))
        self._moreBtn.setClassName("hover:bg-black-10 rounded-full", "dark:hover:bg-white-20")

        self._loveBtn = Factory.createToggleButton(Icons.large, Paddings.RELATIVE_50)
        self._loveBtn.setActiveIcon(Icons.love.withColor(Colors.danger))
        self._loveBtn.setInactiveIcon(Icons.love.withColor(Colors.gray))
        self._loveBtn.setClassName(
            "rounded-full bg-none active/hover:bg-danger-12 inactive/hover:bg-gray-12",
            "dark:active/hover:bg-danger-20 dark:inactive/hover:bg-white-20"
        )

        self._playBtn = Factory.createToggleButton(size=Icons.large, padding=Paddings.RELATIVE_50)
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

        # ============================================ MORE BUTTONS # ============================================
        self._editSongBtn = Factory.createIconButton(size=Icons.large, padding=Paddings.RELATIVE_50)
        self._editSongBtn.setLightModeIcon(Icons.edit.withColor(Colors.primary))
        self._editSongBtn.setDarkModeIcon(Icons.edit.withColor(Colors.white))
        self._editSongBtn.setClassName("hover:bg-primary-12 rounded-full", "dark:hover:bg-white-20")
        self._editSongBtn.keepSpaceWhenHiding()

        self._editCoverBtn = Factory.createIconButton(size=Icons.large, padding=Paddings.RELATIVE_50)
        self._editCoverBtn.setLightModeIcon(Icons.image.withColor(Colors.primary))
        self._editCoverBtn.setDarkModeIcon(Icons.image.withColor(Colors.white))
        self._editCoverBtn.setClassName("hover:bg-primary-12 rounded-full", "dark:hover:bg-white-20")
        self._editCoverBtn.keepSpaceWhenHiding()

        self._deleteBtn = Factory.createIconButton(size=Icons.large, padding=Paddings.RELATIVE_50)
        self._deleteBtn.setLightModeIcon(Icons.delete.withColor(Colors.primary))
        self._deleteBtn.setDarkModeIcon(Icons.delete.withColor(Colors.white))
        self._deleteBtn.setClassName("hover:bg-primary-12 rounded-full", "dark:hover:bg-white-20")
        self._deleteBtn.keepSpaceWhenHiding()

        self._closeMenuBtn = Factory.createIconButton(size=Icons.medium, padding=Paddings.RELATIVE_50, parent=self)
        self._closeMenuBtn.setLightModeIcon(Icons.close.withColor(Colors.white))
        self._closeMenuBtn.setClassName("rounded-full bg-danger hover:bg-danger-[w120]")
        self._closeMenuBtn.hide()

        self._moreButtons = StyleWidget()
        self._moreButtons.setClassName("bg-black-4 rounded-12 dark:bg-white-4")
        self._moreButtonsLayout = FlexBox(self._moreButtons)
        self._moreButtonsLayout.setContentsMargins(8, 4, 8, 4)
        self._moreButtonsLayout.setSpacing(8)
        self._moreButtons.hide()

        self._moreButtonsLayout.addWidget(self._editSongBtn)
        self._moreButtonsLayout.addWidget(self._editCoverBtn)
        self._moreButtonsLayout.addWidget(self._deleteBtn)

        self._mainLayout.addWidget(self._mainButtons)
        self._mainLayout.addWidget(self._moreButtons)

    def _translateUI(self) -> None:
        self._moreBtn.setToolTip(translator.translate("SONG_ROW.MORE_BTN"))
        self._loveBtn.setToolTips([translator.translate("SONG_ROW.UNLOVE_BTN"), translator.translate("SONG_ROW.LOVE_BTN")])
        self._playBtn.setToolTips([translator.translate("SONG_ROW.PAUSE_BTN"), translator.translate("SONG_ROW.PLAY_BTN")])
        self._editSongBtn.setToolTip(translator.translate("SONG_ROW.EDIT_BTN"))
        self._editCoverBtn.setToolTip(translator.translate("SONG_ROW.EDIT_COVER_BTN"))
        self._deleteBtn.setToolTip(translator.translate("SONG_ROW.DELETE_BTN"))
        self._closeMenuBtn.setToolTip(translator.translate("SONG_ROW.CLOSE_BTN"))

    def _connectSignalSlots(self) -> None:
        self._moreBtn.clicked.connect(lambda: silence(lambda: self.showMoreButtons(True)))
        self._closeMenuBtn.clicked.connect(lambda: silence(lambda: self.showMoreButtons(False)))

        self._loveBtn.clicked.connect(lambda: silence(lambda: self.__song.updateLoveState(self._loveBtn.isActive())))
        self._playBtn.clicked.connect(lambda: self.__playOrPauseCurrentSong())
        self._editCoverBtn.clicked.connect(lambda: self.__changeCover())
        self._editSongBtn.clicked.connect(lambda: self.__changeSongInfo())
        self._deleteBtn.clicked.connect(lambda: self.__confirmToDeleteSong())

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
        self.__editable = editable
        self.__setEditable(editable and musicPlayer.getCurrentSong() != self.__song)

    @suppressException
    def __checkEditable(self, currentPlayingSong: Song) -> None:
        if self.__editable:
            editable = currentPlayingSong != self.__song
            self.__setEditable(editable)

    def __setEditable(self, editable):
        self._editSongBtn.setVisible(editable)
        self._editCoverBtn.setVisible(editable)
        self._deleteBtn.setVisible(editable)

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
        self.showMoreButtons(False)
        super().show()

        if not self.__song.isCoverLoaded():
            self.__song.loadCover()

    @suppressException
    def showMoreButtons(self, a0: bool) -> None:
        self._mainButtons.setVisible(not a0)
        self._moreButtons.setVisible(a0)
        self._closeMenuBtn.setVisible(a0)
        if a0:
            menuCorner = self._moreButtons.geometry().topRight()
            self._closeMenuBtn.move(menuCorner.x() - self._closeMenuBtn.width() - 4, menuCorner.y() + 4)
            self._closeMenuBtn.raise_()

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
        self._cover.setCover(CoverProps.fromBytes(cover, width=64, height=64, radius=12))

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


class LoadCoverThread(QThread):

    def __init__(self, song: Song) -> None:
        super().__init__()
        self.__song = song

    def run(self) -> None:
        self.__song.loadCover()
