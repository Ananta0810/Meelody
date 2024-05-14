from typing import Optional

from PyQt5.QtCore import QObject, QTimer


class After(QObject):

    def __init__(self, delay: int = 16, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)

        self.__timer = QTimer(parent)

        self.__timer.setInterval(delay)
        self.__timer.setSingleShot(True)
        self.__timer.timeout.connect(lambda: self.deleteLater())

    def call(self, function: callable) -> None:
        self.__timer.timeout.connect(lambda: function())
        self.__timer.start()
