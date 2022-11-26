from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from modules.helpers.types.Decorators import override
from modules.statics.view.Material import Images
from modules.views.ViewComponent import ViewComponent
from modules.views.body.PlaylistInfoView import PlaylistInfoView
from modules.views.body.songs_table.SongTable import SongTable


class CurrentPlaylistView(QWidget, ViewComponent):
    __main_layout: QHBoxLayout
    __info: PlaylistInfoView
    __menu: SongTable

    def __init__(self, parent: Optional["QWidget"] = None):
        super(CurrentPlaylistView, self).__init__(parent)
        self.__init_ui()

    def __init_ui(self) -> None:
        self.__main_layout = QHBoxLayout(self)
        self.__main_layout.setAlignment(Qt.AlignLeft)
        self.__main_layout.setSpacing(50)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.__info = PlaylistInfoView()
        self.__info.set_default_cover(Images.DEFAULT_PLAYLIST_COVER)

        self.__menu = SongTable()

        self.__main_layout.addLayout(self.__info)
        self.__main_layout.addWidget(self.__menu, stretch=2)

    @override
    def apply_light_mode(self) -> None:
        self.__info.apply_light_mode()
        self.__menu.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.__info.apply_dark_mode()
        self.__menu.apply_dark_mode()

    def set_current_playlist___info(self, name: str, total_song: int, cover: bytes = None) -> None:
        if cover is None:
            cover = (
                Images.FAVOURITES_PLAYLIST_COVER
                if name.lower() == "favourites"
                else Images.DEFAULT_PLAYLIST_COVER
            )

        self.__info.set_cover(cover)
        self.__info.set_title(name)
        self.__info.set_total_song(total_song)
