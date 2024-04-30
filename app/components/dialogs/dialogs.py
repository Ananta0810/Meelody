from typing import Optional, final

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut, QDialog, QDesktopWidget, QSizePolicy

from app.components.base import CoverProps, Component, Cover, Factory, LabelWithDefaultText, ActionButton, Label
from app.components.widgets import Box, StyleWidget, FlexBox
from app.helpers.base import Numbers
from app.resource.qt import Images


class _ConfirmDialog(QDialog, Component):
    canceled: pyqtSignal() = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._initComponent()
        self.applyTheme()

    def _createUI(self) -> None:
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowModality(Qt.ApplicationModal)

        self._inner = StyleWidget(self)
        self._inner.setContentsMargins(24, 24, 24, 24)
        self._inner.setClassName("rounded-12 bg-white dark:bg-dark")

        self._header = Label()
        self._header.setFont(Factory.createFont(family="Segoe UI Semibold", size=16, bold=True))
        self._header.setClassName("text-black dark:text-white")
        self._header.setAlignment(Qt.AlignLeft)

        self._message = Label()
        self._message.setFont(Factory.createFont(size=10))
        self._message.setClassName("text-black dark:text-white")
        self._message.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._acceptBtn = ActionButton()
        self._acceptBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=11))
        self._acceptBtn.setClassName("text-white rounded-4 bg-black-90 hover:bg-black py-8 px-24")
        self._acceptBtn.setMinimumWidth(64)

        self._cancelBtn = ActionButton()
        self._cancelBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=11))
        self._cancelBtn.setClassName("rounded-4 text-black border-gray-40 hover:bg-black-8 py-8 px-24")
        self._acceptBtn.setMinimumWidth(64)

        self._buttonBox = FlexBox()
        self._buttonBox.setSpacing(12)
        self._buttonBox.setAlignment(Qt.AlignRight)
        self._buttonBox.addWidget(self._acceptBtn)
        self._buttonBox.addWidget(self._cancelBtn)

        self._mainLayout = Box(self._inner)
        self._mainLayout.setAlignment(Qt.AlignLeft)

        self._mainLayout.addWidget(self._header)
        self._mainLayout.addWidget(self._message)
        self._mainLayout.addSpacing(8)
        self._mainLayout.addLayout(self._buttonBox)

    def _connectSignalSlots(self) -> None:
        self._acceptBtn.clicked.connect(self.accepted.emit)
        self._cancelBtn.clicked.connect(self.canceled.emit)
        self.accepted.connect(self.close)
        self.canceled.connect(self.close)

    def _assignShortcuts(self) -> None:
        acceptShortcut = QShortcut(QKeySequence(Qt.Key_Return), self._acceptBtn)
        acceptShortcut.activated.connect(self.accepted.emit)

        cancelShortcut = QShortcut(QKeySequence(Qt.Key_Escape), self._cancelBtn)
        cancelShortcut.activated.connect(self.canceled.emit)

    def setFixedSize(self, w: int, h: int) -> None:
        margins = self._inner.contentsMargins()
        super().setFixedSize(w + margins.left() + margins.right(), h + margins.top() + margins.bottom())
        self._inner.setFixedSize(w, h)

    def setInfo(self, header: str, message: str, acceptText: str, cancelText: str) -> None:
        self._header.setText(header)
        self._message.setText(message)
        self._acceptBtn.setText(acceptText)
        self._cancelBtn.setText(cancelText)

    def applyLightMode(self) -> None:
        super().applyLightMode()
        super().applyThemeToChildren()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        super().applyThemeToChildren()

    def moveToCenter(self):
        width = Numbers.clamp(self._inner.sizeHint().width(), 480, 640)
        self.setFixedSize(width, self._inner.sizeHint().height())

        qtRectangle = self._inner.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def open(self) -> None:
        self.applyTheme()
        self.moveToCenter()
        self.exec_()


class _AlertDialog(QDialog, Component):
    canceled: pyqtSignal() = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._initComponent()

    def _createUI(self) -> None:
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowModality(Qt.ApplicationModal)

        self._inner = StyleWidget(self)
        self._inner.setContentsMargins(24, 24, 24, 24)
        self._inner.setClassName("rounded-12 bg-white dark:bg-dark")

        self._mainLayout = Box(self._inner)
        self._mainLayout.setAlignment(Qt.AlignCenter)

        self._image = Cover()
        self._image.setAlignment(Qt.AlignCenter)

        self._header = LabelWithDefaultText()
        self._header.setFont(Factory.createFont(family="Segoe UI Semibold", size=16, bold=True))
        self._header.setClassName("text-black dark:text-white")
        self._header.enableEllipsis(False)
        self._header.setAlignment(Qt.AlignCenter)

        self._message = LabelWithDefaultText()
        self._message.setFont(Factory.createFont(size=11))
        self._message.setClassName("text-black dark:text-white")
        self._message.enableEllipsis(False)
        self._message.setAlignment(Qt.AlignCenter)

        self._acceptBtn = ActionButton()
        self._acceptBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=11))

        self._mainLayout.addWidget(self._image)
        self._mainLayout.addWidget(self._header)
        self._mainLayout.addWidget(self._message)
        self._mainLayout.addSpacing(8)
        self._mainLayout.addWidget(self._acceptBtn)

    def _connectSignalSlots(self) -> None:
        self._acceptBtn.clicked.connect(self.accepted.emit)
        self.accepted.connect(self.close)

    def _assignShortcuts(self) -> None:
        QShortcut(QKeySequence(Qt.Key_Return), self._acceptBtn).activated.connect(self.accepted.emit)
        QShortcut(QKeySequence(Qt.Key_Escape), self._acceptBtn).activated.connect(self.accepted.emit)

    def setFixedSize(self, w: int, h: int) -> None:
        margins = self._inner.contentsMargins()
        super().setFixedSize(w + margins.left() + margins.right(), h + margins.top() + margins.bottom())
        self._inner.setFixedSize(w, h)

    def setInfo(self, image: bytes, header: str, message: str, acceptText: str, onClose: Optional[callable]) -> None:
        self._image.setCover(CoverProps.fromBytes(image, width=128))
        self._header.setText(header)
        self._message.setText(message)
        self._acceptBtn.setText(acceptText)

        if onClose is not None:
            self.accepted.connect(lambda: onClose())

        self.setFixedSize(360, self._inner.sizeHint().height())

    def setState(self, state: str) -> None:
        if state == "info":
            self._acceptBtn.setClassName("text-white rounded-4 bg-danger-75 bg-primary py-8")
        if state == "danger":
            self._acceptBtn.setClassName("text-white rounded-4 bg-danger-75 bg-danger py-8")
        if state == "success":
            self._acceptBtn.setClassName("text-white rounded-4 bg-danger-75 bg-success py-8")

    def applyLightMode(self) -> None:
        super().applyLightMode()
        super().applyThemeToChildren()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        super().applyThemeToChildren()

    def moveToCenter(self):
        qtRectangle = self._inner.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def open(self) -> None:
        self.applyTheme()
        self.moveToCenter()
        self.exec_()


@final
class Dialogs:

    @staticmethod
    def info(header: str, message: str, image: bytes = Images.SUCCESS, acceptText: str = "OK", onAccept: Optional[callable] = None):
        dialog = _AlertDialog()
        dialog.setInfo(image, header, message, acceptText, onAccept)
        dialog.setState("info")
        dialog.open()

    @staticmethod
    def success(message: str, header: str = "Succeed", image: bytes = Images.SUCCESS, acceptText: str = "OK", onAccept: Optional[callable] = None):
        dialog = _AlertDialog()
        dialog.setInfo(image, header, message, acceptText, onAccept)
        dialog.setState("success")
        dialog.open()

    @staticmethod
    def alert(message: str, header: str = "Warning", image: bytes = Images.WARNING, acceptText: str = "OK", onAccept: Optional[callable] = None):
        dialog = _AlertDialog()
        dialog.setInfo(image, header, message, acceptText, onAccept)
        dialog.setState("danger")
        dialog.open()

    @staticmethod
    def confirm(message: str,
                header: str = "Warning",
                acceptText: str = "OK",
                cancelText: str = "Cancel",
                onAccept: Optional[callable] = None):
        dialog = _ConfirmDialog()
        dialog.setInfo(header, message, acceptText, cancelText)

        if onAccept is not None:
            dialog.accepted.connect(lambda: onAccept())

        dialog.open()
