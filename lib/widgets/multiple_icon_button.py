from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton


class QMultipleIconButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.iconList: dict[str, QIcon] = []
        # self.currentIconIndex = 0
        self.changeIconOnPressed = False
        self.currentIcon = None

    def setIconList(self, list: dict[str, QIcon]):
        self.iconList = list

    def setChangeIconOnPressed(self, a0: bool):
        self.changeIconOnPressed = a0

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # if self.changeIconOnPressed:
        # self.currentIconIndex = (self.currentIconIndex + 1) % len(self.iconList)
        # self.__changeIconBaseOnState()

    def setCurrentIcon(self, iconId):
        if iconId not in self.iconList:
            return
        # self.currentIconIndex = iconIndex
        self.currentIcon = self.iconList[iconId]
        self.__changeIconBaseOnState()

    def __changeIconBaseOnState(self):
        self.setIcon(self.currentIcon)
