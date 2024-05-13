from typing import Optional

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QLabel, QWidget

from app.components.threads import UpdateUIThread
from app.utils.reflections import suppressException


class Gif(QLabel):
    def __init__(self, path: str, fps: int = 24, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.__animationThread = UpdateUIThread(action=lambda: self.__updateAnimation(), interval=1000 / fps)
        self._createUI(path)

    def _createUI(self, path: str) -> None:
        self.setMovie(QMovie(path))

    def setFixedHeight(self, h: int) -> None:
        super().setFixedHeight(h)
        self.movie().setScaledSize(QSize(h, h))

    def setFixedWidth(self, w: int) -> None:
        super().setFixedWidth(w)
        self.movie().setScaledSize(QSize(w, w))

    def setFixedSize(self, w: int, h: int) -> None:
        super().setFixedSize(w, h)
        self.movie().setScaledSize(QSize(w, h))

    def setGifSize(self, w: int) -> None:
        self.movie().setScaledSize(QSize(w, w))

    @suppressException
    def start(self) -> None:
        self.__animationThread.start()

    @suppressException
    def stop(self) -> None:
        self.__animationThread.quit()

    @suppressException
    def __updateAnimation(self) -> None:
        self.movie().jumpToNextFrame()
