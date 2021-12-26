from typing import Optional

from constants.application import supportedLanguages
from constants.ui.qss import Backgrounds, ColorBoxes, Colors, Paddings
from constants.ui.qt import AppCursors, AppIcons
from modules.screens.components.dropdowns import DropdownMenu
from modules.screens.components.font_builder import FontBuilder
from modules.screens.components.icon_buttons import IconButton
from modules.screens.components.labels import StandardLabel
from modules.screens.qss.qss_elements import Background, Border, ColorBox
from modules.screens.themes.theme_builders import ButtonThemeBuilder, LabelThemeBuilder
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QVBoxLayout, QWidget
from utils.ui.application_utils import UiUtils
from widgets.toggle import Toggle

from views.view import View


class SettingsPanel(QWidget, View):
    def __init__(self, parent: Optional["QWidget"] = None):
        super(SettingsPanel, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        iconButtonThemeBuilder = ButtonThemeBuilder()
        icons = AppIcons()
        cursors = AppCursors()
        fontBuilder = FontBuilder()
        labelThemeBuilder = LabelThemeBuilder()

        # Template
        iconTheme = (
            iconButtonThemeBuilder.addLightModeBackground(Backgrounds.CIRCLE_PRIMARY_25)
            .addDarkModeBackground(Backgrounds.CIRCLE_WHITE_25)
            .build(itemSize=48)
        )
        buttonTheme = (
            iconButtonThemeBuilder.addLightModeBackground(Backgrounds.ROUNDED_PRIMARY_25)
            .addDarkModeBackground(Backgrounds.ROUNDED_WHITE_25)
            .build(itemSize=48)
        )
        itemFont = fontBuilder.withSize(9).build()
        itemTextStyle = (
            labelThemeBuilder.addLightModeTextColor(ColorBoxes.BLACK).addDarkModeTextColor(ColorBoxes.WHITE).build()
        )

        # UI
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAutoFillBackground(True)
        self.main_layout = QVBoxLayout(self)

        self.header = QHBoxLayout()
        self.header.setContentsMargins(8, 8, 8, 8)
        self.body = QVBoxLayout()
        self.body.setContentsMargins(48, 8, 48, 8)
        self.body.setSpacing(16)
        self.main_layout.addLayout(self.header)
        self.main_layout.addLayout(self.body, stretch=3)
        self.main_layout.addStretch()

        self.close_settings_window_btn = IconButton.render(
            padding=Paddings.RELATIVE_75,
            size=icons.SIZES.LARGE,
            lightModeIcon=UiUtils.paintIcon(icons.BACKWARD, Colors.PRIMARY),
            darkModeIcon=UiUtils.paintIcon(icons.BACKWARD, Colors.WHITE),
        )
        self._addThemeForItem(
            self.close_settings_window_btn,
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
                .build(self.close_settings_window_btn.height())
            ),
        )
        self._addButtonToList(self.close_settings_window_btn)
        self.close_settings_window_btn.setCursor(cursors.HAND)
        self.header.addWidget(self.close_settings_window_btn)
        self.header.addStretch()

        self.settings_label = StandardLabel.render(fontBuilder.withSize(24).withWeight("bold").build())
        self._addThemeForItem(self.settings_label, itemTextStyle)
        self.body.addWidget(self.settings_label)

        self.settings_items = QVBoxLayout()
        self.body.addLayout(self.settings_items, stretch=1)
        self.settings_item_language = QHBoxLayout()
        self.settings_item_language.setSpacing(8)
        self.settings_item_dark_mode = QHBoxLayout()
        self.settings_item_dark_mode.setSpacing(8)
        self.settings_item_folder = QHBoxLayout()
        self.settings_item_folder.setSpacing(8)
        self.settings_items.addLayout(self.settings_item_language)
        self.settings_items.addLayout(self.settings_item_dark_mode)
        self.settings_items.addLayout(self.settings_item_folder)

        # ===================Langauges===================
        self.language_icon = IconButton.render(
            padding=Paddings.RELATIVE_50,
            size=icons.SIZES.LARGE,
            lightModeIcon=UiUtils.paintIcon(icons.LANGUAGES, Colors.PRIMARY),
            darkModeIcon=UiUtils.paintIcon(icons.LANGUAGES, Colors.WHITE),
            parent=self,
        )
        self._addButtonToList(self.language_icon)
        self._addThemeForItem(self.language_icon, theme=iconTheme)

        self.language_label = StandardLabel.render(font=itemFont, parent=self)
        self._addThemeForItem(self.language_label, itemTextStyle)

        dropdownMenuFormer = DropdownMenu()
        self.change_language_dropdown = dropdownMenuFormer.render()
        self.change_language_dropdown.setFixedHeight(48)
        self.change_language_dropdown.addItems(supportedLanguages)

        dropDownBorder = Border(2, "solid", ColorBoxes.PRIMARY)
        lightModeDropDownBackground = Background(dropDownBorder, borderRadius=8, color=ColorBoxes.WHITE)
        darkModeDropDownBackground = Background(dropDownBorder, borderRadius=8, color=ColorBoxes.BLACK)
        self._addThemeForItem(
            self.change_language_dropdown,
            theme=(
                dropdownMenuFormer.getThemeBuilder()
                .addPadding(Paddings.ABSOLUTE_MEDIUM)
                .addLightModeTextColor(ColorBoxes.BLACK)
                .addDarkModeTextColor(ColorBoxes.WHITE)
                .addLightModeBackground(lightModeDropDownBackground)
                .addLightModeMenuBackground(lightModeDropDownBackground)
                .addDarkModeBackground(darkModeDropDownBackground)
                .addDarkModeMenuBackground(darkModeDropDownBackground)
                .addLightModeItemBackground(
                    Background(
                        borderRadius=4,
                        color=ColorBoxes.HOVERABLE_HIDDEN_PRIMARY,
                    )
                )
                .addDarkModeItemBackground(
                    Background(
                        borderRadius=4,
                        color=ColorBoxes.HOVERABLE_HIDDEN_WHITE,
                    )
                )
                .addLightModeMenuTextColor(
                    ColorBox(
                        normal=Colors.BLACK,
                        active=Colors.PRIMARY,
                    )
                )
                .addDarkModeMenuTextColor(ColorBoxes.WHITE)
                .build()
            ),
        )
        self.settings_item_language.addWidget(self.language_icon)
        self.settings_item_language.addWidget(self.language_label)
        self.settings_item_language.addWidget(self.change_language_dropdown, stretch=1)

        # ===================Dark mode===================
        self.dark_mode_icon = IconButton.render(
            padding=Paddings.RELATIVE_33,
            size=icons.SIZES.LARGE,
            lightModeIcon=UiUtils.paintIcon(icons.DARKMODE, Colors.PRIMARY),
            darkModeIcon=UiUtils.paintIcon(icons.DARKMODE, Colors.WHITE),
            parent=self,
        )
        self._addButtonToList(self.dark_mode_icon)
        self._addThemeForItem(self.dark_mode_icon, theme=iconTheme)

        self.dark_mode_label = StandardLabel.render(font=itemFont, parent=self)
        self._addThemeForItem(self.dark_mode_label, itemTextStyle)

        self.switch_dark_mode_btn = Toggle(self)
        self.switch_dark_mode_btn.setFixedSize(56, 32)
        self.switch_dark_mode_btn.setActiveBackgroundColor(Colors.PRIMARY.toStylesheet())
        self.switch_dark_mode_btn.stylize()
        self.switch_dark_mode_btn.setAnimationDuration(125)

        self.settings_item_dark_mode.addWidget(self.dark_mode_icon)
        self.settings_item_dark_mode.addWidget(self.dark_mode_label)
        self.settings_item_dark_mode.addStretch()
        self.settings_item_dark_mode.addWidget(self.switch_dark_mode_btn)

        # ===================Folder===================
        self.folder_icon = IconButton.render(
            padding=Paddings.RELATIVE_50,
            size=icons.SIZES.LARGE,
            lightModeIcon=UiUtils.paintIcon(icons.FOLDER, Colors.PRIMARY),
            darkModeIcon=UiUtils.paintIcon(icons.FOLDER, Colors.WHITE),
            parent=self,
        )
        self._addButtonToList(self.folder_icon)
        self._addThemeForItem(self.folder_icon, theme=iconTheme)

        self.folder_label = StandardLabel.render(font=itemFont, parent=self)
        self._addThemeForItem(self.folder_label, itemTextStyle)

        self.current_folder = StandardLabel.render(font=itemFont, parent=self)
        self._addThemeForItem(
            self.current_folder,
            theme=(
                labelThemeBuilder.addPadding(12)
                .addLightModeTextColor(ColorBoxes.BLACK)
                .addDarkModeTextColor(ColorBoxes.WHITE)
                .addLightModeBackground(
                    Background(
                        borderRadius=12,
                        color=ColorBoxes.HOVERABLE_PRIMARY_25,
                    )
                )
                .addDarkModeBackground(
                    Background(
                        borderRadius=12,
                        color=ColorBoxes.HOVERABLE_WHITE_25,
                    )
                )
                .build()
            ),
        )

        self.change_folder_btn = IconButton.render(
            padding=Paddings.RELATIVE_75,
            size=icons.SIZES.LARGE,
            lightModeIcon=UiUtils.paintIcon(icons.FORWARD, Colors.PRIMARY),
            darkModeIcon=UiUtils.paintIcon(icons.FORWARD, Colors.WHITE),
            parent=self,
        )
        self._addButtonToList(self.change_folder_btn)
        self._addThemeForItem(self.change_folder_btn, theme=buttonTheme)
        self.change_folder_btn.setCursor(cursors.HAND)

        self.settings_item_folder.addWidget(self.folder_icon)
        self.settings_item_folder.addWidget(self.folder_label)
        self.settings_item_folder.addWidget(self.current_folder, stretch=1)
        self.settings_item_folder.addWidget(self.change_folder_btn)

    def openFolderChoosingDialogThenSendDataTo(self, controller):
        path = QFileDialog.getExistingDirectory()
        controller.handleChangedFolder(path)

    def connectSignalsToController(self, controller):
        self.change_language_dropdown.currentIndexChanged.connect(controller.handleChangedLanguage)
        self.switch_dark_mode_btn.valueChanged.connect(controller.handleChangedDarkMode)
        self.change_folder_btn.clicked.connect(lambda: self.openFolderChoosingDialogThenSendDataTo(controller))

    def translate(self, language: dict[str, str]) -> None:
        self.settings_label.setText(language.get("settings"))
        self.language_label.setText(language.get("language"))
        supportedLanguagesBySystem: list[str] = language.get("supported_languages")
        for index, supporetLanguage in enumerate(supportedLanguagesBySystem):
            self.change_language_dropdown.setItemText(index, supporetLanguage)
        self.dark_mode_label.setText(language.get("dark_mode"))
        self.folder_label.setText(language.get("folder"))
        self.current_folder.setDefaultText(language.get("folder_empty"))

    def changeCurrentFolder(self, dir) -> None:
        self.current_folder.setText(dir)
