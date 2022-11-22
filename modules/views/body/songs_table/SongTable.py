from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from modules.views.body.songs_table.SongTableBody import SongTableBody
from modules.views.body.songs_table.SongTableHeader import SongTableHeader


class SongTable(QWidget):
    main_layout: QVBoxLayout
    header: SongTableHeader
    body: SongTableBody

    def __init__(self, parent: Optional["QWidget"] = None) -> None:
        super().__init__(parent)
        self.setup_ui()
        self.header.set_text()

    def setup_ui(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.header = SongTableHeader()
        self.header.setFixedHeight(48)

        self.main_layout.addWidget(self.header)
        self.main_layout.addStretch(1)

    def apply_light_mode(self) -> None:
        self.header.apply_light_mode()

    def apply_dark_mode(self) -> None:
        self.header.apply_dark_mode()