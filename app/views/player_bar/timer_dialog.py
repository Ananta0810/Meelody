from typing import Optional

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget

from app.components.base import Cover, CoverProps, Input, Factory, ActionButton, Label
from app.components.dialogs import BaseDialog
from app.components.widgets import Box, FlexBox
from app.resource.qt import Images


class TimerDialog(BaseDialog):

    def __init__(self):
        super().__init__()
        super()._initComponent()

        self.applyTheme()

    def _createUI(self) -> None:
        super()._createUI()

        self._cover = Cover()
        self._cover.setDefaultCover(CoverProps.fromBytes(Images.TIMER, width=184))

        self._minuteInput = TimerInput(99)
        self._minuteInput.setFixedSize(64, 48)
        self._minuteInput.setAlignment(Qt.AlignCenter)
        self._minuteInput.setFont(Factory.createFont(size=14, bold=True))
        self._minuteInput.setClassName("px-12 rounded-4 border border-primary-12 bg-primary-4")
        self._minuteInput.setText("60")

        self._secondInput = TimerInput(60)
        self._secondInput.setFixedSize(64, 48)
        self._secondInput.setAlignment(Qt.AlignCenter)
        self._secondInput.setFont(Factory.createFont(size=14, bold=True))
        self._secondInput.setClassName("px-12 rounded-4 border border-primary-12 bg-primary-4")
        self._secondInput.setPlaceholderText("00")

        self._separator = Label()
        self._separator.setFont(Factory.createFont(size=14, bold=True))
        self._separator.setClassName("text-black bg-none")
        self._separator.setText(":")
        self._separator.setFixedWidth(self._separator.sizeHint().width())

        self._inputLayout = FlexBox()
        self._inputLayout.setSpacing(8)
        self._inputLayout.setAlignment(Qt.AlignCenter)
        self._inputLayout.addWidget(self._minuteInput)
        self._inputLayout.addWidget(self._separator)
        self._inputLayout.addWidget(self._secondInput)

        self._acceptBtn = ActionButton()
        self._acceptBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=10))
        self._acceptBtn.setClassName("text-white rounded-4 bg-primary-75 bg-primary py-8 disabled:bg-gray-10 disabled:text-gray")
        self._acceptBtn.setText("Start Now")
        self._acceptBtn.setDisabled(False)
        self._acceptBtn.setFixedWidth(320)

        self._mainView = QWidget()
        self._mainView.setContentsMargins(12, 4, 12, 12)

        self._viewLayout = Box(self._mainView)
        self._viewLayout.setAlignment(Qt.AlignCenter)
        self._viewLayout.addWidget(self._cover, alignment=Qt.AlignCenter)
        self._viewLayout.addSpacing(8)
        self._viewLayout.addLayout(self._inputLayout)
        self._viewLayout.addSpacing(12)
        self._viewLayout.addWidget(self._acceptBtn)

        self.addWidget(self._mainView)

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()

    def _assignShortcuts(self) -> None:
        super()._assignShortcuts()


class TimerInput(Input):

    def __init__(self, maxValue: int, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.__max = maxValue
        self.setValidator(QRegExpValidator(QRegExp("^[0-9]+$")))
        self.textChanged.connect(lambda: self._reformat())

    def _reformat(self) -> None:
        text = self.text()
        number = int(text)

        if number < 10:
            self.setText(f"0{number}")
            return

        if len(text) > 2:
            self.setText(f"{int(text[1:])}")
            return

        if number > self.__max:
            self.setText(f"{self.__max}")
