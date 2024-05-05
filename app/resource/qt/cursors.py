from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

from app.helpers.base import memoizeStaticProperty


class Cursors:

    @memoizeStaticProperty
    def HAND(self) -> QCursor:
        return QCursor(Qt.PointingHandCursor)

    @memoizeStaticProperty
    def DEFAULT(self) -> QCursor:
        return QCursor(Qt.ArrowCursor)

    @memoizeStaticProperty
    def NOT_ALLOWED(self) -> QCursor:
        return QCursor(Qt.ForbiddenCursor)

    @memoizeStaticProperty
    def WAITING(self) -> QCursor:
        return QCursor(Qt.WaitCursor)
