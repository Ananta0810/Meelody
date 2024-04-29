from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QResizeEvent
from PyQt5.QtWidgets import QWidget, QShortcut

from app.components.base import Cover, CoverProps, Factory, Input, ActionButton
from app.components.dialogs import BaseDialog
from app.components.widgets import Box
from app.resource.qt import Images


class NewPlaylistDialog(BaseDialog):

    def __init__(self):
        super().__init__()
        super()._initComponent()
        self.applyTheme()

    def _createUI(self) -> None:
        super()._createUI()

        self._cover = Cover()
        self._cover.setFixedSize(320, 320)
        self._cover.setDefaultCover(CoverProps.fromBytes(Images.DEFAULT_PLAYLIST_COVER, 320, 320, radius=16))

        self._titleInput = Input()
        self._titleInput.setFont(Factory.createFont(size=12))
        self._titleInput.setFixedSize(320, 48)
        self._titleInput.setClassName("px-12 rounded-4 border-1 border-primary-12 bg-primary-4")
        self._titleInput.setPlaceholderText("Name...")

        self._acceptBtn = ActionButton()
        self._acceptBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=11))
        self._acceptBtn.setClassName("text-white rounded-4 bg-primary-75 bg-primary py-8")
        self._acceptBtn.setText("Add Playlist")

        self._mainView = QWidget()
        self._mainView.setContentsMargins(12, 4, 12, 12)

        self._viewLayout = Box(self._mainView)
        self._viewLayout.setAlignment(Qt.AlignVCenter)
        self._viewLayout.addWidget(self._cover)
        self._viewLayout.addSpacing(8)
        self._viewLayout.addWidget(self._titleInput)
        self._viewLayout.addSpacing(8)
        self._viewLayout.addWidget(self._acceptBtn)

        self.addWidget(self._mainView)

        self._editCoverBtn = ActionButton(self._mainView)
        self._editCoverBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=9))
        self._editCoverBtn.setClassName("text-white rounded-4 bg-primary-75 bg-primary py-8")
        self._editCoverBtn.setText("Choose cover")

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        margin = self._mainView.contentsMargins()
        self._editCoverBtn.move(
            self._cover.x() + self._cover.width() - self._editCoverBtn.width() - 8 + margin.right(),
            self._cover.y() + 8 + margin.top(),
        )

    def applyLightMode(self) -> None:
        super().applyLightMode()
        super().applyThemeToChildren()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        super().applyThemeToChildren()

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()

    def _assignShortcuts(self) -> None:
        super()._assignShortcuts()
        acceptShortcut = QShortcut(QKeySequence(Qt.Key_Return), self._acceptBtn)
        acceptShortcut.activated.connect(self._acceptBtn.click)
