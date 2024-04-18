from PyQt5.QtCore import QObject, QEvent


class ClickObserver(QObject):
    __onclick_fn: callable = None
    __on_doubleclick_fn: callable = None

    def __init__(self, widget: "QObject"):
        super().__init__(widget)
        self._widget = widget
        self.widget.installEventFilter(self)

    def onClick(self, fn: callable) -> None:
        self.__onclick_fn = fn

    def onDoubleClick(self, fn: callable) -> None:
        self.__on_doubleclick_fn = fn

    @property
    def widget(self):
        return self._widget

    def eventFilter(self, obj: "QObject", event: "QEvent") -> bool:
        if obj is not self._widget:
            return super().eventFilter(obj, event)
        if event.type() == QEvent.MouseButtonPress and self.__onclick_fn is not None:
            self.__onclick_fn()
        if event.type() == QEvent.MouseButtonDblClick and self.__on_doubleclick_fn is not None:
            self.__on_doubleclick_fn()
        return super().eventFilter(obj, event)
