from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from modules.statics.view.Material import Images
from modules.views.body.PlaylistInfoView import PlaylistInfoView


class CurrentPlaylistView(QWidget):
    main_layout: QHBoxLayout
    info: PlaylistInfoView

    def __init__(self, parent: Optional["QWidget"] = None):
        super(CurrentPlaylistView, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignLeft)
        self.main_layout.setSpacing(50)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.info = PlaylistInfoView()
        self.info.set_default_cover(Images.DEFAULT_PLAYLIST_COVER)

        self.main_layout.addLayout(self.info)

    def apply_light_mode(self) -> None:
        self.info.apply_light_mode()

    def apply_dark_mode(self) -> None:
        self.info.apply_dark_mode()

    def set_current_playlist_info(self, name: str, total_song: int, cover: bytes = None) -> None:
        if cover is None:
            cover = (
                Images.FAVOURITES_PLAYLIST_COVER
                if name.lower() == "favourites"
                else Images.DEFAULT_PLAYLIST_COVER
            )

        self.info.set_cover(cover)
        self.info.set_title(name)
        self.info.set_total_song(total_song)
