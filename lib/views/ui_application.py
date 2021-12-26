from typing import Optional

from constants.ui.base import ApplicationImage
from constants.ui.qss import ColorBoxes, Colors, Paddings
from constants.ui.qt import AppCursors, AppIcons
from modules.screens.components.icon_buttons import IconButton
from modules.screens.components.playlist_info import PlaylistInfo
from modules.screens.qss.qss_elements import Background
from modules.screens.themes.theme_builders import ThemeData
from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QHBoxLayout, QScrollArea, QVBoxLayout, QWidget
from utils.ui.application_utils import UiUtils
from utils.ui.color_utils import ColorUtils
from widgets.framless_window import FramelessWindow

from .playlist_menu import PlaylistTable
from .ui_player_music import UIPlayerMusic
from .ui_playlist_carousel import UiPlaylistCarousel
from .window_settings_panel import SettingsPanel


class ApplicationInterface(object):
    def __init__(self):
        self.setupUi()

    def setupUi(self):
        self.MainWindow = FramelessWindow()
        self.MainWindow.resize(1368, 768)
        self.MainWindow.setTitleBarHeight(80)

        self.isDarkMode = True
        iconButtonThemeBuilder = IconButton.getThemeBuilder()
        icons = AppIcons()
        self.themeItems = {}
        self.buttonsWithDarkMode = []

        backgroundTheme = ThemeData(
            lightMode="background:WHITE;border-radius:24px",
            darkMode="background:BLACK;border-radius:24px",
        )

        self.app_background = QWidget(self.MainWindow)
        self.app_background.resize(self.MainWindow.size())
        self.__addThemeForItem(self.app_background, theme=backgroundTheme)

        self.home_screen = QWidget(self.MainWindow)
        self.MainWindow.setCentralWidget(self.home_screen)

        self.main_layout = QVBoxLayout(self.home_screen)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

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

        self.main_layout.addLayout(self.title_bar)
        self.main_layout.addWidget(self.body)

        self.minimize_btn = IconButton.render(
            padding=Paddings.RELATIVE_50,
            size=icons.SIZES.MEDIUM,
            lightModeIcon=UiUtils.paintIcon(icons.MINIMIZE, Colors.PRIMARY),
            darkModeIcon=UiUtils.paintIcon(icons.MINIMIZE, Colors.WHITE),
        )
        self.__addButtonToList(self.minimize_btn)
        self.__addThemeForItem(
            self.minimize_btn,
            theme=(
                iconButtonThemeBuilder.addLightModeBackground(
                    Background(
                        borderRadius=0.33,
                        color=ColorBoxes.HOVERABLE_PRIMARY_25,
                    )
                )
                .addDarkModeBackground(
                    Background(
                        borderRadius=0.33,
                        color=ColorBoxes.HOVERABLE_WHITE_25,
                    )
                )
                .build(self.minimize_btn.height())
            ),
        )
        self.minimize_btn.setCursor(AppCursors.hand())
        self.minimize_btn.clicked.connect(self.MainWindow.showMinimized)

        self.close_btn = IconButton.render(
            padding=Paddings.RELATIVE_50,
            size=icons.SIZES.MEDIUM,
            lightModeIcon=UiUtils.paintIcon(icons.CLOSE, Colors.DANGER),
        )
        self.__addThemeForItem(
            self.close_btn,
            theme=(
                iconButtonThemeBuilder.addLightModeBackground(
                    Background(
                        borderRadius=0.33,
                        color=ColorBoxes.DANGER_50,
                    )
                )
                .addDarkModeBackground(None)
                .build(self.close_btn.height())
            ),
        )
        self.close_btn.setCursor(AppCursors.hand())
        self.close_btn.clicked.connect(self.MainWindow.close)

        self.title_bar.addStretch()
        self.title_bar.addWidget(self.minimize_btn)
        self.title_bar.addWidget(self.close_btn)

        self.menu_bar = QHBoxLayout()
        self.menu_bar.setContentsMargins(20, 0, 20, 0)

        self.open_settings_btn = IconButton.render(
            padding=Paddings.RELATIVE_25,
            size=icons.SIZES.LARGE,
            lightModeIcon=UiUtils.paintIcon(icons.SETTINGS, Colors.PRIMARY),
            darkModeIcon=UiUtils.paintIcon(icons.SETTINGS, Colors.WHITE),
        )
        self.__addButtonToList(self.open_settings_btn)
        self.__addThemeForItem(
            self.open_settings_btn,
            theme=(iconButtonThemeBuilder.addLightModeBackground(None).build(icons.SIZES.LARGE.height())),
        )
        self.open_settings_btn.setCursor(AppCursors.hand())
        self.open_settings_btn.clicked.connect(self.clickedOpenSettingBtn)

        self.__addButtonToList(self.open_settings_btn)
        self.menu_bar.addWidget(self.open_settings_btn)
        self.menu_bar.addStretch()

        self.playlist_carousel = UiPlaylistCarousel()
        self.playlist_carousel.setFixedHeight(360)
        self.playlist_carousel.setStyleSheet("background:TRANSPARENT;border:none")
        self.playlist_carousel.main_layout.setContentsMargins(84, 0, 50, 0)

        self.currentPlaylist = QHBoxLayout()
        self.currentPlaylist.setAlignment(Qt.AlignLeft)
        self.currentPlaylist.setContentsMargins(84, 50, 50, 0)
        self.currentPlaylist.setSpacing(50)
        self.playlist_info = QVBoxLayout()

        self.playlist_info = PlaylistInfo()
        self.playlist_info.setDefaultCover(ApplicationImage.defaultPlaylistCover)
        self.playlistMenu = PlaylistTable()
        self.playlistMenu.setFixedHeight(600)

        self.currentPlaylist.addLayout(self.playlist_info)
        self.currentPlaylist.addWidget(self.playlistMenu, stretch=2)

        self.body_layout.addLayout(self.menu_bar)
        self.body_layout.addWidget(self.playlist_carousel)
        self.body_layout.addLayout(self.currentPlaylist)
        # self.body_layout.addStretch()

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
        self.main_layout.addWidget(self.music_player, alignment=Qt.AlignBottom)
        self.music_player_layout = QHBoxLayout(self.music_player)
        self.music_player_inner = UIPlayerMusic(self.music_player)
        self.music_player_layout.addWidget(self.music_player_inner)

        self.settings_panel = SettingsPanel(self.MainWindow)
        self.settings_panel.setFixedSize(500, 400)
        self.settings_panel.move(self.MainWindow.rect().center() - self.settings_panel.rect().center())
        self.settings_panel.setGraphicsEffect(
            QGraphicsDropShadowEffect(
                blurRadius=50,
                color=ColorUtils.getQColorFromColor(Colors.PRIMARY.withAlpha(0.25)),
                xOffset=0,
                yOffset=3,
            )
        )
        self.__addThemeForItem(self.settings_panel, theme=backgroundTheme)
        self.settings_panel.hide()

        self.settings_panel.close_settings_window_btn.clicked.connect(self.clickedOpenSettingBtn)

        QMetaObject.connectSlotsByName(self.MainWindow)

    def connectSignalsToControllers(self, controllers) -> None:
        self.settings_panel.connectSignalsToController(controllers.get("application"))
        self.music_player_inner.connectSignalsToController(controllers.get("musicPlayer"))
        self.playlist_carousel.connectSignalsToController(controllers.get("playlistCarousel"))
        self.playlistMenu.connectSignalsToController(controllers.get("playlistMenu"))
        # self.playlsit_carousel.connectSignalsToController(controllers.get("playlistSelector"))

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
        self.settings_panel.lightMode()
        self.music_player_inner.lightMode()
        self.playlist_carousel.lightMode()
        self.playlist_info.lightMode()
        self.playlistMenu.lightMode()

        for button in self.buttonsWithDarkMode:
            button.setDarkMode(False)
        for item in self.themeItems:
            lightModeStyleSheet = self.themeItems.get(item).lightMode
            if lightModeStyleSheet is None or lightModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(lightModeStyleSheet)

    def darkMode(self) -> None:
        self.isDarkMode = True
        self.settings_panel.darkMode()
        self.music_player_inner.darkMode()
        self.playlist_carousel.darkMode()
        self.playlist_info.darkMode()
        self.playlistMenu.darkMode()

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

    def translate(self, language: dict[str, str]) -> None:
        self.settings_panel.translate(language)
        self.music_player_inner.translate(language)
