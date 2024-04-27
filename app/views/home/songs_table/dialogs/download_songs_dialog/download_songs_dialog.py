from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from app.components.base import Cover, LabelWithDefaultText, Factory, Input, ActionButton, CoverProps
from app.components.dialogs import BaseDialog
from app.components.widgets import StyleWidget
from app.resource.qt import Images
from app.views.home.songs_table.dialogs.download_songs_dialog.download_songs_menu import DownloadSongsMenu


class DownloadSongsDialog(BaseDialog):

    def __init__(self):
        super().__init__()
        super()._initComponent()
        self._menu.addItem()

    def _createUI(self) -> None:
        super()._createUI()

        self._image = Cover()
        self._image.setAlignment(Qt.AlignHCenter)

        self._header = LabelWithDefaultText()
        self._header.setFont(Factory.createFont(family="Segoe UI Semibold", size=16, bold=True))
        self._header.setClassName("text-black dark:text-white")
        self._header.setAlignment(Qt.AlignCenter)

        self._input = Input()
        self._input.setFont(Factory.createFont(size=12))
        self._input.setFixedHeight(48)

        self._downloadBtn = ActionButton()
        self._downloadBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=11))
        self._downloadBtn.setClassName("text-white rounded-4 bg-primary-75 bg-primary")

        self._menuOuter = StyleWidget()
        self._menuOuter.setClassName("bg-none border-none")

        self._menuOuter.setContentsMargins(24, 12, 24, 24)
        self._menuLayout = QVBoxLayout(self._menuOuter)
        self._menuLayout.setContentsMargins(0, 0, 0, 0)
        self._menu = DownloadSongsMenu()
        self._menuLayout.addWidget(self._menu)

        self._mainView = QWidget()
        self._mainView.setContentsMargins(24, 24, 24, 0)

        cover_wrapper_layout = QVBoxLayout()
        self._image.setFixedHeight(156)
        cover_wrapper_layout.addWidget(self._image)

        self._viewLayout = QVBoxLayout(self._mainView)
        self._viewLayout.setContentsMargins(0, 0, 0, 0)
        self._viewLayout.setAlignment(Qt.AlignVCenter)
        self._viewLayout.addLayout(cover_wrapper_layout)
        self._viewLayout.addWidget(self._header)
        self._viewLayout.addSpacing(4)
        self._viewLayout.addWidget(self._input)
        self._viewLayout.addSpacing(8)
        self._viewLayout.addWidget(self._downloadBtn)

        self.addWidget(self._mainView)
        self.addWidget(self._menuOuter)

        self._image.setCover(CoverProps.fromBytes(Images.DOWNLOAD, width=128))
        self._header.setText("Download Youtube Song")
        self._downloadBtn.setText("Download")

        self.setFixedWidth(640)
        self.setFixedHeight(self.__height())

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
