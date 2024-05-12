from typing import Optional, final

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence, QResizeEvent
from PyQt5.QtWidgets import QShortcut, QVBoxLayout, QHBoxLayout

from app.common.others import translator
from app.common.statics.qt import Images
from app.components.base import FontFactory
from app.components.buttons import ActionButton
from app.components.dialogs import BaseDialog
from app.components.images import Cover
from app.components.labels import Label
from app.components.windows import FramelessWindow
from app.helpers.base import Numbers


class _ConfirmDialog(FramelessWindow):
    confirmed: pyqtSignal() = pyqtSignal()
    canceled: pyqtSignal() = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._initComponent()

    def _createUI(self) -> None:
        self.setWindowModality(Qt.ApplicationModal)
        self.setContentsMargins(24, 16, 24, 16)
        self.setClassName("rounded-12 bg-white dark:bg-dark")

        self._header = Label()
        self._header.setFont(FontFactory.create(family="Segoe UI Semibold", size=16, bold=True))
        self._header.setClassName("text-black dark:text-white")
        self._header.setAlignment(Qt.AlignLeft)

        self._message = Label()
        self._message.setFont(FontFactory.create(size=10))
        self._message.setClassName("text-black dark:text-white")

        self._acceptBtn = ActionButton()
        self._acceptBtn.setFont(FontFactory.create(family="Segoe UI Semibold", size=10))
        self._acceptBtn.setClassName("text-white rounded-4 bg-danger hover:bg-danger-[w120] px-24")
        self._acceptBtn.setFixedHeight(32)

        self._cancelBtn = ActionButton()
        self._cancelBtn.setFont(FontFactory.create(family="Segoe UI Semibold", size=10))
        self._cancelBtn.setClassName(
            "rounded-4 text-black border border-gray-40 hover:bg-black-12 px-24",
            "dark:text-white dark:border-gray-[b40] dark:hover:bg-white-12"
        )
        self._cancelBtn.setFixedHeight(32)

        self._buttonBox = QHBoxLayout()
        self._buttonBox.setSpacing(12)
        self._buttonBox.addStretch(1)
        self._buttonBox.addWidget(self._acceptBtn)
        self._buttonBox.addWidget(self._cancelBtn)

        self._body = QVBoxLayout()
        self._body.setAlignment(Qt.AlignLeft)

        self._body.addWidget(self._header)
        self._body.addSpacing(8)
        self._body.addWidget(self._message)
        self._body.addSpacing(8)
        self._body.addLayout(self._buttonBox)

        super().addLayout(self._body)

    def _connectSignalSlots(self) -> None:
        self._acceptBtn.clicked.connect(lambda: self.confirmed.emit())
        self._cancelBtn.clicked.connect(lambda: self.canceled.emit())
        self.confirmed.connect(lambda: self.close())
        self.canceled.connect(lambda: self.close())

    def _assignShortcuts(self) -> None:
        acceptShortcut = QShortcut(QKeySequence(Qt.Key_Return), self._acceptBtn)
        acceptShortcut.activated.connect(lambda: self.confirmed.emit())

        cancelShortcut = QShortcut(QKeySequence(Qt.Key_Escape), self._cancelBtn)
        cancelShortcut.activated.connect(lambda: self.canceled.emit())

    def setInfo(self, header: str, message: str, acceptText: str, cancelText: str) -> None:
        self._header.setText(header)
        self._message.setText(message)
        self._acceptBtn.setText(acceptText)
        self._cancelBtn.setText(cancelText)

        width = Numbers.clamp(self.sizeHint().width(), 480, 640)
        self.setFixedWidth(width)
        self._message.setMinimumHeight(self._message.sizeHint().height())

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.moveToCenter()

    def applyLightMode(self) -> None:
        super().applyLightMode()
        super().applyThemeToChildren()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        super().applyThemeToChildren()

    def show(self) -> None:
        self.applyTheme()
        self.moveToCenter()
        super().show()


class _AlertDialog(BaseDialog):

    def __init__(self):
        super().__init__()
        self._initComponent()

    def _createUI(self) -> None:
        super()._createUI()
        self.setFixedWidth(360)

        self.setContentsMargins(16, 16, 16, 16)

        self._image = Cover()
        self._image.setAlignment(Qt.AlignCenter)

        self._header = Label()
        self._header.setFont(FontFactory.create(family="Segoe UI Semibold", size=16, bold=True))
        self._header.setClassName("text-black dark:text-white")
        self._header.setAlignment(Qt.AlignCenter)

        self._message = Label()
        self._message.setFont(FontFactory.create(size=11))
        self._message.setClassName("text-black dark:text-white")
        self._message.setAlignment(Qt.AlignCenter)

        self._acceptBtn = ActionButton()
        self._acceptBtn.setFont(FontFactory.create(family="Segoe UI Semibold", size=10))

        self.addWidget(self._image)
        self.addWidget(self._header)
        self.addWidget(self._message)
        self.addSpacing(8)
        self.addWidget(self._acceptBtn)

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()
        self._acceptBtn.clicked.connect(lambda: self.closed.emit())

    def _assignShortcuts(self) -> None:
        super()._assignShortcuts()
        QShortcut(QKeySequence(Qt.Key_Return), self._acceptBtn).activated.connect(lambda: self.closed.emit())

    def setInfo(self, image: bytes, header: str, message: str, acceptText: str, onClose: Optional[callable]) -> None:
        self._image.setCover(Cover.Props.fromBytes(image, width=128))
        self._header.setText(header)
        self._message.setText(message)
        self._acceptBtn.setText(acceptText)

        if onClose is not None:
            self.closed.connect(lambda: onClose())

    def setState(self, state: str) -> None:
        if state == "info":
            self._acceptBtn.setClassName("text-white rounded-4 bg-primary-75 bg-primary py-8")
        if state == "danger":
            self._acceptBtn.setClassName("text-white rounded-4 bg-danger-75 bg-danger py-8")
        if state == "success":
            self._acceptBtn.setClassName("text-white rounded-4 bg-success-75 bg-success py-8")


@final
class Dialogs:

    @staticmethod
    def info(header: str,
             message: str,
             acceptText: Optional[str] = None,
             image: bytes = Images.success,
             onAccept: Optional[callable] = None) -> None:
        dialog = _AlertDialog()
        dialog.setInfo(image, header, message, acceptText or translator.translate("DIALOG.CLOSE"), onAccept)
        dialog.setState("info")
        dialog.show()

    @staticmethod
    def success(message: str,
                header: Optional[str] = None,
                acceptText: Optional[str] = None,
                image: bytes = Images.success,
                onAccept: Optional[callable] = None) -> None:
        dialog = _AlertDialog()
        dialog.setInfo(image, header or translator.translate("DIALOG.SUCCESS"), message, acceptText or translator.translate("DIALOG.CLOSE"), onAccept)
        dialog.setState("success")
        dialog.show()

    @staticmethod
    def alert(message: str,
              header: Optional[str] = None,
              acceptText: Optional[str] = None,
              image: bytes = Images.warning,
              onAccept: Optional[callable] = None) -> None:
        dialog = _AlertDialog()
        dialog.setInfo(image, header or translator.translate("DIALOG.WARNING"), message, acceptText or translator.translate("DIALOG.CLOSE"), onAccept)
        dialog.setState("danger")
        dialog.show()

    @staticmethod
    def confirm(
        message: str,
        header: Optional[str] = None,
        acceptText: Optional[str] = None,
        cancelText: Optional[str] = None,
        onAccept: Optional[callable] = None,
        onCancel: Optional[callable] = None,
    ) -> None:
        dialog = _ConfirmDialog()
        dialog.setInfo(
            header or translator.translate("DIALOG.WARNING"),
            message,
            acceptText or translator.translate("DIALOG.CONTINUE"),
            cancelText or translator.translate("DIALOG.CANCEL")
        )

        if onAccept is not None:
            dialog.confirmed.connect(lambda: onAccept())

        if onCancel is not None:
            dialog.canceled.connect(lambda: onCancel())

        dialog.show()
