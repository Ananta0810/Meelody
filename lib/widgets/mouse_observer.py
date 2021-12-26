from PyQt5.QtCore import QEvent, QObject, pyqtSignal


class MouseObserver(QObject):
    enterHover = pyqtSignal()
    leaveHover = pyqtSignal()

    def __init__(self, widget):
        super().__init__(widget)
        self._widget = widget
        self.widget.installEventFilter(self)

    @property
    def widget(self):
        return self._widget

    def eventFilter(self, obj, event):
        if obj is not self._widget:
            return super().eventFilter(obj, event)
        if event.type() == QEvent.HoverEnter:
            self.enterHover.emit()
        if event.type() == QEvent.HoverLeave:
            self.leaveHover.emit()
        return super().eventFilter(obj, event)


class ClickObserver(QObject):
    clicked = pyqtSignal()
    doubleClicked = pyqtSignal()

    def __init__(self, widget: "QObject"):
        super().__init__(widget)
        self._widget = widget
        self.widget.installEventFilter(self)

    @property
    def widget(self):
        return self._widget

    def eventFilter(self, obj: "QObject", event: "QEvent") -> bool:
        if obj is not self._widget:
            return super().eventFilter(obj, event)
        if event.type() == QEvent.MouseButtonPress:
            self.clicked.emit()
        if event.type() == QEvent.MouseButtonDblClick:
            self.doubleClicked.emit()
        return super().eventFilter(obj, event)
