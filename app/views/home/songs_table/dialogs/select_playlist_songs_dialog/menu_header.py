from typing import Optional

from PyQt5.QtWidgets import QWidget

from app.components.base import Label, Factory
from app.components.widgets import ExtendableStyleWidget, FlexBox


class MenuHeader(ExtendableStyleWidget):

    def __init__(self, parent: Optional[QWidget] = None):
        self._scrollBarWidth = 4

        super().__init__(parent)
        self._initComponent()

        self._trackLabel.setText("TITLE")
        self._artistLabel.setText("ARTIST")
        self._lengthLabel.setText("TIME")

    def _createUI(self) -> None:
        self._mainLayout = FlexBox(self)
        self._mainLayout.setContentsMargins(28, 0, 28 + self._scrollBarWidth, 0)

        self._trackLabel = Label()
        self._trackLabel.setFont(Factory.createFont(size=9))
        self._trackLabel.setClassName("text-black dark:text-white bg-none")

        self._artistLabel = Label()
        self._artistLabel.setFont(Factory.createFont(size=9))
        self._artistLabel.setClassName("text-black dark:text-white bg-none")

        self._lengthLabel = Label()
        self._lengthLabel.setFont(Factory.createFont(size=9))
        self._lengthLabel.setClassName("text-black dark:text-white bg-none")

        self._mainLayout.addWidget(self._trackLabel)
        self._mainLayout.addSpacing(237)
        self._mainLayout.addWidget(self._artistLabel)
        self._mainLayout.addSpacing(114)
        self._mainLayout.addWidget(self._lengthLabel)
        self._mainLayout.addStretch()
