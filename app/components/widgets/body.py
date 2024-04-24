from typing import Optional

from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout


class Body(QScrollArea):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.__initUI()

    def __initUI(self) -> None:
        self._inner = QWidget()
        self.setWidget(self._inner)

        self._mainLayout = QVBoxLayout(self._inner)
        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainLayout.setSpacing(50)

    def addWidget(self, widget: QWidget) -> None:
        self._mainLayout.addWidget(widget)
