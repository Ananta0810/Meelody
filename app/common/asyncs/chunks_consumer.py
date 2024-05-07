from abc import ABCMeta
from typing import TypeVar, Generic, Callable

from PyQt5.QtCore import QObject, QTimer, pyqtSignal
from PyQt5.QtWidgets import QWidget

QObjectType = type(QObject)
T = TypeVar('T')


class QABCMeta(QObjectType, ABCMeta):
    pass


class ChunksConsumer(QObject, Generic[T], metaclass=QABCMeta):
    stopped = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, items: list[T], size: int, parent: QWidget) -> None:
        super().__init__(parent)
        self.__chunks: list[list[T]] = [items[index:index + size] for index in range(0, len(items), size)]
        self.__timer: QTimer = QTimer()
        self.__currentChunkIndex: int = 0

    def forEach(self, fn: Callable[[T], None], delay: int = 0) -> None:
        self.stop()
        self.__timer.start(delay)
        self.__timer.timeout.connect(lambda: self.__displayChunk(delay, fn))

    def __displayChunk(self, delay: int, fn: Callable[[T], None]) -> None:
        if self.__currentChunkIndex >= len(self.__chunks):
            self.stop()
            self.finished.emit()
            return

        chunk = self.__chunks[self.__currentChunkIndex]

        for item in chunk:
            fn(item)

        self.__currentChunkIndex += 1
        self.__timer.start(delay)

    def stop(self) -> None:
        if self.__timer.isActive():
            self.__timer.stop()
            self.__timer.timeout.disconnect()
            self.stopped.emit()
