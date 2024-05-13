from typing import Optional

from PyQt5.QtCore import QTimer, QObject


class Debounce(QObject):

    def __init__(self, fn: callable, parent: Optional[QObject] = None, delay: int = 500) -> None:
        super().__init__(parent)

        self.__timer = QTimer(parent)

        self.__timer.setInterval(delay)
        self.__timer.setSingleShot(True)
        self.__timer.timeout.connect(lambda: fn())

    def setDelay(self, delay: int) -> None:
        self.__timer.setInterval(delay)

    def call(self) -> None:
        self.__timer.start()
