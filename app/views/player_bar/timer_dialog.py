from typing import Optional

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator, QWheelEvent
from PyQt5.QtWidgets import QWidget

from app.components.base import Cover, CoverProps, Input, Factory, ActionButton, Label
from app.components.dialogs import BaseDialog
from app.components.widgets import Box, FlexBox
from app.resource.qt import Images


class TimerDialog(BaseDialog):

    def __init__(self):
        super().__init__()
        super()._initComponent()

        self.setCountDownTime(2000)

    def _createUI(self) -> None:
        super()._createUI()

        self._cover = Cover()
        self._cover.setDefaultCover(CoverProps.fromBytes(Images.TIMER, width=184))

        # ================================= Setup Timer =================================
        self._minuteInput = TimerInput(99)
        self._minuteInput.setFixedSize(64, 48)
        self._minuteInput.setAlignment(Qt.AlignCenter)
        self._minuteInput.setFont(Factory.createFont(size=14, bold=True))
        self._minuteInput.setClassName("px-12 rounded-4 border border-primary-12 bg-primary-4")
        self._minuteInput.setText("60")

        self._secondInput = TimerInput(59)
        self._secondInput.setFixedSize(64, 48)
        self._secondInput.setAlignment(Qt.AlignCenter)
        self._secondInput.setFont(Factory.createFont(size=14, bold=True))
        self._secondInput.setClassName("px-12 rounded-4 border border-primary-12 bg-primary-4")
        self._secondInput.setText("00")

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

        self._startBtn = ActionButton()
        self._startBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=10))
        self._startBtn.setClassName("text-white rounded-4 bg-primary-75 bg-primary py-8 disabled:bg-gray-10 disabled:text-gray")
        self._startBtn.setText("Start Now")
        self._startBtn.setFixedWidth(320)

        self._setupTimer = QWidget()
        self._setupTimer.setContentsMargins(0, 0, 0, 0)
        self._setupTimer.hide()

        self._setupTimerLayout = Box(self._setupTimer)
        self._setupTimerLayout.setAlignment(Qt.AlignCenter)

        self._setupTimerLayout.addLayout(self._inputLayout)
        self._setupTimerLayout.addSpacing(12)
        self._setupTimerLayout.addWidget(self._startBtn)

        # ================================= Countdown Timer =================================
        self._minuteLabel = Label()
        self._minuteLabel.setFixedSize(64, 48)
        self._minuteLabel.setAlignment(Qt.AlignCenter)
        self._minuteLabel.setFont(Factory.createFont(size=14, bold=True))
        self._minuteLabel.setClassName("bg-none")

        self._secondLabel = Label()
        self._secondLabel.setFixedSize(64, 48)
        self._secondLabel.setAlignment(Qt.AlignCenter)
        self._secondLabel.setFont(Factory.createFont(size=14, bold=True))
        self._secondLabel.setClassName("bg-none")

        self._countDownSeparator = Label()
        self._countDownSeparator.setFont(Factory.createFont(size=14, bold=True))
        self._countDownSeparator.setClassName("text-black bg-none")
        self._countDownSeparator.setText(":")
        self._countDownSeparator.setFixedWidth(self._separator.sizeHint().width())

        self._timeLabelLayout = FlexBox()
        self._timeLabelLayout.setSpacing(8)
        self._timeLabelLayout.setAlignment(Qt.AlignCenter)
        self._timeLabelLayout.addWidget(self._minuteLabel)
        self._timeLabelLayout.addWidget(self._separator)
        self._timeLabelLayout.addWidget(self._secondLabel)

        self._stopBtn = ActionButton()
        self._stopBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=10))
        self._stopBtn.setClassName("text-white rounded-4 bg-danger-75 bg-danger py-8 ")
        self._stopBtn.setText("Stop Now")
        self._stopBtn.setFixedWidth(320)

        self._countDown = QWidget()
        self._countDown.setContentsMargins(0, 0, 0, 0)

        self._countDownLayout = Box(self._countDown)
        self._countDownLayout.setAlignment(Qt.AlignCenter)

        self._countDownLayout.addLayout(self._timeLabelLayout)
        self._countDownLayout.addSpacing(12)
        self._countDownLayout.addWidget(self._stopBtn)

        # ================================= Main Layout =================================
        self._mainView = QWidget()
        self._mainView.setContentsMargins(12, 4, 12, 12)

        self._viewLayout = Box(self._mainView)
        self._viewLayout.setAlignment(Qt.AlignCenter)

        self._viewLayout.addWidget(self._cover, alignment=Qt.AlignCenter)
        self._setupTimerLayout.addSpacing(8)
        self._viewLayout.addWidget(self._setupTimer, alignment=Qt.AlignCenter)
        self._viewLayout.addWidget(self._countDown, alignment=Qt.AlignCenter)

        self.addWidget(self._mainView)

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()

    def _assignShortcuts(self) -> None:
        super()._assignShortcuts()

    def setCountDownTime(self, time: int) -> None:
        mm = time // 60
        ss = int(time) % 60

        self._minuteLabel.setText(str(mm).zfill(2))
        self._secondLabel.setText(str(ss).zfill(2))


class TimerInput(Input):

    def __init__(self, maxValue: int, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.__max = maxValue

        self.setValidator(QRegExpValidator(QRegExp("^[0-9]+$")))
        self.textChanged.connect(lambda: self._reformat())

    def _reformat(self) -> None:
        text = self.text()
        number = int(text)

        if number < 0:
            self.setText(f"{self.__max}")
            return

        if number < 10:
            self.setText(f"0{number}")
            return

        if len(text) > 2:
            self.setText(f"{int(text[1:])}")
            return

        if number > self.__max:
            self.setText(f"00")

    def wheelEvent(self, a0: Optional[QWheelEvent]) -> None:
        super().wheelEvent(a0)
        rate = a0.angleDelta().y() / abs(a0.angleDelta().y())
        self.setText(f"{int(self.text()) + int(rate)}")
