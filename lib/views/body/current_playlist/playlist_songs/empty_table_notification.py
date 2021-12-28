from typing import Optional

from constants.ui.base import ApplicationImage
from constants.ui.qss import Backgrounds, ColorBoxes
from constants.ui.qt import IconSizes
from modules.screens.themes.theme_builders import ButtonThemeBuilder, LabelThemeBuilder, ThemeData
from PyQt5.QtCore import QEvent, Qt, pyqtSignal
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget
from utils.ui.application_utils import UiUtils
from views.view import View
from widgets.image_displayer import ImageDisplayer


class EmptySongTableNotification(QWidget, View):
    def __init__(self, parent: Optional["QWidget"] = None) -> None:
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(8)

        edge: int = 128
        self.img = ImageDisplayer()
        self.img.setFixedSize(edge, edge)
        self.img.setPixmap(UiUtils.getEditedPixmapFromBytes(ApplicationImage.errorPlaylist, width=edge, height=edge))
        self.mainLayout.addWidget(self.img)

        self.label = QLineEdit()
        self.label.setReadOnly(True)
        self.label.setStyleSheet("background:red")
        self.label.setAlignment(Qt.AlignCenter)
        self.mainLayout.addWidget(self.label)

        self.button = QPushButton()
        self.button.setStyleSheet("background:red")
        self.mainLayout.addWidget(self.button)

    def setMessage(self, label: str, button: str) -> None:
        self.label.setText(label)
        self.button.setText(button)
