from typing import Optional

from PyQt5.QtCore import QObject, pyqtSignal, QEvent, QTimer

from app.utils.qt import Widgets


class VisibleObserver(QObject):
    visible = pyqtSignal(bool)

    def __init__(self, widget: QObject, oneTime: bool = True, delay: Optional[int] = None):
        super().__init__(widget)
        self._widget = widget
        self._isVisible = False
        self._widget.installEventFilter(self)
        self._delay = delay

        if oneTime:
            self.visible.connect(lambda visible: self.deleteLater() if visible else None)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if obj is not self._widget:
            return super().eventFilter(obj, event)

        newState = Widgets.isInView(obj)

        if self._isVisible != newState:
            self._isVisible = newState

            if self._delay is None:
                self.visible.emit(newState)
            else:
                timer = QTimer(self)
                timer.setSingleShot(True)
                timer.timeout.connect(lambda: self.visible.emit(newState))
                timer.start(self._delay)

        return super().eventFilter(obj, event)
