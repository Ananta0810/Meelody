from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton


class QToggleButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.normalIcon = None
        self.darkModeNormalIcon = None
        self.checkedIcon = None
        self.darkModeCheckedIcon = None
        self.isDarkMode = False
        self.currentNormalIcon = None
        self.currentCheckedIcon = None
        self._isChangeIconWhenClicked = True

    def setChangeIconWhenClicked(self, state: bool) -> None:
        self._isChangeIconWhenClicked = state

    def setLightModeNormalIcon(self, icon: QIcon):
        self.normalIcon = icon

    def setLightModeCheckedIcon(self, icon: QIcon):
        self.checkedIcon = icon

    def setDarkModeNormalIcon(self, icon: QIcon):
        self.darkModeNormalIcon = icon

    def setDarkModeCheckedIcon(self, icon: QIcon):
        self.darkModeCheckedIcon = icon

    def setDarkMode(self, a0: bool):
        self.isDarkMode = a0
        self.__changeIconBaseOnState(self.isChecked())

    def setChecked(self, a0: bool):
        super().setChecked(a0)
        self.__changeIconBaseOnState(a0)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self._isChangeIconWhenClicked:
            self.__changeIconBaseOnState(not self.isChecked())

    def __changeIconBaseOnState(self, checked: bool):
        if not self.isCheckable():
            return
        if checked:
            self.setIcon(self.__getCurrentCheckedIcon())
        else:
            self.setIcon(self.__getCurrentNormalIcon())

    def __getCurrentNormalIcon(self):
        return self.darkModeNormalIcon if self.isDarkMode and self.darkModeNormalIcon is not None else self.normalIcon

    def __getCurrentCheckedIcon(self):
        return (
            self.darkModeCheckedIcon if self.isDarkMode and self.darkModeCheckedIcon is not None else self.checkedIcon
        )
