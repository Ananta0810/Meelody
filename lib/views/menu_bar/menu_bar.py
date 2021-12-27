from typing import Optional

from constants.ui.qss import Background, Colors, Paddings
from constants.ui.qt import AppCursors, AppIcons
from modules.screens.components.icon_buttons import IconButton
from modules.screens.themes.theme_builders import ButtonThemeBuilder, ThemeData
from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QHBoxLayout, QScrollArea, QVBoxLayout, QWidget
from utils.ui.application_utils import UiUtils
from utils.ui.color_utils import ColorUtils
from views.dialogs.settings_dialog import SettingsDialog
from views.view import View


class MenuBar(QHBoxLayout, View):
    def __init__(self, parent: Optional["QWidget"] = None):
        super(MenuBar, self).__init__(parent)
        self.setupUi()

    def setupUi(self) -> None:
        icons = AppIcons()

        self.openSettingBtn = IconButton.render(
            padding=Paddings.RELATIVE_25,
            size=icons.SIZES.LARGE,
            lightModeIcon=UiUtils.paintIcon(icons.SETTINGS, Colors.PRIMARY),
            darkModeIcon=UiUtils.paintIcon(icons.SETTINGS, Colors.WHITE),
        )
        self._addButtonToList(self.openSettingBtn)
        self._addThemeForItem(
            self.openSettingBtn,
            theme=(ButtonThemeBuilder().addLightModeBackground(None).build()),
        )
        self.openSettingBtn.setCursor(AppCursors.hand())
        # self.openSettingBtn.clicked.connect(self.openSettingsDiaglog)

        self._addButtonToList(self.openSettingBtn)
        self.addWidget(self.openSettingBtn)
        self.addStretch()

        # self.settingsPanel = SettingsDialog(self.mainWindow)
        # self.settingsPanel.setFixedSize(500, 400)
        # self.settingsPanel.setGraphicsEffect(
        #     QGraphicsDropShadowEffect(
        #         blurRadius=50,
        #         color=ColorUtils.getQColorFromColor(Colors.PRIMARY.withAlpha(0.25)),
        #         xOffset=0,
        #         yOffset=3,
        #     )
        # )
        # self._addThemeForItem(
        #     self.settingsPanel,
        #     theme=ThemeData(
        #         lightMode="background:white;border-radius:24px",
        #         darkMode="background:black;border-radius:24px",
        #     ),
        # )
        # self.settingsPanel.hide()
        # self.settingsPanel.close_settings_window_btn.clicked.connect(self.openSettingsDiaglog)

    def connectToControllers(self, controllers) -> None:
        # self.settingsPanel.connectToController(controllers.get("application"))
        # self.playlsit_carousel.connectToController(controllers.get("playlistSelector"))
        pass

    # def openSettingsDiaglog(self) -> None:
    #     self.settingsPanel.setVisible(not self.settingsPanel.isVisible())

    def lightMode(self) -> None:
        return super().lightMode()

    def darkMode(self) -> None:
        return super().darkMode()

    def translate(self, language: dict[str, str]) -> None:
        # self.settingsPanel.translate(language)
        pass
