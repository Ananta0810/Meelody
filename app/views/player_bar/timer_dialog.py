import time
from typing import Optional

from PyQt5.QtCore import Qt, QRegExp, QThread, QObject, pyqtSignal
from PyQt5.QtGui import QRegExpValidator, QWheelEvent, QResizeEvent
from PyQt5.QtWidgets import QWidget

from app.common.others import musicPlayer
from app.components.base import Cover, CoverProps, Input, Factory, ActionButton, Label
from app.components.dialogs import BaseDialog
from app.components.widgets import Box, FlexBox
from app.helpers.others import Logger
from app.resource.qt import Images


class TimerDialog(BaseDialog):

    def __init__(self):
        self.__isCountDown: bool = False
        super().__init__()
        super()._initComponent()
        self.__setIsCountDown(False)
        self.__checkValidTime()

    def _createUI(self) -> None:
        super()._createUI()

        self._cover = Cover()
        self._cover.setDefaultCover(CoverProps.fromBytes(Images.TIMER, width=184))

        # ================================= Setup Timer =================================
        self._minuteInput = TimerInput(99)
        self._minuteInput.setFixedSize(64, 48)
        self._minuteInput.setAlignment(Qt.AlignCenter)
        self._minuteInput.setFont(Factory.createFont(size=16, bold=True))
        self._minuteInput.setClassName(
            "px-12 rounded-4 border border-primary-12 bg-primary-4 disabled:bg-none disabled:border-none disabled:text-black",
            "dark:border-white-12 dark:bg-white-4 dark:text-white dark:disabled:text-white",
        )
        self._minuteInput.setText("01")

        self._secondInput = TimerInput(59)
        self._secondInput.setFixedSize(64, 48)
        self._secondInput.setAlignment(Qt.AlignCenter)
        self._secondInput.setFont(Factory.createFont(size=16, bold=True))
        self._secondInput.setClassName(
            "px-12 rounded-4 border border-primary-12 bg-primary-4 disabled:bg-none disabled:border-none disabled:text-black",
            "dark:border-white-12 dark:bg-white-4 dark:text-white dark:disabled:text-white",
        )
        self._secondInput.setText("00")

        self._separator = Label()
        self._separator.setFont(Factory.createFont(size=14, bold=True))
        self._separator.setClassName("text-black bg-none dark:text-white")
        self._separator.setText(":")
        self._separator.setFixedWidth(self._separator.sizeHint().width())

        self._inputLayout = FlexBox()
        self._inputLayout.setSpacing(8)
        self._inputLayout.setAlignment(Qt.AlignHCenter)
        self._inputLayout.addWidget(self._minuteInput)
        self._inputLayout.addWidget(self._separator, alignment=Qt.AlignVCenter)
        self._inputLayout.addWidget(self._secondInput)

        self._startBtn = ActionButton()
        self._startBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=10))
        self._startBtn.setClassName("text-white rounded-4 bg-primary-75 bg-primary py-8 disabled:bg-gray-10 disabled:text-gray")
        self._startBtn.setText("Start Now")
        self._startBtn.setFixedWidth(320)

        self._stopBtn = ActionButton()
        self._stopBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=10))
        self._stopBtn.setClassName("text-white rounded-4 bg-danger-75 bg-danger py-8 ")
        self._stopBtn.setText("Cancel")
        self._stopBtn.setFixedWidth(320)

        self._setupTimer = QWidget()

        self._setupTimerLayout = Box(self._setupTimer)
        self._setupTimerLayout.setSpacing(12)

        self._setupTimerLayout.addLayout(self._inputLayout)
        self._setupTimerLayout.addWidget(self._startBtn)
        self._setupTimerLayout.addWidget(self._stopBtn)

        # ================================= Main Layout =================================
        self._mainView = QWidget()

        self._viewLayout = Box(self._mainView)
        self._viewLayout.setSpacing(0)
        self._viewLayout.setContentsMargins(12, 0, 12, 0)

        self._viewLayout.addWidget(self._cover, alignment=Qt.AlignHCenter)
        self._viewLayout.addSpacing(8)
        self._viewLayout.addWidget(self._setupTimer, alignment=Qt.AlignHCenter)

        self._titleBarLayout.setContentsMargins(12, 12, 12, 0)
        self._body.setContentsMargins(4, 4, 4, 12)
        self.addWidget(self._mainView)

    def _createThreads(self) -> None:
        self._countDownThread = CountDownThread()

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()

        self._minuteInput.textChanged.connect(lambda: self.__checkValidTime() if not self.__isCountDown else None)
        self._secondInput.textChanged.connect(lambda: self.__checkValidTime() if not self.__isCountDown else None)

        self._startBtn.clicked.connect(lambda: self.__startCountDown())
        self._stopBtn.clicked.connect(lambda: self.__stopCountDown())

        self._countDownThread.finished.connect(lambda: self.__onTimerFinished())
        self._countDownThread.tick.connect(lambda value: self.__setCountDownTime(value))

        musicPlayer.played.connect(lambda: self.__continueCountDown())
        musicPlayer.paused.connect(lambda: self.__pauseCountDown())

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.setFixedHeight(self.sizeHint().height())

    def __checkValidTime(self) -> None:
        isInvalid = self.__getCountDownTime() < 60
        self._startBtn.setDisabled(isInvalid)

    def __continueCountDown(self) -> None:
        if self.__isCountDown and not self._countDownThread.isRunning():
            self._countDownThread.start()

    def __pauseCountDown(self) -> None:
        self._countDownThread.quit()

    def __startCountDown(self) -> None:
        self.__setIsCountDown(True)
        self.__setCountDownTime(self.__getCountDownTime())
        self._countDownThread.setTime(self.__getCountDownTime())
        self._countDownThread.start()
        self.close()
        Logger.info("Starting timer")

    def __stopCountDown(self) -> None:
        self.__setIsCountDown(False)
        self._countDownThread.quit()
        Logger.info("Stop timer")

    def __onTimerFinished(self) -> None:
        self.__setIsCountDown(False)
        musicPlayer.pause()
        Logger.info("Time up. Pause song.")

    def __setCountDownTime(self, value: int) -> None:
        mm = value // 60
        ss = int(value) % 60

        self._minuteInput.setText(str(mm).zfill(2))
        self._secondInput.setText(str(ss).zfill(2))

    def __setIsCountDown(self, countdownStarted: bool) -> None:
        self.__isCountDown = countdownStarted

        self._startBtn.setVisible(not countdownStarted)
        self._stopBtn.setVisible(countdownStarted)
        self._minuteInput.setDisabled(countdownStarted)
        self._secondInput.setDisabled(countdownStarted)

    def __getCountDownTime(self) -> int:
        return int(self._minuteInput.text()) * 60 + int(self._secondInput.text())


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


class CountDownThread(QThread):
    finished = pyqtSignal()
    tick = pyqtSignal(int)

    def __init__(self, parent: Optional[QObject] = None) -> None:
        self.__currentTime = 0
        self.__started = False

        super().__init__(parent)

    def setTime(self, value: int) -> None:
        self.__currentTime = value

    def start(self, priority: QThread.Priority = None) -> None:
        if priority is None:
            super().start()
        else:
            super().start(priority)

        self.__started = True

    def quit(self) -> None:
        self.__started = False
        super().quit()

    def run(self) -> None:
        while self.__started and self.__currentTime > 0 and musicPlayer.isPlaying():
            time.sleep(1)
            self.__currentTime = self.__currentTime - 1
            self.tick.emit(self.__currentTime)

        if self.__currentTime <= 0:
            self.__currentTime = 0
            self.finished.emit()
            self.quit()
