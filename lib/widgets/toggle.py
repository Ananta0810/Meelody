from PyQt5.QtCore import QVariantAnimation
from PyQt5.QtWidgets import QPushButton


class Toggle(QPushButton):
    def __init__(
        self,
        parent,
        width: int = 48,
        height: int = 30,
        gap: int = 4,
        animationDuration: float = 125,
    ):
        super().__init__(parent)
        self._width = width
        self._height = height
        self.gap = gap
        self.duration = animationDuration

        self.setFixedSize(self._width, self._height)
        self.setCheckable(True)
        self.clicked.connect(self.toggleSwitch)

        self.toggle_front = QPushButton(self)
        self.toggle_front.clicked.connect(self.clicked)
        self.stylize()

    def stylize(
        self,
        frontColor: str = "white",
        backColor: str = "#eaeaea",
        activeBackColor: str = "#00dd50",
    ):
        self.setStyleSheet(
            "QPushButton{"
            + "border: none;"
            + f"border-radius: {self._height / 2}px;"
            + f"background:{backColor};"
            + "}"
            + "QPushButton::checked{"
            + f"background:{activeBackColor};"
            + "}"
        )

        self.setTogglePosition()
        frontSize = self._height - self.gap * 2
        self.toggle_front.resize(frontSize, frontSize)
        self.toggle_front.setStyleSheet(
            f"background:{frontColor};"
            + "border:none;"
            + f"border-radius:{self._height / 2 - self.gap}px;"
        )

    # Override
    def setGeometry(self, *args, **kwargs):
        QPushButton.setGeometry(self, *args, **kwargs)
        self._width = self.size().width()
        self._height = self.size().height()

    # Override
    def setChecked(self, a0: bool):
        QPushButton.setChecked(self, a0)
        self.setTogglePosition()

    def setTogglePosition(self):
        if self.isChecked():
            self.toggle_front.move(
                self._width - self._height + self.gap, self.gap
            )
        else:
            self.toggle_front.move(self.gap, self.gap)

    def toggleSwitch(self):
        if self.sender() == self.toggle_front:
            self.nextCheckState()
        # get the position base on state
        if self.isChecked():
            start = 0.00
            end = 1.00
        else:
            start = 1.00
            end = 0.00

        # Get the switch animation
        self._animation = QVariantAnimation(
            self,
            valueChanged=self.toggleAnimation,
            startValue=start,
            endValue=end,
            duration=self.duration,
        )
        self._animation.start()

    def toggleAnimation(self, value):
        value = int(value * (self._width - self._height) + self.gap)
        self.toggle_front.move(value, self.gap)
