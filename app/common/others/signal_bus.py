from PyQt5.QtCore import QObject, pyqtSignal


class SignalBus(QObject):
    themeChanged = pyqtSignal(bool)


signalBus = SignalBus()
