from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFileDialog

from app.common.models import Song
from app.common.others import musicPlayer, appCenter
from app.components.base import Cover, Factory, LabelWithDefaultText, CoverProps
from app.components.dialogs import Dialogs
from app.components.widgets import ExtendableStyleWidget, StyleWidget, FlexBox
from app.helpers.base import Bytes
from app.helpers.others import Times, Logger
from app.helpers.qt import Widgets, Pixmaps
from app.helpers.stylesheets import Paddings, Colors
from app.resource.others import FileType
from app.resource.qt import Icons, Images


class SongRow(ExtendableStyleWidget):
    def __init__(self, song: Song):
        self.__song = song

        super().__init__()
        super()._initComponent()

        self.__displaySongInfo(song)

    def _createUI(self) -> None:
        self.setClassName("bg-none hover:bg-gray-12 rounded-12")

        self._mainLayout = QHBoxLayout()
        self._mainLayout.setContentsMargins(20, 4, 4, 4)
        self._mainLayout.setSpacing(0)
        self._mainLayout.setAlignment(Qt.AlignLeft)
        self.setLayout(self._mainLayout)

        # ================================================= INFO  =================================================

        self._cover = Cover(self)
        self._cover.setFixedSize(64, 64)
        self._cover.setDefaultCover(CoverProps.fromBytes(Images.DEFAULT_SONG_COVER, width=64, height=64, radius=12))

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
        self._moreBtn = Factory.createIconButton(size=Icons.LARGE, padding=Paddings.RELATIVE_50)
        self._moreBtn.setLightModeIcon(Icons.MORE.withColor(Colors.GRAY))
        self._moreBtn.setDarkModeIcon(Icons.MORE.withColor(Colors.WHITE))
        self._moreBtn.setClassName("hover:bg-black-10 rounded-full", "dark:hover:bg-white-20")

        self._loveBtn = Factory.createToggleButton(Icons.LARGE, Paddings.RELATIVE_50)
        self._loveBtn.setActiveIcon(Icons.LOVE.withColor(Colors.DANGER))
        self._loveBtn.setInactiveIcon(Icons.LOVE.withColor(Colors.GRAY))
        self._loveBtn.setClassName(
            "rounded-full bg-none active/hover:bg-danger-12 inactive/hover:bg-gray-12",
            "dark:active/hover:bg-danger-20 dark:inactive/hover:bg-white-20"
        )

        self._playBtn = Factory.createIconButton(size=Icons.LARGE, padding=Paddings.RELATIVE_50)
        self._playBtn.setLightModeIcon(Icons.PLAY.withColor(Colors.PRIMARY))
        self._playBtn.setDarkModeIcon(Icons.PLAY.withColor(Colors.WHITE))
        self._playBtn.setClassName("hover:bg-primary-25 bg-primary-10 rounded-full", "dark:bg-white-20 dark:hover:bg-primary")

        self._mainButtons = QWidget()
        self._mainButtonsLayout = FlexBox(self._mainButtons)
        self._mainButtonsLayout.setContentsMargins(8, 8, 8, 8)
        self._mainButtonsLayout.setSpacing(8)
        self._mainButtonsLayout.addWidget(self._moreBtn)
        self._mainButtonsLayout.addWidget(self._loveBtn)
        self._mainButtonsLayout.addWidget(self._playBtn)

        # ============================================ MORE BUTTONS # ============================================
        self._editSongBtn = Factory.createIconButton(size=Icons.LARGE, padding=Paddings.RELATIVE_50)
        self._editSongBtn.setLightModeIcon(Icons.EDIT.withColor(Colors.PRIMARY))
        self._editSongBtn.setDarkModeIcon(Icons.EDIT.withColor(Colors.WHITE))
        self._editSongBtn.setClassName("hover:bg-primary-12 rounded-full", "dark:hover:bg-white-20")
        self._editSongBtn.keepSpaceWhenHiding()

        self._editCoverBtn = Factory.createIconButton(size=Icons.LARGE, padding=Paddings.RELATIVE_50)
        self._editCoverBtn.setLightModeIcon(Icons.IMAGE.withColor(Colors.PRIMARY))
        self._editCoverBtn.setDarkModeIcon(Icons.IMAGE.withColor(Colors.WHITE))
        self._editCoverBtn.setClassName("hover:bg-primary-12 rounded-full", "dark:hover:bg-white-20")
        self._editCoverBtn.keepSpaceWhenHiding()

        self._deleteBtn = Factory.createIconButton(size=Icons.LARGE, padding=Paddings.RELATIVE_50)
        self._deleteBtn.setLightModeIcon(Icons.DELETE.withColor(Colors.PRIMARY))
        self._deleteBtn.setDarkModeIcon(Icons.DELETE.withColor(Colors.WHITE))
        self._deleteBtn.setClassName("hover:bg-primary-12 rounded-full", "dark:hover:bg-white-20")
        self._deleteBtn.keepSpaceWhenHiding()

        self._closeMenuBtn = Factory.createIconButton(size=Icons.MEDIUM, padding=Paddings.RELATIVE_50, parent=self)
        self._closeMenuBtn.setLightModeIcon(Icons.CLOSE.withColor(Colors.WHITE))
        self._closeMenuBtn.setClassName("rounded-full bg-danger-75 hover:bg-danger")
        self._closeMenuBtn.hide()

        self._moreButtons = StyleWidget()
        self._moreButtons.setClassName("bg-black-4 rounded-12")
        self._moreButtonsLayout = FlexBox(self._moreButtons)
        self._moreButtonsLayout.setContentsMargins(8, 4, 8, 4)
        self._moreButtonsLayout.setSpacing(8)
        self._moreButtons.hide()

        self._moreButtonsLayout.addWidget(self._editSongBtn)
        self._moreButtonsLayout.addWidget(self._editCoverBtn)
        self._moreButtonsLayout.addWidget(self._deleteBtn)

        self._mainLayout.addWidget(self._mainButtons)
        self._mainLayout.addWidget(self._moreButtons)

    def _connectSignalSlots(self) -> None:
        self._moreBtn.clicked.connect(lambda: self.__showMoreButtons(True))
        self._closeMenuBtn.clicked.connect(lambda: self.__showMoreButtons(False))

        self._playBtn.clicked.connect(lambda: self.__playCurrentSong())
        self._loveBtn.clicked.connect(lambda: self.__song.changeLoveState(self._loveBtn.isActive()))
        self._editCoverBtn.clicked.connect(lambda: self.__changeCover())

        self.__song.loved.connect(lambda loved: self._loveBtn.setActive(loved))
        self.__song.coverChanged.connect(lambda cover: self._cover.setCover(CoverProps.fromBytes(cover, width=64, height=64, radius=12)))

    def content(self) -> Song:
        return self.__song

    def __showMoreButtons(self, a0: bool) -> None:
        self._mainButtons.setVisible(not a0)
        self._moreButtons.setVisible(a0)
        self._closeMenuBtn.setVisible(a0)
        if a0:
            menuCorner = self._moreButtons.geometry().topRight()
            self._closeMenuBtn.move(menuCorner.x() - self._closeMenuBtn.width() - 4, menuCorner.y() + 4)
            self._closeMenuBtn.raise_()

    def __playCurrentSong(self) -> None:
        musicPlayer.loadPlaylist(appCenter.currentPlaylist.getSongs())
        musicPlayer.playSong(self.__song)

    def __displaySongInfo(self, song: Song) -> None:
        if song.isCoverLoaded() and Widgets.isInView(self):
            self._cover.setCover(CoverProps.fromBytes(song.getCover(), width=64, height=64, radius=12))

        self._titleLabel.setDefaultText(song.getTitle())
        self._artistLabel.setDefaultText(song.getArtist())
        self._lengthLabel.setDefaultText(Times.toString(song.getLength()))
        self._loveBtn.setActive(song.isLoved())

    def __changeCover(self) -> None:
        path = QFileDialog.getOpenFileName(self, filter=FileType.IMAGE)[0]
        if path is None or path == '':
            return
        try:
            coverData = Bytes.fromFile(path)
            coverProps = CoverProps.fromBytes(coverData, 320, 320, radius=16)
            self.__song.changeCover(Pixmaps.toBytes(coverProps.content()))
        except Exception as e:
            Logger.error(e)
            Dialogs.alert(message="Something is wrong when saving your cover. Please try again.")

    def loadCover(self) -> None:
        self.__song.loadCover()
