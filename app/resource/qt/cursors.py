from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor


class Cursors:
    HAND: QCursor = None
    DEFAULT: QCursor = None

    @staticmethod
    def init():
        Cursors.HAND = QCursor(Qt.PointingHandCursor)
        Cursors.DEFAULT = QCursor(Qt.ArrowCursor)
