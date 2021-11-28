from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton


class QToggleButton(QPushButton):
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
        self.__changeIconBaseOnState(a0)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.__changeIconBaseOnState(not self.isChecked())

    def __changeIconBaseOnState(self, checked: bool):
        if not self.isCheckable():
            return
        if checked:
            self.setIcon(self.checkedIcon)
        else:
            self.setIcon(self.normalIcon)
