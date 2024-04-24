from PyQt5.QtCore import QObject, pyqtSignal

from app.common.models import Playlist


class SignalBus(QObject):
    themeChanged = pyqtSignal(bool)
    playlistChanged = pyqtSignal(Playlist)


signalBus = SignalBus()
