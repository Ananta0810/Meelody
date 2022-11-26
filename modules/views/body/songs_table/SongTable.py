from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from modules.helpers.types.Decorators import override
from modules.views.ViewComponent import ViewComponent
from modules.views.body.songs_table.SongTableBody import SongTableBody
from modules.views.body.songs_table.SongTableHeader import SongTableHeader


class SongTable(QWidget, ViewComponent):
    __main_layout: QVBoxLayout
    __header: SongTableHeader
    __body: SongTableBody

    def __init__(self, parent: Optional["QWidget"] = None) -> None:
        super().__init__(parent)
        self.setup_ui()
        self.__header.setText()
        self.__body.add_new_song()
        self.__body.add_new_song()
        self.__body.add_new_song()
        self.__body.add_new_song()
        self.__body.add_new_song()
        self.__body.add_new_song()
        self.__body.add_new_song()

    def setup_ui(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.__main_layout = QVBoxLayout(self)
        self.__main_layout.setSpacing(4)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.__header = SongTableHeader()
        self.__header.setFixedHeight(48)

        self.__body = SongTableBody()

        self.__main_layout.addWidget(self.__header)
        self.__main_layout.addWidget(self.__body)

    @override
    def apply_light_mode(self) -> None:
        self.__header.apply_light_mode()
        self.__body.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.__header.apply_dark_mode()
        self.__body.apply_dark_mode()