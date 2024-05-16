from PyQt5.QtCore import QObject, pyqtBoundSignal


class SignalConnector(QObject):
    def __init__(self, parent: QObject) -> None:
        super().__init__(parent)
        self._signals: list[tuple[pyqtBoundSignal, callable]] = []
        parent.destroyed.connect(lambda: self.disconnectSignals())

    def connect(self, signal: pyqtBoundSignal, fn: callable) -> None:
        self._signals.append((signal, fn))
        signal.connect(fn)

    def disconnectSignals(self) -> None:
        for signal, fn in self._signals:
            signal.disconnect(fn)
