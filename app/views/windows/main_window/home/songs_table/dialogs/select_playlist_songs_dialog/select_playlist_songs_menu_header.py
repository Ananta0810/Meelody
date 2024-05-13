from typing import Optional

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from app.common.others import translator
from app.components.base import FontFactory
from app.components.labels import Label
from app.components.widgets import ExtendableStyleWidget, FlexBox


class MenuHeader(ExtendableStyleWidget):

    def __init__(self, parent: Optional[QWidget] = None):
        self._scrollBarWidth = 4

        super().__init__(parent)
        self._initComponent()

    def _createUI(self) -> None:
        self._mainLayout = FlexBox(self)
        self._mainLayout.setContentsMargins(0, 0, self._scrollBarWidth, 0)

        self._titleLabel = Label()
        self._titleLabel.setFixedWidth(64)
        self._titleLabel.setAlignment(Qt.AlignCenter)
        self._titleLabel.setFont(FontFactory.create(size=9))
        self._titleLabel.setClassName("text-black dark:text-white bg-none")

        self._artistLabel = Label()
        self._artistLabel.setFixedWidth(128)
        self._artistLabel.setAlignment(Qt.AlignLeft)
        self._artistLabel.setFont(FontFactory.create(size=9))
        self._artistLabel.setClassName("text-black dark:text-white bg-none")

        self._lengthLabel = Label()
        self._lengthLabel.setAlignment(Qt.AlignLeft)
        self._lengthLabel.setFont(FontFactory.create(size=9))
        self._lengthLabel.setClassName("text-black dark:text-white bg-none")

        self._mainLayout.addSpacing(64)
        self._mainLayout.addWidget(self._titleLabel)
        self._mainLayout.addSpacing(24)
        self._mainLayout.addSpacing(200)
        self._mainLayout.addSpacing(24)
        self._mainLayout.addWidget(self._artistLabel)
        self._mainLayout.addSpacing(24)
        self._mainLayout.addWidget(self._lengthLabel)
        self._mainLayout.addStretch()

    def translateUI(self) -> None:
        self._titleLabel.setText(translator.translate("SELECT_PLAYLIST_SONGS_DIALOG.HEADER.TITLE"))
        self._artistLabel.setText(translator.translate("SELECT_PLAYLIST_SONGS_DIALOG.HEADER.ARTIST"))
        self._lengthLabel.setText(translator.translate("SELECT_PLAYLIST_SONGS_DIALOG.HEADER.TIME"))

    def showEvent(self, a0: Optional[QtGui.QShowEvent]) -> None:
        super().showEvent(a0)
        self.translateUI()
