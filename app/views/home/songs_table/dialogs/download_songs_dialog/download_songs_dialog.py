from PyQt5.QtCore import Qt

from app.components.base import Cover, LabelWithDefaultText, Factory, Input, ActionButton, CoverProps
from app.components.dialogs import BaseDialog
from app.resource.qt import Images
from app.views.home.songs_table.dialogs.download_songs_dialog.download_songs_menu import DownloadSongsMenu


class DownloadSongsDialog(BaseDialog):

    def __init__(self):
        super().__init__()
        super()._initComponent()

    def _createUI(self) -> None:
        super()._createUI()
        self.setFixedWidth(640)
        self.setContentsMargins(24, 24, 24, 12)

        self._image = Cover()
        self._image.setAlignment(Qt.AlignHCenter)
        self._image.setFixedHeight(156)
        self._image.setCover(CoverProps.fromBytes(Images.DOWNLOAD, width=128))

        self._header = LabelWithDefaultText()
        self._header.setFont(Factory.createFont(family="Segoe UI Semibold", size=16, bold=True))
        self._header.setAlignment(Qt.AlignCenter)
        self._header.setText("Download Youtube Song")
        self._header.setClassName("text-black dark:text-white")

        self._input = Input()
        self._input.setFont(Factory.createFont(size=12))
        self._input.setFixedHeight(48)
        self._input.setClassName("px-12 rounded-4 border-1 border-primary-12 bg-primary-4")

        self._downloadBtn = ActionButton()
        self._downloadBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=11))
        self._downloadBtn.setClassName("text-white rounded-4 bg-primary-75 bg-primary py-8")
        self._downloadBtn.setText("Download")

        self._menu = DownloadSongsMenu()
        self._menu.setClassName("scroll/bg-primary-50 scroll/hover:bg-primary scroll/rounded-2")
        self._menu.applyTheme()

        self.addWidget(self._image)
        self.addWidget(self._header)
        self.addSpacing(4)
        self.addWidget(self._input)
        self.addSpacing(8)
        self.addWidget(self._downloadBtn)
        self.addSpacing(12)
        self.addWidget(self._menu)

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()
        self._downloadBtn.clicked.connect(lambda: self.__downloadSong())

    def __height(self):
        return self._mainView.sizeHint().height() + self._menuOuter.sizeHint().height()

    def show(self) -> None:
        self.applyTheme()
        super().show()

    def applyLightMode(self) -> None:
        super().applyLightMode()
        super().applyThemeToChildren()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        super().applyThemeToChildren()

    def __downloadSong(self) -> None:
        item = self._menu.addItem()
        item.download(self._input.text().strip())
