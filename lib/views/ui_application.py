from sys import argv, exit, path

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .ui_player_music import UIPlayerMusic
from .window_settings_panel import SettingsWindow

path.append("./lib")
from constants.application import supportedLanguages
from constants.ui.qss import Background, ColorBoxes, Colors, Paddings
from constants.ui.qt import AppCursors, AppIcons
from modules.screens.components.factories import *
from utils.data.config_utils import getLanguagePack, getLanguagePackFromConfig
from utils.ui.application_utils import ApplicationUIUtils as AppUI
from widgets.framless_window import FramelessWindow


class ApplicationInterface(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(1368, 768)
        MainWindow.setTitleBarHeight(80)

        self.isDarkMode = True
        buttonFactory = IconButtonFactory()
        iconButtonFormer = buttonFactory.getByType("default")
        iconButtonThemeBuilder = iconButtonFormer.getThemeBuilder()
        icons = AppIcons()
        cursors = AppCursors()
        self.themeItems = {}
        self.buttonsWithDarkMode = []

        self.app_background = QLabel(MainWindow)
        self.app_background.resize(MainWindow.size())

        self.home_screen = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.home_screen)

        self.main_layout = QVBoxLayout(self.home_screen)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.title_bar = QHBoxLayout()
        self.title_bar.setContentsMargins(12, 12, 12, 12)
        self.title_bar.setSpacing(8)

        self.body = QVBoxLayout()
        self.body.setContentsMargins(0, 0, 0, 0)
        self.body.setSpacing(0)

        self.main_layout.addLayout(self.title_bar)
        self.main_layout.addLayout(self.body)
        self.main_layout.addStretch()

        self.open_settings_btn = iconButtonFormer.render(
            padding=Paddings.RELATIVE_25,
            size=icons.SIZES.LARGE,
            lightModeIcon=AppUI.paintIcon(icons.SETTINGS, Colors.PRIMARY),
            darkModeIcon=AppUI.paintIcon(icons.SETTINGS, Colors.WHITE),
        )
        self.__addButtonToList(self.open_settings_btn)
        self.minimize_btn = iconButtonFormer.render(
            padding=Paddings.RELATIVE_50,
            size=icons.SIZES.MEDIUM,
            lightModeIcon=AppUI.paintIcon(icons.MINIMIZE, Colors.PRIMARY),
        )
        self.__addThemeForItem(
            self.minimize_btn,
            theme=(
                iconButtonThemeBuilder.addLightModeBackground(
                    Background(
                        borderRadius=0.33,
                        color=ColorBoxes.PRIMARY_LIGHTEN_HOVERABLE_25,
                    )
                )
                .addDarkModeBackground(
                    Background(
                        borderRadius=0.33,
                        color=ColorBoxes.WHITE_LIGHTEN_HOVERABLE_25,
                    )
                )
                .build(self.minimize_btn.height())
            ),
        )
        self.minimize_btn.setCursor(cursors.HAND)
        self.minimize_btn.clicked.connect(MainWindow.showMinimized)

        self.close_btn = iconButtonFormer.render(
            padding=Paddings.RELATIVE_50,
            size=icons.SIZES.MEDIUM,
            lightModeIcon=AppUI.paintIcon(icons.CLOSE, Colors.DANGER),
        )
        self.__addThemeForItem(
            self.close_btn,
            theme=(
                iconButtonThemeBuilder.addLightModeBackground(
                    Background(
                        borderRadius=0.33,
                        color=ColorBoxes.DANGER_LIGHTEN_50,
                    )
                ).build(self.close_btn.height())
            ),
        )
        self.close_btn.setCursor(cursors.HAND)
        self.close_btn.clicked.connect(MainWindow.close)

        self.title_bar.addStretch()
        self.title_bar.addWidget(self.minimize_btn)
        self.title_bar.addWidget(self.close_btn)

        self.menu_bar = QHBoxLayout()
        self.menu_bar.setContentsMargins(20, 0, 20, 0)

        self.__addThemeForItem(
            self.open_settings_btn,
            theme=(
                iconButtonThemeBuilder.addLightModeBackground(None)
                .addDarkModeBackground(None)
                .build(self.open_settings_btn.height())
            ),
        )
        self.open_settings_btn.setCursor(cursors.HAND)
        self.open_settings_btn.clicked.connect(self.clickedOpenSettingBtn)

        self.__addButtonToList(self.open_settings_btn)
        self.menu_bar.addWidget(self.open_settings_btn)
        self.menu_bar.addStretch()

        self.playlist_carousel = QWidget()
        self.playlist_carousel.setFixedHeight(360)

        self.body.addLayout(self.menu_bar)
        self.body.addWidget(self.playlist_carousel)

        self.music_player = QWidget()
        self.music_player.setFixedHeight(96)
        self.music_player.setObjectName("music_player")

        self.main_layout.addWidget(self.music_player)
        self.player_layout = QHBoxLayout(self.music_player)
        self.player = UIPlayerMusic()
        self.player.displaySongInfo()
        self.player_layout.addWidget(self.player)

        self.settings_window = SettingsWindow(MainWindow)
        self.settings_window.setGeometry(QRect(434, 184, 500, 400))
        # self.settings_window.setGraphicsEffect(
        #     QGraphicsDropShadowEffect(
        #         blurRadius=50,
        #         color=QColor(128, 64, 255, 100),
        #         xOffset=0,
        #         yOffset=3,
        #     )
        # )
        self.settings_window.switch_dark_mode_btn.clicked.connect(
            self.switchDarkMode
        )
        QMetaObject.connectSlotsByName(MainWindow)

    def connectSignals(self, controllers: dict) -> None:
        self.player.connectSignals(controllers.get("music_player"))
        self.settings_window.connectSignals(controllers.get("application"))

    def switchDarkMode(self) -> None:
        self.isDarkMode = not self.isDarkMode
        if self.isDarkMode:
            self.darkMode()
        else:
            self.lightMode()

    def clickedOpenSettingBtn(self) -> None:
        self.settings_window.open()

    def darkMode(self) -> None:
        self.isDarkMode = True
        self.app_background.setStyleSheet("background:black;border-radius:24px")
        self.settings_window.darkMode()
        self.music_player.setStyleSheet(
            "QWidget#music_player{border-top: 1px solid #202020}"
        )
        self.player.darkMode()
        for button in self.buttonsWithDarkMode:
            button.setDarkMode(True)
        for item in self.themeItems:
            darkModeStyleSheet = self.themeItems.get(item).darkMode
            if darkModeStyleSheet is None or darkModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(darkModeStyleSheet)

    def lightMode(self) -> None:
        self.isDarkMode = False
        self.app_background.setStyleSheet("background:white;border-radius:24px")
        self.settings_window.lightMode()
        self.music_player.setStyleSheet(
            "QWidget#music_player{border-top: 1px solid #eaeaea}"
        )
        self.player.lightMode()
        for button in self.buttonsWithDarkMode:
            button.setDarkMode(False)
        for item in self.themeItems:
            lightModeStyleSheet = self.themeItems.get(item).lightMode
            if lightModeStyleSheet is None or lightModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(lightModeStyleSheet)

    def __addThemeForItem(self, item, theme: str) -> None:
        self.themeItems[item] = theme

    def __addButtonToList(self, item) -> None:
        self.buttonsWithDarkMode.append(item)

    def translate(self, language: dict) -> None:
        self.settings_window.translate(language)
        self.player.translate(language)
