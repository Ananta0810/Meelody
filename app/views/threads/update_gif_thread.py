from time import sleep

from PyQt5.QtCore import QThread
from PyQt5.QtGui import QMovie


class UpdateGifThread(QThread):

    def __init__(self, movie: QMovie, interval) -> None:
        super().__init__()
        self.__movie = movie
        self.__interval = interval / 1000

    def run(self) -> None:
        while True:
            self.__movie.jumpToNextFrame()
            sleep(self.__interval)
