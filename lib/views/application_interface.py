from typing import Optional

from modules.screens.themes.theme_builders import ThemeData
from PyQt5.QtCore import QMetaObject, Qt

from .body.body import HomeScreen
from .menu_bar.menu_bar import MenuBar
from .music_player.music_player import UIPlayerMusic
from .view import View
from .windows.main_window import MainWindow


class ApplicationInterface(View):
    def __init__(self):
        super(ApplicationInterface, self).__init__()
        self.isDarkMode = True
        self.setupUi()

    def setupUi(self) -> None:
        self.mainWindow = MainWindow()
        self.mainWindow.resize(1368, 768)
        self.mainWindow.setTitleBarHeight(80)

        self.menuBar = MenuBar()
        self.menuBar.setContentsMargins(20, 0, 20, 0)

        self.body = HomeScreen()
        self.body.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.body.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.body.setWidgetResizable(True)

        self.musicPlayer = UIPlayerMusic()
        self.musicPlayer.setFixedHeight(96)
        self.musicPlayer.setObjectName("musicPlayer")
        self._addThemeForItem(
            self.musicPlayer,
            theme=ThemeData(
                lightMode="QWidget#musicPlayer{border-top: 1px solid #eaeaea}",
                darkMode="QWidget#musicPlayer{border-top: 1px solid #202020}",
            ),
        )

        self.mainWindow.addLayout(self.menuBar)
        self.mainWindow.addWidget(self.body)
        self.mainWindow.addWidget(self.musicPlayer, alignment=Qt.AlignBottom)

        QMetaObject.connectSlotsByName(self.mainWindow)

    def connectToControllers(self, controllers) -> None:
        self.menuBar.connectToControllers(controllers)
        self.body.connectToControllers(controllers)

    def switchDarkMode(self, mode) -> None:
        self.isDarkMode = mode
        if self.isDarkMode:
            self.darkMode()
            return
        self.lightMode()

    def lightMode(self) -> None:
        self.isDarkMode = False
        self.mainWindow.lightMode()
        self.menuBar.lightMode()
        self.musicPlayer.lightMode()
        self.body.lightMode()
        super().lightMode()

    def darkMode(self) -> None:
        self.isDarkMode = True
        self.mainWindow.darkMode()
        self.menuBar.darkMode()
        self.musicPlayer.darkMode()
        self.body.darkMode()
        super().darkMode()

    def translate(self, language: dict[str, str]) -> None:
        self.menuBar.translate(language)
        self.musicPlayer.translate(language)
