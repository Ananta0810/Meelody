from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QShortcut

from app.common.models import Song
from app.components.base import Cover, CoverProps, Factory, ActionButton, Label, Input
from app.components.dialogs import BaseDialog
from app.components.widgets import Box
from app.resource.qt import Images


class UpdateSongDialog(BaseDialog):

    def __init__(self, song: Song) -> None:
        self.__song = song
        super().__init__()
        super()._initComponent()

    def _createUI(self) -> None:
        super()._createUI()

        self._image = Cover()
        self._image.setAlignment(Qt.AlignHCenter)
        self._image.setDefaultCover(CoverProps.fromBytes(Images.EDIT, width=128))

        self._header = Label()
        self._header.setFont(Factory.createFont(family="Segoe UI Semibold", size=16, bold=True))
        self._header.setClassName("text-black dark:text-white bg-none")
        self._header.setAlignment(Qt.AlignCenter)
        self._header.setText("Update Song")

        self._titleLabel = Label()
        self._titleLabel.setFont(Factory.createFont(size=11))
        self._titleLabel.setClassName("text-black dark:text-white bg-none")
        self._titleLabel.setText("Title")

        self._titleInput = Input()
        self._titleInput.setFont(Factory.createFont(size=12))
        self._titleInput.setClassName("px-12 py-8 rounded-4 border-1 border-primary-12 bg-primary-4")

        self._artistLabel = Label()
        self._artistLabel.setFont(Factory.createFont(size=11))
        self._artistLabel.setClassName("text-black dark:text-white bg-none")
        self._artistLabel.setText("Artist")

        self._artistInput = Input()
        self._artistInput.setFont(Factory.createFont(size=12))
        self._artistInput.setClassName("px-12 py-8 rounded-4 border-1 border-primary-12 bg-primary-4")

        self._acceptBtn = ActionButton()
        self._acceptBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=11))
        self._acceptBtn.setClassName("text-white rounded-4 bg-primary-75 bg-primary py-8 disabled:bg-gray-10 disabled:text-gray")
        self._acceptBtn.setText("Apply")
        self._acceptBtn.setDisabled(True)

        self._mainView = QWidget()
        self._mainView.setContentsMargins(12, 4, 12, 12)

        self._viewLayout = Box(self._mainView)
        self._viewLayout.setSpacing(8)
        self._viewLayout.setAlignment(Qt.AlignVCenter)
        self._viewLayout.addWidget(self._image)
        self._viewLayout.addWidget(self._header)
        self._viewLayout.addWidget(self._titleLabel)
        self._viewLayout.addWidget(self._titleInput)
        self._viewLayout.addWidget(self._artistLabel)
        self._viewLayout.addWidget(self._artistInput)
        self._viewLayout.addWidget(self._acceptBtn)

        self.addWidget(self._mainView)
        self.setFixedWidth(480 + 24 * 2)

    def applyLightMode(self) -> None:
        super().applyLightMode()
        super().applyThemeToChildren()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        super().applyThemeToChildren()

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()
        self._acceptBtn.clicked.connect(self._updateSong)

    def _assignShortcuts(self) -> None:
        super()._assignShortcuts()
        acceptShortcut = QShortcut(QKeySequence(Qt.Key_Return), self._acceptBtn)
        acceptShortcut.activated.connect(self._acceptBtn.click)

    def __checkValid(self, title: str) -> None:
        pass

    def _updateSong(self) -> None:
        pass

    def show(self) -> None:
        self.moveToCenter()
        self.applyTheme()
        super().show()
