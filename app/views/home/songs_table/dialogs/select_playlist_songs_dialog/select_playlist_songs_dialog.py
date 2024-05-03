from app.common.models import Playlist
from app.components.dialogs import BaseDialog
from app.views.home.songs_table.dialogs.select_playlist_songs_dialog.menu_header import MenuHeader


class SelectPlaylistSongsDialog(BaseDialog):

    def __init__(self, playlist: Playlist) -> None:
        self.__playlist = playlist

        super().__init__()
        super()._initComponent()

    def _createUI(self) -> None:
        super()._createUI()
        self.setFixedWidth(720)
        self.setContentsMargins(20, 20, 20, 20)

        self._menuHeader = MenuHeader()
        self._menuHeader.setContentsMargins(0, 16, 0, 16)
        self._menuHeader.setClassName("bg-gray-8 border-1 border-gray-12 rounded-t-8")
        self.addWidget(self._menuHeader)

    def applyLightMode(self) -> None:
        super().applyLightMode()
        super().applyThemeToChildren()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        super().applyThemeToChildren()

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()

    def show(self) -> None:
        self.moveToCenter()
        self.applyTheme()
        super().show()
