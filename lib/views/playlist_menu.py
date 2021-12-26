from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from .playlist_table_body import PlaylistTableBody
from .playlist_table_header import PlaylistTableHeader


class PlaylistTable(QWidget):
    def __init__(self, parent: Optional["QWidget"] = None) -> None:
        super().__init__(parent)
        self.setupUI()

    def setupUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.header = PlaylistTableHeader()
        self.header.setFixedHeight(64)
        self.body = PlaylistTableBody()

        self.mainLayout.addWidget(self.header)
        self.mainLayout.addWidget(self.body, 1)

    def lightMode(self) -> None:
        self.header.lightMode()
        self.body.lightMode()

    def darkMode(self) -> None:
        self.header.darkMode()
        self.body.darkMode()

    def connectSignalsToController(self, controller):
        self.body.connectSignalsToController(controller)
