from PyQt5.QtCore import QObject, pyqtSignal, QEvent

from app.helpers.qt import Widgets


class VisibleObserver(QObject):
    visible = pyqtSignal(bool)

    def __init__(self, widget: QObject):
        super().__init__(widget)
        self._widget = widget
        self._isVisible = False
        self._widget.installEventFilter(self)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if obj is not self._widget:
            return super().eventFilter(obj, event)

        newState = Widgets.isInView(obj)

        if self._isVisible != newState:
            self._isVisible = newState
            self.visible.emit(newState)

        return super().eventFilter(obj, event)
