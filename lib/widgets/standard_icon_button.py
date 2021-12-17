from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton


class QIconButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lightModeIcon = None
        self.darkModeIcon = None
        self.isDarkMode = False

    def setLightModeIcon(self, icon: QIcon):
        self.lightModeIcon = icon

    def setDarkModeIcon(self, icon: QIcon):
        self.darkModeIcon = icon

    def setDarkMode(self, a0: bool):
        self.isDarkMode = a0
        self.__changeIconBaseOnState()

    def __changeIconBaseOnState(self):
        if self.isDarkMode:
            self.setIcon(
                self.lightModeIcon
                if self.darkModeIcon is None
                else self.darkModeIcon
            )
        else:
            self.setIcon(self.lightModeIcon)
