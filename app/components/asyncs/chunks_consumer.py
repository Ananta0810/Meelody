from abc import ABCMeta
from typing import TypeVar, Generic, Callable

from PyQt5.QtCore import QObject, QTimer, pyqtSignal, pyqtBoundSignal
from PyQt5.QtWidgets import QWidget

QObjectType = type(QObject)
T = TypeVar('T')


class QABCMeta(QObjectType, ABCMeta):
    pass


class ChunksConsumer(QObject, Generic[T], metaclass=QABCMeta):
    stopped: pyqtBoundSignal = pyqtSignal()
    finished: pyqtBoundSignal = pyqtSignal()

    def __init__(self, items: list[T], size: int, parent: QWidget) -> None:
        super().__init__(parent)
        self.__size = size
        self.__chunks: list[list[T]] = [items[index:index + size] for index in range(0, len(items), size)]
        self.__timer: QTimer = QTimer()
        self.__currentChunkIndex: int = 0

    def forEach(self, fn: Callable[[T, int], None], delay: int = 0) -> None:
        self.stop()
        self.__timer.start(delay)
        self.__timer.timeout.connect(lambda: self.__displayChunk(delay, fn))

    def __displayChunk(self, delay: int, fn: Callable[[T, int], None]) -> None:
        if self.__currentChunkIndex >= len(self.__chunks):
            self.stop()
            self.finished.emit()
            return

        chunk = self.__chunks[self.__currentChunkIndex]

        lastIndex = self.__currentChunkIndex * self.__size

        for index, item in enumerate(chunk):
            fn(item, index + lastIndex)

        self.__currentChunkIndex += 1
        self.__timer.start(delay)

    def stop(self) -> None:
        if self.__timer.isActive():
            self.__timer.stop()
            self.__timer.timeout.disconnect()
            self.stopped.emit()
