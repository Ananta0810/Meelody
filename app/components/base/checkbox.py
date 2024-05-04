from typing import Optional

from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton

from app.components.base import Component
from app.components.widgets import ExtendableStyleWidget, FlexBox
from app.helpers.stylesheets import Colors
from app.resource.qt import Cursors, Icons


class CheckBox(ExtendableStyleWidget):
    checked = pyqtSignal()
    unchecked = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        self.__states = {}
        self.__checked: bool = False

        super().__init__(parent)
        self._initComponent()

    def _createUI(self) -> None:
        super()._createUI()
        self._mainLayout = FlexBox(self)

        self._normal = _CheckBoxState()
        self._normal.setCursor(Cursors.HAND)
        self._normal.setClassName("bg-white rounded-4 border border-gray-[w50] hover:bg-primary-12 hover:border-primary hover:border-2 p-2")

        self._active = _CheckBoxState()
        self._active.setCursor(Cursors.HAND)
        self._active.setClassName("bg-primary rounded-4 border border-primary hover:bg-primary-[w125] p-2")
        self._active.setIcon(Icons.APPLY.withColor(color=Colors.WHITE))
        self._active.hide()

        self._mainLayout.addWidget(self._normal)
        self._mainLayout.addWidget(self._active)

    def _connectSignalSlots(self) -> None:
        self._normal.clicked.connect(self.nextCheckState)
        self._active.clicked.connect(self.nextCheckState)

    def nextCheckState(self) -> None:
        self.setCheckState(not self.__checked)

    def setCheckState(self, checked: bool) -> None:
        self.__checked = checked
        self._normal.setVisible(not checked)
        self._active.setVisible(checked)

        if checked:
            self.checked.emit()
        else:
            self.unchecked.emit()

    def isChecked(self) -> bool:
        return self.__checked

    def setFixedWidth(self, w: int) -> None:
        super().setFixedWidth(w)
        self._normal.setFixedSize(w, w)
        self._active.setFixedSize(w, w)
        self._active.setIconSize(QSize(w, w))


class _CheckBoxState(QPushButton, Component):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._initComponent()
