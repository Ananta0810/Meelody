from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from app.common.others import appCenter
from app.components.base import Cover, LabelWithDefaultText, Factory, Input, ActionButton, CoverProps, Component
from app.components.dialogs import BaseDialog
from app.resource.qt import Images


class DownloadSongsDialog(BaseDialog):

    def __init__(self):
        super().__init__()
        super()._initComponent()

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
        self._downloadBtn.setClassName("text-white rounded-4 bg-danger-75 bg-danger")

        self._menuOuter = QWidget()
        self._menuOuter.setContentsMargins(24, 12, 24, 24)
        # layout = QVBoxLayout(self._menuOuter)
        # layout.setContentsMargins(0, 0, 0, 0)
        # self._menu = DownloadMenu()
        # layout.addWidget(self._menu)

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
        super().show()
        children = self.findChildren(Component)
        if appCenter.isLightMode:
            self.applyLightMode()
            for component in children:
                component.applyLightMode()
        else:
            self.applyDarkMode()
            for component in children:
                component.applyDarkMode()
