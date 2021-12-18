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
from modules.screens.themes.theme_builders import ThemeData
from utils.data.config_utils import getLanguagePackage
from utils.ui.application_utils import ApplicationUIUtils as AppUI
from utils.ui.application_utils import ColorUtils
from widgets.framless_window import FramelessWindow


class ApplicationInterface(object):
    def setupUi(self):
        self.MainWindow = FramelessWindow()
        self.MainWindow.resize(1368, 768)
        self.MainWindow.setTitleBarHeight(80)

        self.isDarkMode = True
        buttonFactory = IconButtonFactory()
        iconButtonFormer = buttonFactory.getByType("default")
        iconButtonThemeBuilder = iconButtonFormer.getThemeBuilder()
        icons = AppIcons()
        cursors = AppCursors()
        self.themeItems = {}
        self.buttonsWithDarkMode = []

        backgroundTheme = ThemeData(
            lightMode="background:white;border-radius:24px",
            darkMode="background:black;border-radius:24px",
        )

        self.app_background = QLabel(self.MainWindow)
        self.app_background.resize(self.MainWindow.size())
        self.__addThemeForItem(self.app_background, theme=backgroundTheme)

        self.home_screen = QWidget(self.MainWindow)
        self.MainWindow.setCentralWidget(self.home_screen)

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
        self.minimize_btn.clicked.connect(self.MainWindow.showMinimized)

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
        self.close_btn.clicked.connect(self.MainWindow.close)

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
        self.__addThemeForItem(
            self.music_player,
            theme=ThemeData(
                lightMode="QWidget#music_player{border-top: 1px solid #eaeaea}",
                darkMode="QWidget#music_player{border-top: 1px solid #202020}",
            ),
        )
        self.main_layout.addWidget(self.music_player)
        self.music_player_layout = QHBoxLayout(self.music_player)
        self.music_player_inner = UIPlayerMusic(self.music_player)
        self.music_player_layout.addWidget(self.music_player_inner)

        self.settings_panel = QWidget(self.MainWindow)
        self.settings_panel.setGeometry(QRect(434, 184, 500, 400))
        self.settings_panel.setGraphicsEffect(
            QGraphicsDropShadowEffect(
                blurRadius=50,
                color=ColorUtils.getQColorFromColor(
                    Colors.PRIMARY.withAlpha(0.25)
                ),
                xOffset=0,
                yOffset=3,
            )
        )
        self.__addThemeForItem(self.settings_panel, theme=backgroundTheme)
        self.settings_panel.hide()

        self.settings_panel_inner = SettingsWindow(self.settings_panel)
        self.settings_panel_inner.close_settings_window_btn.clicked.connect(
            self.clickedOpenSettingBtn
        )

        QMetaObject.connectSlotsByName(self.MainWindow)

    def connectSignalsToControllers(self, controllers: dict) -> None:
        self.music_player_inner.connectSignalsToController(
            controllers.get("musicPlayer")
        )
        self.settings_panel_inner.connectSignalsToController(
            controllers.get("application")
        )

    def switchDarkMode(self, mode) -> None:
        self.isDarkMode = mode
        if self.isDarkMode:
            self.darkMode()
        else:
            self.lightMode()

    def clickedOpenSettingBtn(self) -> None:
        self.settings_panel.setVisible(not self.settings_panel.isVisible())

    def lightMode(self) -> None:
        self.isDarkMode = False
        self.settings_panel_inner.lightMode()
        self.music_player_inner.lightMode()

        for button in self.buttonsWithDarkMode:
            button.setDarkMode(False)
        for item in self.themeItems:
            lightModeStyleSheet = self.themeItems.get(item).lightMode
            if lightModeStyleSheet is None or lightModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(lightModeStyleSheet)

    def darkMode(self) -> None:
        self.isDarkMode = True
        self.settings_panel_inner.darkMode()
        self.music_player_inner.darkMode()

        for button in self.buttonsWithDarkMode:
            button.setDarkMode(True)
        for item in self.themeItems:
            darkModeStyleSheet = self.themeItems.get(item).darkMode
            if darkModeStyleSheet is None or darkModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(darkModeStyleSheet)

    def __addThemeForItem(self, item, theme: ThemeData) -> None:
        self.themeItems[item] = theme

    def __addButtonToList(self, item) -> None:
        self.buttonsWithDarkMode.append(item)

    def translate(self, language: dict) -> None:
        self.settings_panel_inner.translate(language)
        self.music_player_inner.translate(language)

    def show(self):
        self.MainWindow.show()

    def displayDataRetrievedFrom(self, settingsData: dict) -> None:
        isDarkMode = settingsData.get("darkMode")
        language = settingsData.get("language")
        self.settings_panel_inner.change_language_dropdown.setCurrentIndex(
            supportedLanguages.index(language)
        )
        self.translate(getLanguagePackage(language))
        self.settings_panel_inner.switch_dark_mode_btn.setChecked(isDarkMode)
        self.settings_panel_inner.current_folder.setText(
            settingsData.get("path")
        )
        self.switchDarkMode(isDarkMode)
