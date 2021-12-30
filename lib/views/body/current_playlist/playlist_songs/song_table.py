from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from .song_table_body import SongTableBody
from .song_table_header import SongTableHeader


class SongTable(QWidget):
    def __init__(self, parent: Optional["QWidget"] = None) -> None:
        super().__init__(parent)
        self.setupUI()

    def setupUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.header = SongTableHeader()
        self.header.setFixedHeight(48)
        self.body = SongTableBody()

        self.mainLayout.addWidget(self.header)
        self.mainLayout.addWidget(self.body, 1)

    def lightMode(self) -> None:
        self.header.lightMode()
        self.body.lightMode()

    def darkMode(self) -> None:
        self.header.darkMode()
        self.body.darkMode()
