from typing import Union

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence, QResizeEvent
from PyQt5.QtWidgets import QHBoxLayout, QShortcut, QWidget, QLayout

from app.common.statics.qt import Icons
from app.common.statics.styles import Colors
from app.common.statics.styles import Paddings
from app.components.animations import Fade
from app.components.buttons import ButtonFactory
from app.components.widgets import Box
from app.components.windows import FramelessWindow


class BaseDialog(FramelessWindow):
    closed: pyqtSignal() = pyqtSignal()

    def __init__(self):
        super().__init__()

    def _createUI(self) -> None:
        self.setWindowModality(Qt.ApplicationModal)
        self.setClassName("rounded-12 bg-white dark:bg-dark")

        self._btnClose = ButtonFactory.createIconButton(Icons.medium, Paddings.RELATIVE_50)
        self._btnClose.setLightModeIcon(Icons.close.withColor(Colors.gray))
        self._btnClose.setDarkModeIcon(Icons.close.withColor(Colors.white))
        self._btnClose.setClassName("bg-gray-12 hover:bg-gray-25 rounded-8 dark:bg-gray-20 dark:hover:bg-gray-33")

        self._titleBar = QWidget()

        self._titleBarLayout = QHBoxLayout(self._titleBar)
        self._titleBarLayout.setContentsMargins(12, 12, 12, 0)

        self._titleBarLayout.addStretch(1)
        self._titleBarLayout.addWidget(self._btnClose)

        self._body = Box()
        self._body.setContentsMargins(4, 4, 4, 4)
        self._body.setAlignment(Qt.AlignVCenter)

        super().addWidget(self._titleBar)
        super().addLayout(self._body)
        self._animation = Fade(self)

    def _connectSignalSlots(self) -> None:
        self._btnClose.clicked.connect(lambda: self.closed.emit())
        self.closed.connect(lambda: self.closeWithAnimation())

    def _assignShortcuts(self) -> None:
        cancelShortcut = QShortcut(QKeySequence(Qt.Key_Escape), self._btnClose)
        cancelShortcut.activated.connect(lambda: self._btnClose.click())

    def _hideTitleBar(self) -> None:
        self._titleBar.hide()

    def setFixedWidth(self, w: int) -> None:
        super().setFixedWidth(w)
        self._btnClose.move(w - self._btnClose.width() - 4, 4)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.moveToCenter()

    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self._body.setContentsMargins(left, top, right, bottom)

    def addLayout(self, widget: QLayout) -> None:
        self._body.addLayout(widget)

    def addWidget(self, widget: QWidget, stretch: int = None, alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = None) -> None:
        self._body.addWidget(widget, stretch, alignment)

    def addSpacing(self, space: int) -> None:
        self._body.addSpacing(space)

    def applyLightMode(self) -> None:
        super().applyLightMode()
        super().applyThemeToChildren()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        super().applyThemeToChildren()

    def show(self) -> None:
        self.applyTheme()
        self.translateUI()
        self.moveToCenter()
        self.setWindowOpacity(0)
        super().show()
        self._animation.fadeIn()

    def closeWithAnimation(self) -> None:
        self._animation.fadeOut(onFinished=lambda: self.close())
