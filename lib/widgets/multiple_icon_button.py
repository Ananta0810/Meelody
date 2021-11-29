from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton


class QMultipleIconButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.iconList: list[QIcon] = []
        self.currentIconIndex = 0
        self.changeIconOnPressed = False
        self.currentIcon = None

    def setIconList(self, list: list[QIcon]):
        self.iconList = list

    def setChangeIconOnPressed(self, a0: bool):
        self.changeIconOnPressed = a0

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.changeIconOnPressed:
            self.currentIconIndex = (self.currentIconIndex + 1) % len(self.iconList)
        self.__changeIconBaseOnState()

    def setCurrentIcon(self, iconIndex):
        if iconIndex >= len(self.iconList):
            return
        self.currentIconIndex = iconIndex
        self.__changeIconBaseOnState()

    def __changeIconBaseOnState(self):
        self.setIcon(self.iconList[self.currentIconIndex])
