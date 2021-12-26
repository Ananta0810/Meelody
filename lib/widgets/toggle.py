from typing import Optional

from PyQt5.QtCore import QEasingCurve, QRect, Qt, QVariantAnimation, pyqtSignal
from PyQt5.QtGui import QResizeEvent, QShowEvent
from PyQt5.QtWidgets import QPushButton, QWidget


class Toggle(QWidget):
    valueChanged = pyqtSignal()

    def __init__(
        self,
        parent: Optional["QWidget"] = None,
        gap: int = 4,
    ):
        super().__init__(parent)
        self._isChecked = False
        self._gap = gap
        self._foregroundColor = "WHITE"
        self._backgroundColor = "#eaeaea"
        self._activeBackgroundColor = "#00dd50"

        self.__setupUi()
        self._animation = QVariantAnimation(self, valueChanged=self.__moveFrontButton, duration=0)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        super().resizeEvent(a0)
        self.sizingButton()
        self.stylize()

    # !Fix a bug when setChecked while button is not visible
    def showEvent(self, a0: QShowEvent) -> None:
        self.__moveFrontButton(self.__getFrontXPos())
        return super().showEvent(a0)

    def isChecked(self) -> bool:
        return self._isChecked

    def nextCheckState(self) -> None:
        self._isChecked = not self._isChecked
        self.__setBackStyleSheet()

    def setChecked(self, a0: bool) -> None:
        self._isChecked = a0
        self.__setBackStyleSheet()
        self.__moveFrontButton(self.__getFrontXPos())

    def setAnimationDuration(self, duration: int) -> None:
        self._animation.setDuration(duration)

    def setForegroundColor(self, color: str) -> None:
        self._foregroundColor = color

    def setBackgroundColor(self, color: str):
        self._backgroundColor = color

    def setActiveBackgroundColor(self, color: str) -> None:
        self._activeBackgroundColor = color

    def stylize(self) -> None:
        self.__setForegroundColor(self._foregroundColor)
        self.__setBackStyleSheet()

    def __setupUi(self) -> None:
        self.back = QPushButton(self)
        self.front = QPushButton(self)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.back.clicked.connect(self.__clicked)
        self.front.clicked.connect(self.__clicked)

        self.sizingButton()
        self.stylize()

    def sizingButton(self) -> None:
        buttonSize = self.size()
        self.back.setFixedSize(buttonSize)

        frontEdge: float = buttonSize.height() - self._gap * 2
        self.front.setFixedSize(frontEdge, frontEdge)
        self.front.move(self.__getFrontRootXPos(), self.__getFrontRootXPos())

    def __setBackStyleSheet(self) -> None:
        if self._isChecked:
            self.__setBackgroundColor(self._activeBackgroundColor)
            return
        self.__setBackgroundColor(self._backgroundColor)

    def __setForegroundColor(self, color: str) -> None:
        self.front.setStyleSheet(
            "".join(
                [
                    f"background:{color};",
                    "border:none;",
                    f"border-radius:{self.front.height() / 2}px;",
                ]
            )
        )

    def __setBackgroundColor(self, color: str):
        self.back.setStyleSheet(
            "".join(
                [
                    "border:none;",
                    f"border-radius:{self.back.height() // 2}px;",
                    f"background:{color};",
                ]
            )
        )

    def __clicked(self) -> None:
        self.nextCheckState()
        self.__switchToggle()
        self.valueChanged.emit()

    def __getFrontXPos(self) -> int:
        return self.__getFrontCheckedXPos() if self._isChecked else self.__getFrontRootXPos()

    def __getFrontYPos(self) -> int:
        return self._gap

    def __getFrontRootXPos(self) -> int:
        return self._gap

    def __getFrontCheckedXPos(self) -> int:
        size = self.size()
        return size.width() - size.height() + self._gap

    def __switchToggle(self) -> None:
        self._animation.stop()
        self._animation.setStartValue(self.front.pos().x())
        self._animation.setEndValue(self.__getFrontXPos())
        self._animation.start()
        self._isAnimating = True

    def __moveFrontButton(self, value: float) -> None:
        self.front.move(value, self.__getFrontYPos())
