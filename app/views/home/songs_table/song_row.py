from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from app.components.base import Component, Cover, Factory, LabelWithDefaultText
from app.components.widgets import BackgroundWidget
from app.helpers.stylesheets import Paddings, Colors
from app.resource.qt import Icons


class SongRow(BackgroundWidget, Component):
    def __init__(self, parent: Optional[QWidget] = None):
        self.defaultArtist = ""

        super().__init__(parent)
        super()._initComponent()
        
        self.setClassName("bg-none hover:bg-primary-12 rounded-12")

    def _createUI(self) -> None:
        self._mainLayout = QHBoxLayout()
        self._mainLayout.setContentsMargins(20, 12, 20, 12)
        self._mainLayout.setSpacing(0)
        self._mainLayout.setAlignment(Qt.AlignLeft)
        self.setLayout(self._mainLayout)

        # ================================================= INFO  =================================================

        self._cover = Cover(self)
        self._cover.setFixedSize(64, 64)

        self._labelTitle = LabelWithDefaultText()
        self._labelTitle.enableEllipsis()
        self._labelTitle.setFixedWidth(188)
        self._labelTitle.setFont(Factory.createFont(size=10))

        self._labelArtist = LabelWithDefaultText()
        self._labelArtist.enableEllipsis()
        self._labelArtist.setFixedWidth(128)
        self._labelArtist.setFont(Factory.createFont(size=10))

        self._labelLength = LabelWithDefaultText()
        self._labelLength.enableEllipsis()
        self._labelLength.setFixedWidth(64)
        self._labelLength.setFont(Factory.createFont(size=10))

        self._info = QHBoxLayout()
        self._info.setSpacing(24)
        self._info.setContentsMargins(0, 8, 0, 8)
        self._info.addWidget(self._cover)
        self._info.addWidget(self._labelTitle, 1)
        self._info.addWidget(self._labelArtist, 1)
        self._info.addWidget(self._labelLength)
        self._mainLayout.addLayout(self._info)

        # ============================================ REACT BUTTONS # ============================================
        self._btnMore = Factory.createIconButton(size=Icons.LARGE, padding=Paddings.RELATIVE_50)
        self._btnMore.setLightModeIcon(Icons.MORE.withColor(Colors.PRIMARY))
        self._btnMore.setDarkModeIcon(Icons.MORE.withColor(Colors.WHITE))
        self._btnMore.setClassName("hover:bg-primary-25 rounded-full", "dark:bg-primary dark:hover:bg-primary")

        self._btnLove = Factory.createToggleButton(Icons.LARGE, Paddings.RELATIVE_50)
        self._btnLove.setActiveIcon(Icons.LOVE.withColor(Colors.DANGER))
        self._btnLove.setInactiveIcon(Icons.LOVE.withColor(Colors.GRAY))
        self._btnLove.setClassName("rounded-full bg-none active/hover:bg-danger-12 inactive/hover:bg-gray-12")

        self._btnPlay = Factory.createIconButton(size=Icons.LARGE, padding=Paddings.RELATIVE_50)
        self._btnPlay.setLightModeIcon(Icons.PLAY.withColor(Colors.PRIMARY))
        self._btnPlay.setDarkModeIcon(Icons.PLAY.withColor(Colors.WHITE))
        self._btnPlay.setClassName("hover:bg-primary-25 bg-primary-10 rounded-full", "dark:bg-primary dark:hover:bg-primary")

        self._buttons = QWidget()
        self._buttonsLayout = QHBoxLayout(self._buttons)
        self._buttonsLayout.setContentsMargins(8, 8, 8, 8)
        self._buttonsLayout.setSpacing(8)
        self._buttonsLayout.addWidget(self._btnMore)
        self._buttonsLayout.addWidget(self._btnLove)
        self._buttonsLayout.addWidget(self._btnPlay)
        self._mainLayout.addWidget(self._buttons)
