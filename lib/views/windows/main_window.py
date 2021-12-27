from typing import Optional, Union

from constants.ui.qss import Backgrounds, Colors, Paddings
from constants.ui.qt import AppCursors, AppIcons
from modules.screens.components.icon_buttons import IconButton
from modules.screens.themes.theme_builders import ButtonThemeBuilder, ThemeData
from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QHBoxLayout, QLayout, QScrollArea, QVBoxLayout, QWidget
from utils.ui.application_utils import UiUtils
from views.view import View
from widgets.framless_window import FramelessWindow


class MainWindow(FramelessWindow, View):
    def __init__(self, parent: Optional["QWidget"] = None):
        super(MainWindow, self).__init__(parent)
        self.setupUi()

    def setupUi(self) -> None:
        btnThemeBuilder = ButtonThemeBuilder()
        icons = AppIcons()

        backgroundTheme = ThemeData(
            lightMode="background:WHITE;border-radius:24px",
            darkMode="background:BLACK;border-radius:24px",
        )

        self.background = QWidget(self)
        self._addThemeForItem(self.background, theme=backgroundTheme)

        self.home_screen = QWidget(self)
        self.setCentralWidget(self.home_screen)

        self.mainLayout = QVBoxLayout(self.home_screen)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.titleBar = QHBoxLayout()
        self.titleBar.setContentsMargins(12, 12, 12, 12)
        self.titleBar.setSpacing(8)
        self.mainLayout.addLayout(self.titleBar)

        self.minimize_btn = IconButton.render(
            padding=Paddings.RELATIVE_50,
            size=icons.SIZES.MEDIUM,
            lightModeIcon=UiUtils.paintIcon(icons.MINIMIZE, Colors.PRIMARY),
            darkModeIcon=UiUtils.paintIcon(icons.MINIMIZE, Colors.WHITE),
        )
        self._addButtonToList(self.minimize_btn)
        self._addThemeForItem(
            self.minimize_btn,
            theme=(
                btnThemeBuilder.addLightModeBackground(Backgrounds.ROUNDED_PRIMARY_25)
                .addDarkModeBackground(Backgrounds.ROUNDED_WHITE_25)
                .build()
            ),
        )
        self.minimize_btn.setCursor(AppCursors.hand())
        self.minimize_btn.clicked.connect(self.showMinimized)

        self.close_btn = IconButton.render(
            padding=Paddings.RELATIVE_50,
            size=icons.SIZES.MEDIUM,
            lightModeIcon=UiUtils.paintIcon(icons.CLOSE, Colors.WHITE),
        )
        self._addThemeForItem(
            self.close_btn,
            theme=(
                btnThemeBuilder.addLightModeBackground(Backgrounds.ROUNDED_DANGER).addDarkModeBackground(None).build()
            ),
        )
        self.close_btn.setCursor(AppCursors.hand())
        self.close_btn.clicked.connect(self.close)

        self.titleBar.addStretch()
        self.titleBar.addWidget(self.minimize_btn)
        self.titleBar.addWidget(self.close_btn)

        QMetaObject.connectSlotsByName(self)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.background.resize(self.size())
        return super().resizeEvent(a0)

    def setTitleBarHeight(self, height: int) -> None:
        return super().setTitleBarHeight(height)

    def addLayout(self, widget: Optional["QWidget"]) -> None:
        self.mainLayout.addLayout(widget)

    def addWidget(self, a0: QWidget, stretch: int = 0, alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = None) -> None:
        if alignment is None:
            self.mainLayout.addWidget(a0, stretch)
            return
        self.mainLayout.addWidget(a0, stretch, alignment)

    def addLayout(self, layout: QLayout) -> None:
        self.mainLayout.addLayout(layout)

    # def addLayout(self, layout: QLayout, stretch: int = ...) -> None:
    #     self.mainLayout.addLayout(layout, stretch=stretch)
