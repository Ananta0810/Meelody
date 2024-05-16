from contextlib import suppress

from PyQt5.QtCore import pyqtBoundSignal


class Signals:
    @staticmethod
    def disconnect(signal: pyqtBoundSignal, fn: callable) -> None:
        with suppress(TypeError):
            signal.disconnect(fn)
