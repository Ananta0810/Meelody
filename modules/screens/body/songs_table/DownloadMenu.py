from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea

from modules.helpers.types.Decorators import override
from modules.screens.AbstractScreen import BaseView
from modules.screens.body.songs_table.DownloadSongRow import DownloadRow
from modules.statics.view.Material import Backgrounds
from modules.widgets.ScrollAreas import SmoothVerticalScrollArea


class DownloadMenu(QScrollArea, BaseView):
    __menu: QVBoxLayout

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)
        self._items: list[DownloadRow] = []
        self.__init_ui()
        self.setFixedHeight(0)

    def __init_ui(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.__inner = QWidget(self)
        self.__inner.setStyleSheet(Backgrounds.TRANSPARENT.to_stylesheet())
        self.setWidget(self.__inner)
        self.__menu = QVBoxLayout(self.__inner)
        self.__menu.setAlignment(Qt.AlignTop)
        self.__menu.setSpacing(8)
        self.__menu.setContentsMargins(0, 0, 0, 0)

    @override
    def apply_light_mode(self) -> None:
        self.setStyleSheet(SmoothVerticalScrollArea.build_style(background=Backgrounds.CIRCLE_PRIMARY))
        for item in self._items:
            item.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.setStyleSheet(SmoothVerticalScrollArea.build_style(background=Backgrounds.CIRCLE_PRIMARY))
        for item in self._items:
            item.apply_dark_mode()

    def set_progress_at(self, index: int, value: float) -> None:
        self._items[index].set_progress(value)

    def set_description_at(self, index: int, value: str) -> None:
        self._items[index].set_description(value)

    def add(self, title: str) -> None:
        row = DownloadRow()
        row.set_label(title)
        row.setFixedHeight(64)
        row.apply_light_mode()
        self._items.append(row)
        self.__menu.addWidget(row)
        self.setFixedHeight(min(len(self._items), 3) * 64)
