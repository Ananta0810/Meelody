from typing import Optional

from constants.application import supportedLanguages
from constants.ui.qss import Backgrounds, ColorBoxes, Colors, Paddings
from constants.ui.qt import AppCursors, AppIcons
from modules.screens.components.dropdowns import DropdownMenu
from modules.screens.components.font_builder import FontBuilder
from modules.screens.components.icon_buttons import IconButton
from modules.screens.components.labels import LabelWithDefaultText
from modules.screens.qss.qss_elements import Background, Border, ColorBox
from modules.screens.themes.theme_builders import ButtonThemeBuilder, LabelThemBuilder
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QVBoxLayout, QWidget
from utils.ui.application_utils import UiUtils
from views.view import View
from widgets.toggle import Toggle


class SettingsDialog(QWidget, View):
    def __init__(self, parent: Optional["QWidget"] = None):
        super(SettingsDialog, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        iconButtonThemeBuilder = ButtonThemeBuilder()
        icons = AppIcons()
        cursors = AppCursors()
        fontBuilder = FontBuilder()
        labelThemBuilder = LabelThemBuilder()
        buttonWithCheveronTheme = (
            iconButtonThemeBuilder.addLightModeBackground(Backgrounds.CIRCLE_PRIMARY_25)
            .addDarkModeBackground(Backgrounds.CIRCLE_WHITE_25)
            .build(icons.SIZES.LARGE.height() * 0.67)
        )
        iconTheme = (
            iconButtonThemeBuilder.addLightModeBackground(Backgrounds.CIRCLE_PRIMARY_25)
            .addDarkModeBackground(Backgrounds.CIRCLE_WHITE_25)
            .build(itemSize=48)
        )
        itemFont = fontBuilder.withSize(9).build()
        itemTextStyle = (
            labelThemBuilder.addLightModeTextColor(ColorBoxes.BLACK).addDarkModeTextColor(ColorBoxes.WHITE).build()
        )

        # =========================UI=========================
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)
        self.setAttribute(Qt.WA_StyledBackground, True)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.mainLayout = QVBoxLayout(self)

        self.header = QHBoxLayout()
        self.header.setContentsMargins(8, 8, 8, 8)
        self.body = QVBoxLayout()
        self.body.setContentsMargins(48, 8, 48, 8)
        self.body.setSpacing(16)
        self.mainLayout.addLayout(self.header)
        self.mainLayout.addLayout(self.body, stretch=3)
        self.mainLayout.addStretch()

        self.closePanelBtn = IconButton.render(
            padding=Paddings.RELATIVE_75,
            size=icons.SIZES.LARGE,
            lightModeIcon=UiUtils.paintIcon(icons.BACKWARD, Colors.PRIMARY),
            darkModeIcon=UiUtils.paintIcon(icons.BACKWARD, Colors.WHITE),
        )
        self._addThemeForItem(self.closePanelBtn, theme=buttonWithCheveronTheme)
        self._addButtonToList(self.closePanelBtn)
        self.closePanelBtn.setCursor(cursors.HAND)
        self.header.addWidget(self.closePanelBtn)
        self.header.addStretch()

        self.settingsLabel = LabelWithDefaultText.render(fontBuilder.withSize(24).withWeight("bold").build())
        self._addThemeForItem(self.settingsLabel, itemTextStyle)
        self.body.addWidget(self.settingsLabel)

        self.settingsItems = QVBoxLayout()
        self.body.addLayout(self.settingsItems, stretch=1)
        self.settingsItemLanguage = QHBoxLayout()
        self.settingsItemLanguage.setSpacing(8)
        self.settingsItemDarkMode = QHBoxLayout()
        self.settingsItemDarkMode.setSpacing(8)
        self.settingsItemFolder = QHBoxLayout()
        self.settingsItemFolder.setSpacing(8)
        self.settingsItems.addLayout(self.settingsItemLanguage)
        self.settingsItems.addLayout(self.settingsItemDarkMode)
        self.settingsItems.addLayout(self.settingsItemFolder)

        # ===================Langauges===================
        self.languageIcon = IconButton.render(
            padding=Paddings.RELATIVE_50,
            size=icons.SIZES.LARGE,
            lightModeIcon=UiUtils.paintIcon(icons.LANGUAGES, Colors.PRIMARY),
            darkModeIcon=UiUtils.paintIcon(icons.LANGUAGES, Colors.WHITE),
            parent=self,
        )
        self._addButtonToList(self.languageIcon)
        self._addThemeForItem(self.languageIcon, theme=iconTheme)

        self.languageLabel = LabelWithDefaultText.render(font=itemFont, parent=self)
        self._addThemeForItem(self.languageLabel, itemTextStyle)

        dropdownMenuFormer = DropdownMenu()
        self.changeLanguagueDropdown = dropdownMenuFormer.render()
        self.changeLanguagueDropdown.setFixedHeight(48)
        self.changeLanguagueDropdown.addItems(supportedLanguages)

        dropDownBorder = Border(2, "solid", ColorBoxes.PRIMARY)
        lightModeDropDownBackground = Background(dropDownBorder, borderRadius=8, color=ColorBoxes.WHITE)
        darkModeDropDownBackground = Background(dropDownBorder, borderRadius=8, color=ColorBoxes.BLACK)
        self._addThemeForItem(
            self.changeLanguagueDropdown,
            theme=dropdownMenuFormer.getThemeBuilder()
            .addPadding(Paddings.ABSOLUTE_MEDIUM)
            .addLightModeTextColor(ColorBoxes.BLACK)
            .addDarkModeTextColor(ColorBoxes.WHITE)
            .addLightModeBackground(lightModeDropDownBackground)
            .addLightModeMenuBackground(lightModeDropDownBackground)
            .addDarkModeBackground(darkModeDropDownBackground)
            .addDarkModeMenuBackground(darkModeDropDownBackground)
            .addLightModeItemBackground(Backgrounds.CIRCLE_HIDDEN_PRIMARY_25)
            .addDarkModeItemBackground(Backgrounds.CIRCLE_HIDDEN_WHITE_25)
            .addLightModeMenuTextColor(ColorBox(normal=Colors.BLACK, active=Colors.PRIMARY))
            .addDarkModeMenuTextColor(ColorBoxes.WHITE)
            .build(8),
        )
        self.settingsItemLanguage.addWidget(self.languageIcon)
        self.settingsItemLanguage.addWidget(self.languageLabel)
        self.settingsItemLanguage.addWidget(self.changeLanguagueDropdown, stretch=1)

        # ===================Dark mode===================
        self.darkModeIcon = IconButton.render(
            padding=Paddings.RELATIVE_33,
            size=icons.SIZES.LARGE,
            lightModeIcon=UiUtils.paintIcon(icons.DARKMODE, Colors.PRIMARY),
            darkModeIcon=UiUtils.paintIcon(icons.DARKMODE, Colors.WHITE),
            parent=self,
        )
        self._addButtonToList(self.darkModeIcon)
        self._addThemeForItem(self.darkModeIcon, theme=iconTheme)

        self.darkModeLabel = LabelWithDefaultText.render(font=itemFont, parent=self)
        self._addThemeForItem(self.darkModeLabel, itemTextStyle)

        self.switchDarkModeBtn = Toggle(self)
        self.switchDarkModeBtn.setFixedSize(56, 32)
        self.switchDarkModeBtn.setActiveBackgroundColor(Colors.PRIMARY.toStylesheet())
        self.switchDarkModeBtn.stylize()
        self.switchDarkModeBtn.setAnimationDuration(125)

        self.settingsItemDarkMode.addWidget(self.darkModeIcon)
        self.settingsItemDarkMode.addWidget(self.darkModeLabel)
        self.settingsItemDarkMode.addStretch()
        self.settingsItemDarkMode.addWidget(self.switchDarkModeBtn)

        # ===================Folder===================
        self.folderIcon = IconButton.render(
            padding=Paddings.RELATIVE_50,
            size=icons.SIZES.LARGE,
            lightModeIcon=UiUtils.paintIcon(icons.FOLDER, Colors.PRIMARY),
            darkModeIcon=UiUtils.paintIcon(icons.FOLDER, Colors.WHITE),
            parent=self,
        )
        self._addButtonToList(self.folderIcon)
        self._addThemeForItem(self.folderIcon, theme=iconTheme)

        self.folderLabel = LabelWithDefaultText.render(font=itemFont, parent=self)
        self._addThemeForItem(self.folderLabel, itemTextStyle)

        self.currentFolder = LabelWithDefaultText.render(font=itemFont, parent=self)
        self._addThemeForItem(
            self.currentFolder,
            theme=labelThemBuilder.addPadding(12)
            .addLightModeTextColor(ColorBoxes.BLACK)
            .addDarkModeTextColor(ColorBoxes.WHITE)
            .addLightModeBackground(Backgrounds.ROUNDED_PRIMARY_25)
            .addDarkModeBackground(Backgrounds.ROUNDED_WHITE_25)
            .build(),
        )

        self.changeFolderBtn = IconButton.render(
            padding=Paddings.RELATIVE_75,
            size=icons.SIZES.LARGE,
            lightModeIcon=UiUtils.paintIcon(icons.FORWARD, Colors.PRIMARY),
            darkModeIcon=UiUtils.paintIcon(icons.FORWARD, Colors.WHITE),
            parent=self,
        )
        self._addButtonToList(self.changeFolderBtn)
        self._addThemeForItem(self.changeFolderBtn, theme=buttonWithCheveronTheme)
        self.changeFolderBtn.setCursor(cursors.HAND)

        self.settingsItemFolder.addWidget(self.folderIcon)
        self.settingsItemFolder.addWidget(self.folderLabel)
        self.settingsItemFolder.addWidget(self.currentFolder, stretch=1)
        self.settingsItemFolder.addWidget(self.changeFolderBtn)

    def openFolderChoosingDialogThenSendDataTo(self, controller):
        path = QFileDialog.getExistingDirectory()
        controller.handleChangedFolder(path)

    def connectToController(self, controller):
        self.changeLanguagueDropdown.currentIndexChanged.connect(controller.handleChangedLanguage)
        self.switchDarkModeBtn.valueChanged.connect(controller.handleChangedDarkMode)
        self.changeFolderBtn.clicked.connect(lambda: self.openFolderChoosingDialogThenSendDataTo(controller))

    def translate(self, language: dict[str, str]) -> None:
        self.settingsLabel.setText(language.get("settings"))
        self.languageLabel.setText(language.get("language"))
        supportedLanguagesBySystem: list[str] = language.get("supported_languages")
        for index, supporetLanguage in enumerate(supportedLanguagesBySystem):
            self.changeLanguagueDropdown.setItemText(index, supporetLanguage)
        self.darkModeLabel.setText(language.get("dark_mode"))
        self.folderLabel.setText(language.get("folder"))
        self.currentFolder.setDefaultText(language.get("folder_empty"))

    def changeCurrentFolder(self, dir) -> None:
        self.currentFolder.setText(dir)
