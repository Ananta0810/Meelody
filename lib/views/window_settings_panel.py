from constants.application import supportedLanguages
from constants.ui.qss import ColorBoxes, Colors, Paddings
from constants.ui.qt import AppCursors, AppIcons
from modules.screens.components.dropdowns import DropdownMenu
from modules.screens.components.factories import IconButtonFactory, LabelFactory
from modules.screens.components.font_builder import FontBuilder
from modules.screens.qss.qss_elements import Background, Border, ColorBox
from modules.screens.themes.theme_builders import ThemeData
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QVBoxLayout, QWidget
from utils.ui.application_utils import ApplicationUIUtils as AppUI
from widgets.toggle import Toggle


class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.themeItems = {}
        self.buttonsWithDarkMode = []
        # Declaration
        buttonFactory = IconButtonFactory()
        iconButtonFormer = buttonFactory.getByType("default")
        iconButtonThemeBuilder = iconButtonFormer.getThemeBuilder()
        icons = AppIcons()
        cursors = AppCursors()
        fontBuilder = FontBuilder()
        labelFormer = LabelFactory().getByType("default")
        labelThemeBuilder = labelFormer.getThemeBuilder()

        # Template
        iconTheme = (
            iconButtonThemeBuilder.addLightModeBackground(
                Background(
                    borderRadius=0.5,
                    color=ColorBoxes.PRIMARY_LIGHTEN_25,
                )
            )
            .addDarkModeBackground(
                Background(
                    borderRadius=0.5,
                    color=ColorBoxes.WHITE_LIGHTEN_25,
                )
            )
            .build(itemSize=48)
        )
        buttonTheme = (
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
            .build(itemSize=48)
        )
        itemFont = fontBuilder.withSize(9).build()
        itemTextStyle = (
            labelThemeBuilder.addLightModeTextColor(ColorBoxes.BLACK)
            .addDarkModeTextColor(ColorBoxes.WHITE)
            .build()
        )
        lightForwardBtn = AppUI.paintIcon(icons.FORWARD, Colors.PRIMARY)
        darkForwardBtn = AppUI.paintIcon(icons.FORWARD, Colors.WHITE)

        # UI
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

        self.close_settings_window_btn = iconButtonFormer.render(
            padding=Paddings.RELATIVE_75,
            size=icons.SIZES.LARGE,
            lightModeIcon=AppUI.paintIcon(icons.BACKWARD, Colors.PRIMARY),
            darkModeIcon=AppUI.paintIcon(icons.BACKWARD, Colors.WHITE),
        )
        self.__addThemeForItem(
            self.close_settings_window_btn,
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
                .build(self.close_settings_window_btn.height())
            ),
        )
        self.__addButtonToList(self.close_settings_window_btn)
        self.close_settings_window_btn.setCursor(cursors.HAND)
        self.header.addWidget(self.close_settings_window_btn)
        self.header.addStretch()

        self.settings_label = labelFormer.render(
            fontBuilder.withSize(24).withWeight("bold").build()
        )
        self.settings_label.setFixedWidth(200)
        self.__addThemeForItem(self.settings_label, itemTextStyle)
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
        self.language_icon = iconButtonFormer.render(
            padding=Paddings.RELATIVE_50,
            size=icons.SIZES.LARGE,
            lightModeIcon=AppUI.paintIcon(icons.LANGUAGES, Colors.PRIMARY),
            darkModeIcon=AppUI.paintIcon(icons.LANGUAGES, Colors.WHITE),
            parent=self,
        )
        self.__addButtonToList(self.language_icon)
        self.__addThemeForItem(self.language_icon, theme=iconTheme)

        self.language_label = labelFormer.render(font=itemFont, parent=self)
        self.__addThemeForItem(self.language_label, itemTextStyle)

        dropdownMenuFormer = DropdownMenu()
        self.change_language_dropdown = dropdownMenuFormer.render()
        self.change_language_dropdown.setFixedHeight(48)
        self.change_language_dropdown.addItems(supportedLanguages)

        dropDownBorder = Border(2, "solid", ColorBoxes.PRIMARY)
        lightModeDropDownBackground = Background(
            dropDownBorder, borderRadius=8, color=ColorBoxes.WHITE
        )
        darkModeDropDownBackground = Background(
            dropDownBorder, borderRadius=8, color=ColorBoxes.BLACK
        )
        self.__addThemeForItem(
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
                        color=ColorBoxes.HIDDEN_PRIMARY,
                    )
                )
                .addDarkModeItemBackground(
                    Background(
                        borderRadius=4,
                        color=ColorBoxes.HIDDEN_WHITE,
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
        self.settings_item_language.addWidget(
            self.change_language_dropdown, stretch=1
        )

        # ===================Dark mode===================
        self.dark_mode_icon = iconButtonFormer.render(
            padding=Paddings.RELATIVE_33,
            size=icons.SIZES.LARGE,
            lightModeIcon=AppUI.paintIcon(icons.DARKMODE, Colors.PRIMARY),
            darkModeIcon=AppUI.paintIcon(icons.DARKMODE, Colors.WHITE),
            parent=self,
        )
        self.__addButtonToList(self.dark_mode_icon)
        self.__addThemeForItem(self.dark_mode_icon, theme=iconTheme)

        self.dark_mode_label = labelFormer.render(font=itemFont, parent=self)
        self.__addThemeForItem(self.dark_mode_label, itemTextStyle)

        self.switch_dark_mode_btn = Toggle(self)
        self.switch_dark_mode_btn.stylize(
            activeBackColor=Colors.PRIMARY.toStylesheet()
        )
        self.switch_dark_mode_btn.setCheckable(True)

        self.settings_item_dark_mode.addWidget(self.dark_mode_icon)
        self.settings_item_dark_mode.addWidget(self.dark_mode_label)
        self.settings_item_dark_mode.addStretch()
        self.settings_item_dark_mode.addWidget(self.switch_dark_mode_btn)

        # ===================Folder===================
        self.folder_icon = iconButtonFormer.render(
            padding=Paddings.RELATIVE_50,
            size=icons.SIZES.LARGE,
            lightModeIcon=AppUI.paintIcon(icons.FOLDER, Colors.PRIMARY),
            darkModeIcon=AppUI.paintIcon(icons.FOLDER, Colors.WHITE),
            parent=self,
        )
        self.__addButtonToList(self.folder_icon)
        self.__addThemeForItem(self.folder_icon, theme=iconTheme)

        self.folder_label = labelFormer.render(font=itemFont, parent=self)
        self.__addThemeForItem(self.folder_label, itemTextStyle)

        self.current_folder = labelFormer.render(font=itemFont, parent=self)
        self.__addThemeForItem(
            self.current_folder,
            theme=(
                labelThemeBuilder.addPadding(12)
                .addLightModeTextColor(ColorBoxes.BLACK)
                .addDarkModeTextColor(ColorBoxes.WHITE)
                .addLightModeBackground(
                    Background(
                        borderRadius=12,
                        color=ColorBoxes.PRIMARY_LIGHTEN_HOVERABLE_25,
                    )
                )
                .addDarkModeBackground(
                    Background(
                        borderRadius=12,
                        color=ColorBoxes.WHITE_LIGHTEN_HOVERABLE_25,
                    )
                )
                .build()
            ),
        )

        self.change_folder_btn = iconButtonFormer.render(
            padding=Paddings.RELATIVE_75,
            size=icons.SIZES.LARGE,
            lightModeIcon=lightForwardBtn,
            darkModeIcon=darkForwardBtn,
            parent=self,
        )
        self.__addButtonToList(self.change_folder_btn)
        self.__addThemeForItem(self.change_folder_btn, theme=buttonTheme)
        self.change_folder_btn.setCursor(cursors.HAND)

        self.settings_item_folder.addWidget(self.folder_icon)
        self.settings_item_folder.addWidget(self.folder_label)
        self.settings_item_folder.addWidget(self.current_folder, stretch=1)
        self.settings_item_folder.addWidget(self.change_folder_btn)

    def openFolderChoosingDialogThenSendDataTo(self, controller):
        path = QFileDialog.getExistingDirectory()
        controller.handleChangedFolder(path)

    def connectSignalsToController(self, controller):
        self.change_language_dropdown.currentIndexChanged.connect(
            controller.handleChangedLanguage
        )
        self.switch_dark_mode_btn.clicked.connect(
            controller.handleChangedDarkMode
        )
        self.change_folder_btn.clicked.connect(
            lambda: self.openFolderChoosingDialogThenSendDataTo(controller)
        )

    def lightMode(self):
        # Due to some error, the light mode will not work properly the first time
        # Therefore, we need to take a warm settup before apply dark-light mode
        self.change_language_dropdown.setStyleSheet(
            self.themeItems.get(self.change_language_dropdown).lightMode
        )
        self.setStyleSheet("background:white;border-radius:16px")
        for item in self.themeItems:
            lightModeStyleSheet = self.themeItems.get(item).lightMode
            if lightModeStyleSheet is None or lightModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(lightModeStyleSheet)

        for button in self.buttonsWithDarkMode:
            button.setDarkMode(False)

    def darkMode(self):
        self.setStyleSheet("background:black;border-radius:16px")
        self.change_language_dropdown.setStyleSheet(
            self.themeItems.get(self.change_language_dropdown).darkMode
        )
        for item in self.themeItems:
            darkModeStyleSheet = self.themeItems.get(item).darkMode
            if darkModeStyleSheet is None or darkModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(darkModeStyleSheet)
        for button in self.buttonsWithDarkMode:
            button.setDarkMode(True)

    def translate(self, language: dict) -> None:
        self.settings_label.setText(language.get("settings"))
        self.language_label.setText(language.get("language"))
        supportedLanguagesBySystem: list[str] = language.get(
            "supported_languages"
        )
        for index, supporetLanguage in enumerate(supportedLanguagesBySystem):
            self.change_language_dropdown.setItemText(index, supporetLanguage)
        self.dark_mode_label.setText(language.get("dark_mode"))
        self.folder_label.setText(language.get("folder"))
        self.current_folder.setDefaultText(language.get("folder_empty"))

    def __addThemeForItem(self, item, theme: ThemeData) -> None:
        self.themeItems[item] = theme

    def __addButtonToList(self, item) -> None:
        self.buttonsWithDarkMode.append(item)

    def changeCurrentFolder(self, dir) -> None:
        self.current_folder.setText(dir)
