from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton


class ToggleButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.normalIcon = None
        self.checkedIcon = None

    def setNormalIcon(self, icon: QIcon):
        self.normalIcon = icon

    def setCheckedIcon(self, icon: QIcon):
        self.checkedIcon = icon

    def setChecked(self, a0: bool):
        super().setChecked(a0)
        self.__changeIconBaseOnState()

    def mousePressEvent(self, QMouseEvent):
        if self.normalIcon is None or self.checkedIcon is None:
            return
        self.setChecked(not self.isChecked())
        self.__changeIconBaseOnState()

    def __changeIconBaseOnState(self):
        if self.isChecked():
            self.setIcon(self.checkedIcon)
        else:
            self.setIcon(self.normalIcon)
