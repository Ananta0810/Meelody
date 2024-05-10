from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from app.common.models import Song
from app.components.base import Cover, CoverProps, Label, Factory, EllipsisLabel
from app.components.base.gif import Gif
from app.components.widgets import ExtendableStyleWidget, Box, FlexBox
from app.helpers.base import Strings
from app.helpers.stylesheets import Colors, Paddings
from app.resource.qt import Images, Icons


class ImportSongItem(ExtendableStyleWidget):
    songImported = pyqtSignal(str)

    def __init__(self, path: str):
        super().__init__()
        self._initComponent()

        self._path = path
        self._dot: float = 0

        self.__displaySongInfo()

    def _createUI(self) -> None:
        self.setContentsMargins(0, 0, 0, 0)

        self._cover = Cover()
        self._cover.setFixedSize(48, 48)
        self._cover.setCover(CoverProps.fromBytes(Images.DEFAULT_SONG_COVER, width=48, height=48, radius=8))

        self._titleLabel = EllipsisLabel()
        self._titleLabel.setFont(Factory.createFont(size=10))
        self._titleLabel.setClassName("text-black dark:text-white")

        self._descriptionLabel = Label()
        self._descriptionLabel.setFont(Factory.createFont(size=9))
        self._descriptionLabel.setClassName("text-black dark:text-white")

        self._infoLayout = Box()
        self._infoLayout.setSpacing(4)
        self._infoLayout.addStretch(0)
        self._infoLayout.addWidget(self._titleLabel)
        self._infoLayout.addWidget(self._descriptionLabel)
        self._infoLayout.addStretch(0)

        self._successIcon = Factory.createIconButton(size=Icons.SMALL, padding=Paddings.RELATIVE_25)
        self._successIcon.setLightModeIcon(Icons.APPLY.withColor(Colors.WHITE))
        self._successIcon.setClassName("rounded-full bg-success")
        self._successIcon.hide()

        self._failedIcon = Factory.createIconButton(size=Icons.SMALL, padding=Paddings.RELATIVE_25)
        self._failedIcon.setLightModeIcon(Icons.CLOSE.withColor(Colors.WHITE))
        self._failedIcon.setClassName("rounded-full bg-danger")
        self._failedIcon.hide()

        self._importGif = Gif("app/resource/images/defaults/loading-bubble.gif")
        self._importGif.setFixedSize(48, 48)
        self._importGif.hide()

        self._icons = QWidget()
        self._icons.setFixedWidth(48)

        self._iconsLayout = QHBoxLayout(self._icons)
        self._iconsLayout.setAlignment(Qt.AlignRight)
        self._iconsLayout.addWidget(self._importGif)
        self._iconsLayout.addWidget(self._successIcon)
        self._iconsLayout.addWidget(self._failedIcon)

        self._mainLayout = FlexBox()
        self._mainLayout.setSpacing(0)
        self._mainLayout.setAlignment(Qt.AlignLeft)

        self._mainLayout.addWidget(self._cover)
        self._mainLayout.addSpacing(12)
        self._mainLayout.addLayout(self._infoLayout, stretch=1)
        self._mainLayout.addWidget(self._icons)

        self.setLayout(self._mainLayout)

        self.setMaximumHeight(self.sizeHint().height())

    def show(self) -> None:
        super().show()

    def __displaySongInfo(self) -> None:
        song = Song.fromFile(self._path, Strings.sanitizeFileName(Strings.getFileBasename(self._path)))
        song.loadCover()

        self._cover.setCover(CoverProps.fromBytes(song.getCover(), width=48, height=48, radius=9))
        self._titleLabel.setText(Strings.join("   |   ", [song.getTitle(), song.getArtist()]))

    def setDescription(self, value: str) -> None:
        self._descriptionLabel.setText(value)

    def applyLightMode(self) -> None:
        super().applyLightMode()
        super().applyThemeToChildren()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        super().applyThemeToChildren()
