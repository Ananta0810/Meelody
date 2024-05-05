from time import sleep
from typing import Optional

from PyQt5.QtCore import QThread


class UpdateUIThread(QThread):

    def __init__(self, action: callable, interval: Optional[int | float]) -> None:
        super().__init__()
        self.__action = action
        self.__interval = interval / 1000
        self.__canUpdate = True

    def run(self) -> None:
        self.__canUpdate = True
        while self.__canUpdate:
            self.__action()
            sleep(self.__interval)

    def quit(self) -> None:
        super().quit()
        self.__canUpdate = False
