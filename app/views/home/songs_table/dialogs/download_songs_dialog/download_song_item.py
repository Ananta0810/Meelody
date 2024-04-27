from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie, QResizeEvent
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QLabel

from app.components.base import Cover, LabelWithDefaultText, Factory, CoverProps, StateIcon
from app.components.sliders import ProgressBar
from app.components.widgets import ExtendableStyleWidget
from app.helpers.stylesheets import Colors, Paddings
from app.resource.qt import Images, Icons

_downloading = 1
_processing = 2
_finished = 3


class DownloadSongItem(ExtendableStyleWidget):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._initComponent()

        self._state = _downloading
        self._gifMovie: Optional[QMovie] = None
        self._dot: float = 0
        self._frame: int = 0
        self.setProgress(0)

    def _createUI(self) -> None:
        self._cover = Cover()
        self._cover.setFixedSize(48, 48)
        self._cover.setCover(CoverProps.fromBytes(Images.DEFAULT_SONG_COVER, width=48, height=48, radius=8))

        self._labelTitle = LabelWithDefaultText()
        self._labelTitle.setFont(Factory.createFont(size=10, bold=True))
        self._labelTitle.setClassName("text-black dark:text-white")

        self._labelDescription = LabelWithDefaultText()
        self._labelDescription.setFont(Factory.createFont(size=9))
        self._labelDescription.setClassName("text-black dark:text-white")

        self._progressBar = ProgressBar()
        self._progressBar.setFixedHeight(2)
        # self._progressBar.setProgress_style(Backgrounds.CIRCLE_PRIMARY.with_border_radius(1))

        self._infoLayout = QVBoxLayout()
        self._infoLayout.setContentsMargins(0, 0, 0, 0)
        self._infoLayout.setSpacing(4)
        self._infoLayout.addStretch(0)
        self._infoLayout.addWidget(self._labelTitle)
        self._infoLayout.addWidget(self._labelDescription)
        self._infoLayout.addWidget(self._progressBar)
        self._infoLayout.addStretch(0)

        self._icons = QWidget()
        self._icons.setFixedWidth(48)
        self._iconsLayout = QVBoxLayout(self._icons)

        self._resultIcon = Factory.createMultiStatesButton(size=Icons.SMALL, padding=Paddings.RELATIVE_25)
        self._resultIcon.setIcons([StateIcon(Icons.APPLY.withColor(Colors.WHITE)), StateIcon(Icons.CLOSE.withColor(Colors.WHITE))])
        self._resultIcon.keepSpaceWhenHiding()
        self._resultIcon.hide()

        self._gif = QLabel()
        self._gif.setFixedSize(48, 48)

        self._iconsLayout.addWidget(self._gif)
        self._iconsLayout.addWidget(self._resultIcon)

        self._mainLayout = QHBoxLayout()
        self._mainLayout.setSpacing(0)
        self._mainLayout.setSpacing(0)
        self._mainLayout.setAlignment(Qt.AlignLeft)

        self._mainLayout.addWidget(self._cover)
        self._mainLayout.addSpacing(12)
        self._mainLayout.addLayout(self._infoLayout, stretch=1)
        self._mainLayout.addWidget(self._icons)

        self.setLayout(self._mainLayout)
        self.setClassName("bg-transparent")

    def resizeEvent(self, a0: QResizeEvent) -> None:
        super().resizeEvent(a0)

    def setLabel(self, label: str) -> None:
        self._labelTitle.setText(label)

    def setDescription(self, value: str) -> None:
        self._labelDescription.setText(value)

    def setProgress(self, value: float) -> None:
        self._progressBar.set_value(value)
