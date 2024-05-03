from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from app.components.base import Label, Factory
from app.components.widgets import ExtendableStyleWidget, FlexBox


class MenuHeader(ExtendableStyleWidget):

    def __init__(self, parent: Optional[QWidget] = None):
        self._scrollBarWidth = 4

        super().__init__(parent)
        self._initComponent()

        self._titleLabel.setText("TITLE")
        self._artistLabel.setText("ARTIST")
        self._lengthLabel.setText("TIME")

    def _createUI(self) -> None:
        self._mainLayout = FlexBox(self)
        self._mainLayout.setContentsMargins(0, 0, self._scrollBarWidth, 0)

        self._titleLabel = Label()
        self._titleLabel.setFixedWidth(64)
        self._titleLabel.setAlignment(Qt.AlignCenter)
        self._titleLabel.setFont(Factory.createFont(size=9))
        self._titleLabel.setClassName("text-black dark:text-white bg-none")

        self._artistLabel = Label()
        self._artistLabel.setFixedWidth(128)
        self._artistLabel.setAlignment(Qt.AlignLeft)
        self._artistLabel.setFont(Factory.createFont(size=9))
        self._artistLabel.setClassName("text-black dark:text-white bg-none")

        self._lengthLabel = Label()
        self._lengthLabel.setAlignment(Qt.AlignLeft)
        self._lengthLabel.setFont(Factory.createFont(size=9))
        self._lengthLabel.setClassName("text-black dark:text-white bg-none")

        self._mainLayout.addSpacing(44)
        self._mainLayout.addWidget(self._titleLabel)
        self._mainLayout.addSpacing(24 + 200)
        self._mainLayout.addWidget(self._artistLabel)
        self._mainLayout.addWidget(self._lengthLabel)
        self._mainLayout.addStretch()
