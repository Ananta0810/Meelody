from typing import Optional

from constants.ui.base import ApplicationImage
from constants.ui.qss import Backgrounds, ColorBoxes, Paddings
from constants.ui.qt import AppCursors
from lib.modules.screens.themes.theme_builders import ThemeData
from modules.screens.components.action_buttons import ActionButton
from modules.screens.components.font_builder import FontBuilder
from modules.screens.components.labels import StandardLabel
from modules.screens.themes.theme_builders import ActionButtonThemeBuilder, LabelThemBuilder
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QShowEvent
from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout, QWidget
from utils.ui.application_utils import UiUtils
from views.view import View
from widgets.image_displayer import ImageDisplayer


class EmptySongTableNotification(QWidget, View):
    def __init__(self, parent: Optional["QWidget"] = None) -> None:
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setContentsMargins(32, 32, 32, 32)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(12)
        self.mainLayout.setAlignment(Qt.AlignCenter)

        edge: int = 200
        self.img = ImageDisplayer()
        self.img.setFixedSize(edge, edge)
        self.img.setPixmap(UiUtils.getEditedPixmapFromBytes(ApplicationImage.errorPlaylist, width=edge, height=edge))
        self.mainLayout.addWidget(self.img, alignment=Qt.AlignCenter)

        self.label = StandardLabel.render(FontBuilder().withSize(11).build())
        self.label.setAlignment(Qt.AlignHCenter)
        self.mainLayout.addWidget(self.label, alignment=Qt.AlignCenter)
        self._addThemeForItem(
            self.label,
            theme=(
                LabelThemBuilder()
                .addLightModeTextColor(ColorBoxes.BLACK)
                .addDarkModeTextColor(ColorBoxes.WHITE)
                .build()
            ),
        )

        self.button = ActionButton.render(
            font=FontBuilder().withSize(10).withWeight("bold").build(), padding=Paddings.LABEL_LARGE
        )
        self.button.setCursor(AppCursors().HAND)
        self.button.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.mainLayout.addWidget(self.button, alignment=Qt.AlignCenter)
        self._addThemeForItem(
            self.button,
            theme=(
                ActionButtonThemeBuilder()
                .addLightModeTextColor(ColorBoxes.WHITE)
                .addLightModeBackground(Backgrounds.ROUNDED_PRIMARY)
                .build()
            ),
        )

    def showEvent(self, a0: QShowEvent) -> None:
        self.setFixedSize(self.sizeHint())
        return super().showEvent(a0)

    def setMessage(self, label: str, button: str) -> None:
        self.label.setText(label)
        self.button.setText(button)
