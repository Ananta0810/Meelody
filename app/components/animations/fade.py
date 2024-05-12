from contextlib import suppress
from typing import Optional

from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QWidget


class Fade(QPropertyAnimation):
    def __init__(self, widget: QWidget, duration: int = 100):
        super().__init__(widget, b"windowOpacity")

        self.setDuration(duration)
        self.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def fadeIn(self, onFinished: Optional[callable] = None) -> None:
        self.setStartValue(0.0)
        self.setEndValue(1.0)

        with suppress(TypeError):
            self.finished.disconnect()

        if onFinished is not None:
            self.finished.connect(lambda: onFinished())

        self.start()

    def fadeOut(self, onFinished: Optional[callable] = None) -> None:
        self.setStartValue(1.0)
        self.setEndValue(0.0)

        with suppress(TypeError):
            self.finished.disconnect()

        if onFinished is not None:
            self.finished.connect(lambda: onFinished())

        self.start()
