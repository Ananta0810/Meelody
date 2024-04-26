from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QHBoxLayout, QShortcut

from app.components.base import Component, Factory
from app.components.windows import FramelessWindow
from app.helpers.stylesheets import Paddings, Colors
from app.resource.qt import Icons


class BaseDialog(FramelessWindow, Component):
    closed: pyqtSignal() = pyqtSignal()

    def __init__(self):
        super().__init__()

    def _createUI(self) -> None:
        self.setWindowModality(Qt.ApplicationModal)
        self.setClassName("rounded-12 bg-white dark:bg-dark")

        self._btnClose = Factory.createIconButton(Icons.MEDIUM, Paddings.RELATIVE_50)
        self._btnClose.setLightModeIcon(Icons.CLOSE.withColor(Colors.GRAY))
        self._btnClose.setClassName("bg-gray-12 hover:bg-gray-25 rounded-8")

        self._layout = QHBoxLayout()
        self.addLayout(self._layout)

        self._layout.addStretch(1)
        self._layout.addWidget(self._btnClose)
        self._layout.setContentsMargins(8, 8, 8, 0)

    def _connectSignalSlots(self) -> None:
        self._btnClose.clicked.connect(self.close)
        self._btnClose.clicked.connect(lambda: self.closed.emit())

    def _assignShortcuts(self) -> None:
        cancelShortcut = QShortcut(QKeySequence(Qt.Key_Escape), self._btnClose)
        cancelShortcut.activated.connect(self._btnClose.click)

    def setFixedWidth(self, w: int) -> None:
        super().setFixedWidth(w)
        self._btnClose.move(w - self._btnClose.width() - 4, 4)

    def setFixedHeight(self, h: int) -> None:
        super().setFixedHeight(h)
        self.moveToCenter()
