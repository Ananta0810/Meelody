from typing import final

from PyQt5.QtCore import QTimer


@final
class Promise:
    @staticmethod
    def later(delay: int, action: callable) -> None:
        timer = QTimer()
        timer.timeout.connect(lambda: Promise.__takeActionAndStopTimer(action, timer))
        timer.start(delay)

    @staticmethod
    def __takeActionAndStopTimer(action: callable, timer: QTimer):
        action()
        timer.stop()
