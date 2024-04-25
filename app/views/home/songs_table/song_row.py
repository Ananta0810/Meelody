from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from app.common.models import Song
from app.common.others import musicPlayer
from app.components.base import Cover, Factory, LabelWithDefaultText, CoverProps
from app.components.widgets import ExtendableStyleWidget
from app.helpers.others import Times
from app.helpers.stylesheets import Paddings, Colors
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
        self._mainLayout.setContentsMargins(20, 4, 20, 4)
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
        self._moreBtn.setLightModeIcon(Icons.MORE.withColor(Colors.PRIMARY))
        self._moreBtn.setDarkModeIcon(Icons.MORE.withColor(Colors.WHITE))
        self._moreBtn.setClassName("hover:bg-primary-25 rounded-full", "dark:bg-primary dark:hover:bg-primary")

        self._loveBtn = Factory.createToggleButton(Icons.LARGE, Paddings.RELATIVE_50)
        self._loveBtn.setActiveIcon(Icons.LOVE.withColor(Colors.DANGER))
        self._loveBtn.setInactiveIcon(Icons.LOVE.withColor(Colors.GRAY))
        self._loveBtn.setClassName("rounded-full bg-none active/hover:bg-danger-12 inactive/hover:bg-gray-12")

        self._playBtn = Factory.createIconButton(size=Icons.LARGE, padding=Paddings.RELATIVE_50)
        self._playBtn.setLightModeIcon(Icons.PLAY.withColor(Colors.PRIMARY))
        self._playBtn.setDarkModeIcon(Icons.PLAY.withColor(Colors.WHITE))
        self._playBtn.setClassName("hover:bg-primary-25 bg-primary-10 rounded-full", "dark:bg-primary dark:hover:bg-primary")

        self._buttons = QWidget()
        self._buttonsLayout = QHBoxLayout(self._buttons)
        self._buttonsLayout.setContentsMargins(8, 8, 8, 8)
        self._buttonsLayout.setSpacing(8)
        self._buttonsLayout.addWidget(self._moreBtn)
        self._buttonsLayout.addWidget(self._loveBtn)
        self._buttonsLayout.addWidget(self._playBtn)
        self._mainLayout.addWidget(self._buttons)

    def _connectSignalSlots(self) -> None:
        self._playBtn.clicked.connect(lambda: self.__playCurrentSong())

    def __playCurrentSong(self) -> None:
        musicPlayer.playSong(self.__song)

    def __displaySongInfo(self, song: Song) -> None:
        self._cover.setCover(CoverProps.fromBytes(song.getCover(), width=64, height=64, radius=12))

        self._titleLabel.setDefaultText(song.getTitle())
        self._artistLabel.setDefaultText(song.getArtist())
        self._lengthLabel.setDefaultText(Times.toString(song.getLength()))
        self._loveBtn.setActive(song.isLoved())
