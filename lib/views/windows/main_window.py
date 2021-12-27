from typing import Optional

from constants.ui.base import ApplicationImage
from constants.ui.qss import Backgrounds, Colors, Paddings
from constants.ui.qt import AppCursors, AppIcons
from modules.screens.components.icon_buttons import IconButton
from modules.screens.components.playlist_info import PlaylistInfo
from modules.screens.themes.theme_builders import ButtonThemeBuilder, ThemeData
from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtWidgets import (QGraphicsDropShadowEffect, QHBoxLayout,
                             QScrollArea, QVBoxLayout, QWidget)
from utils.ui.application_utils import UiUtils
from utils.ui.color_utils import ColorUtils
from views.view import View
from widgets.framless_window import FramelessWindow


class ApplicationInterface(FramelessWindow, View):
    def __init__(self, parent: Optional["QWidget"]):
        super(ApplicationInterface, self).__init__(parent)
        self.setupUi()

    def setupUi(self) -> None:
        btnThemeBuilder = ButtonThemeBuilder()
        icons = AppIcons()

        backgroundTheme = ThemeData(
            lightMode="background:WHITE;border-radius:24px",
            darkMode="background:BLACK;border-radius:24px",
        )

        self.background = QWidget(self)
        self.background.resize(self.size())
        self._addThemeForItem(self.background, theme=backgroundTheme)

        self.home_screen = QWidget(self)
        self.setCentralWidget(self.home_screen)

        self.mainLayout = QVBoxLayout(self.home_screen)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.title_bar = QHBoxLayout()
        self.title_bar.setContentsMargins(12, 12, 12, 12)
        self.title_bar.setSpacing(8)

        self.body = QScrollArea()
        self.body.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.body.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.body.setWidgetResizable(True)
        self.body.setStyleSheet("background:TRANSPARENT;border:none")
        self.body_inner = QWidget()
        self.body.setWidget(self.body_inner)
        self.body_layout = QVBoxLayout(self.body_inner)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(0)

        self.mainLayout.addLayout(self.title_bar)
        self.mainLayout.addWidget(self.body)

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

        self.title_bar.addStretch()
        self.title_bar.addWidget(self.minimize_btn)
        self.title_bar.addWidget(self.close_btn)

        QMetaObject.connectSlotsByName(self)

    def setTitleBarHeight(self, height: int) -> None:
        return super().setTitleBarHeight(height)

    def addWidget(self, widget: Optional["QWidget"]) -> None:
        self.mainLayout.addWidget(widget)

    def addLayout(self, widget: Optional["QWidget"]) -> None:
        self.mainLayout.addLayout(widget)
