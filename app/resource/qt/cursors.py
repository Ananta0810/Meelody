from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

from app.helpers.base import memoizeStaticProperty


class Cursors:

    @memoizeStaticProperty
    def base(self) -> QCursor:
        return QCursor(Qt.ArrowCursor)

    @memoizeStaticProperty
    def pointer(self) -> QCursor:
        return QCursor(Qt.PointingHandCursor)

    @memoizeStaticProperty
    def notAllowed(self) -> QCursor:
        return QCursor(Qt.ForbiddenCursor)

    @memoizeStaticProperty
    def waiting(self) -> QCursor:
        return QCursor(Qt.WaitCursor)
