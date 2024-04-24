from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from app.components.base import Factory, EllipsisLabel


class SongsTableHeader(QWidget):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._scrollBarWidth = 4
        self.__initUI()
        
        self._labelTrack.setText("TRACK")
        self._labelArtist.setText("ARTIST")
        self._labelLength.setText("LENGTH")

    def __initUI(self) -> None:
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._mainLayout = QHBoxLayout(self)
        self._mainLayout.setContentsMargins(28, 0, 28 + self._scrollBarWidth, 0)
        self._mainLayout.setSpacing(0)

        self._labelTrack = EllipsisLabel()
        self._labelTrack.setFont(Factory.createFont(size=9))

        self._labelTrack.setFixedWidth(64)
        self._labelTrack.setAlignment(Qt.AlignCenter)

        self._labelArtist = EllipsisLabel()
        self._labelArtist.setFont(Factory.createFont(size=9))

        self._labelArtist.setFixedWidth(128)

        self._labelLength = EllipsisLabel()
        self._labelLength.setFont(Factory.createFont(size=9))

        self._labelLength.setFixedWidth(64)
        self._labelLength.setAlignment(Qt.AlignCenter)

        self._mainLayout.addWidget(self._labelTrack)
        self._mainLayout.addStretch(1)
        self._mainLayout.addSpacing(24)
        self._mainLayout.addWidget(self._labelArtist, 1)
        self._mainLayout.addWidget(self._labelLength)
