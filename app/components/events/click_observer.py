from PyQt5.QtCore import QObject, QEvent, pyqtSignal, pyqtBoundSignal


class ClickObserver(QObject):
    clicked: pyqtBoundSignal = pyqtSignal()

    def __init__(self, widget: QObject):
        super().__init__(widget)
        self._widget = widget
        self.widget.installEventFilter(self)

    @property
    def widget(self):
        return self._widget

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if obj is self._widget and event.type() == QEvent.MouseButtonPress:
            self.clicked.emit()
        return super().eventFilter(obj, event)
