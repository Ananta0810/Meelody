from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from app.components.base import Factory, EllipsisLabel


class SongsTableHeader(QWidget):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._scrollBarWidth = 4
        self.__initUI()

        self._trackLabel.setText("TRACK")
        self._artistLabel.setText("ARTIST")
        self._lengthLabel.setText("LENGTH")

    def __initUI(self) -> None:
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._mainLayout = QHBoxLayout(self)
        self._mainLayout.setContentsMargins(28, 0, 28 + self._scrollBarWidth, 0)
        self._mainLayout.setSpacing(0)

        self._trackLabel = EllipsisLabel()
        self._trackLabel.setFont(Factory.createFont(size=9))

        self._trackLabel.setFixedWidth(64)
        self._trackLabel.setAlignment(Qt.AlignCenter)

        self._artistLabel = EllipsisLabel()
        self._artistLabel.setFont(Factory.createFont(size=9))

        self._artistLabel.setFixedWidth(128)

        self._lengthLabel = EllipsisLabel()
        self._lengthLabel.setFont(Factory.createFont(size=9))

        self._lengthLabel.setFixedWidth(64)
        self._lengthLabel.setAlignment(Qt.AlignCenter)

        self._mainLayout.addWidget(self._trackLabel)
        self._mainLayout.addStretch(1)
        self._mainLayout.addSpacing(24)
        self._mainLayout.addWidget(self._artistLabel, 1)
        self._mainLayout.addWidget(self._lengthLabel)
