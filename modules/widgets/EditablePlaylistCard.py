from typing import Optional

from PyQt5.QtGui import QFont

from modules.widgets.PlaylistCard import PlaylistCard


class EditablePlaylistCard(PlaylistCard):
    def __init__(self, font: QFont, parent: Optional["QWidget"] = None):
        super().__init__(font, parent)
