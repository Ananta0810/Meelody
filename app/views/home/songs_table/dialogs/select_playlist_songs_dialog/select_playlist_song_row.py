from typing import Optional

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, Qt

from app.common.models import Song
from app.components.base import Factory, CoverProps, CheckBox, CoverWithPlaceHolder, Label, EllipsisLabel
from app.components.widgets import ExtendableStyleWidget, FlexBox
from app.helpers.others import Times
from app.resource.qt import Images, Cursors


class SongRow(ExtendableStyleWidget):
    checked = pyqtSignal(Song)
    unchecked = pyqtSignal(Song)

    def __init__(self, song: Song):
        self.__song = song

        super().__init__()
        super()._initComponent()

        self.__displaySongInfo()

    def _createUI(self) -> None:
        self.setCursor(Cursors.HAND)
        self.setContentsMargins(0, 0, 0, 0)

        self._mainLayout = FlexBox()
        self._mainLayout.setContentsMargins(0, 8, 0, 8)
        self._mainLayout.setSpacing(0)
        self._mainLayout.setAlignment(Qt.AlignHCenter | Qt.AlignLeft)
        self.setLayout(self._mainLayout)

        # ================================================= INFO  =================================================

        self._checkBox = CheckBox()
        self._checkBox.setFixedWidth(16)

        self._cover = CoverWithPlaceHolder(self)
        self._cover.setFixedSize(64, 64)
        self._cover.setPlaceHolderCover(CoverProps.fromBytes(Images.DEFAULT_SONG_COVER, width=64, height=64, radius=12))

        self._titleLabel = EllipsisLabel()
        self._titleLabel.setFixedWidth(200)
        self._titleLabel.setFont(Factory.createFont(size=10))
        self._titleLabel.setClassName("text-black dark:text-white")

        self._artistLabel = EllipsisLabel()
        self._artistLabel.setFixedWidth(128)
        self._artistLabel.setFont(Factory.createFont(size=10))
        self._artistLabel.setClassName("text-gray")

        self._lengthLabel = Label()
        self._lengthLabel.setFixedWidth(64)
        self._lengthLabel.setFont(Factory.createFont(size=10))
        self._lengthLabel.setClassName("text-gray")

        self._mainLayout.addSpacing(24)
        self._mainLayout.addWidget(self._checkBox)
        self._mainLayout.addSpacing(24)
        self._mainLayout.addWidget(self._cover)
        self._mainLayout.addSpacing(24)
        self._mainLayout.addWidget(self._titleLabel)
        self._mainLayout.addSpacing(24)
        self._mainLayout.addWidget(self._artistLabel)
        self._mainLayout.addSpacing(24)
        self._mainLayout.addWidget(self._lengthLabel)

    def _connectSignalSlots(self) -> None:
        self._checkBox.checked.connect(lambda: self.checked.emit(self.__song))
        self._checkBox.unchecked.connect(lambda: self.unchecked.emit(self.__song))

    def __displaySongInfo(self) -> None:
        self._cover.setCover(CoverProps.fromBytes(self.__song.getCover(), width=64, height=64, radius=12))
        self._titleLabel.setText(self.__song.getTitle())
        self._artistLabel.setText(self.__song.getArtist())
        self._lengthLabel.setText(Times.toString(self.__song.getLength()))
        self._checkBox.setFixedHeight(self.sizeHint().height())

    def mousePressEvent(self, a0: Optional[QtGui.QMouseEvent]) -> None:
        super().mousePressEvent(a0)
        self._checkBox.nextCheckState()

    def select(self) -> None:
        self._checkBox.setCheckState(True)
