from sys import path

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

path.append(".\lib")
from constants.application import supportedLanguages
from constants.ui.qss import Background, ColorBoxes, Colors, Paddings
from constants.ui.qt import AppAlignment, AppCursors, AppIcons
from modules.screens.components.factories import *
from modules.screens.components.font_builder import FontBuilder
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
        aligments = AppAlignment()
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
        self.setObjectName("window_settings_panel")
        # self.setGraphicsEffect(AppEffect.shadow)
        self.main_layout = QVBoxLayout(self)

        self.header = QHBoxLayout()
        self.header.setContentsMargins(16, 8, 16, 8)
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
        self.close_settings_window_btn.clicked.connect(self.hide)
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

        # Change language button
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

        self.change_language_dropdown = QComboBox()
        self.change_language_dropdown.setFixedHeight(48)
        self.change_language_dropdown.setMinimumWidth(160)
        self.change_language_dropdown.addItems(supportedLanguages)

        self.change_language_dropdown.setStyleSheet(
            "QComboBox {"
            + "    padding: 0 12px;"
            + "    color: black;"
            + "    border: 2px solid #8064ea;"
            + "    border-radius: 8px;"
            + "    background-color: white"
            + "}"
            + "QComboBox:hover, QPushButton:hover {"
            + "    border-color: #4032ff"
            + "}"
            + "QComboBox:editable {"
            + "    background-color:transparent;"
            + "    border:none;"
            + "    color: pink;"
            + "}"
            + "QComboBox:!on {"
            + "}"
            + "QComboBox:on {"
            + "}"
            + "QComboBox QAbstractItemView"
            + "{"
            + "    margin-top: 4px;"
            + "    padding: 4px;"
            + "    border-radius: 8px;"
            + "    border: 2px solid #8064ea;"
            + "    background-color: white;"
            + "}"
            + "QComboBox::drop-down {"
            + "    border:none;"
            + "    background-color:transparent;"
            + "    min-width: 32px;"
            + "    color: white"
            + " }"
            + "QComboBox::down-arrow{"
            + "    right: 4px;"
            + "    width: 10px;"
            + "    height: 10px;"
            + "    image: url('assets/images/icons/chevron-down.png');"
            + "}"
            + " /* Menu */"
            + "QComboBox::indicator{"
            + "    background-color:transparent;"
            + "    selection-background-color:transparent;"
            + "    color:transparent;"
            + "    selection-color:transparent;"
            + "}"
            + "QComboBox QAbstractItemView { outline: 0px;}"
            + "QComboBox QAbstractItemView::item{"
            + "    min-height: 32px;"
            + "    padding: 4px;"
            + "    border:none;"
            + "    border-radius: 4px;"
            + "    background-color:transparent;"
            + "    color:black;"
            "}"
            + "QComboBox QAbstractItemView::item:hover{"
            + "    color:rgba(128, 100, 234, 1);"
            + "    border:0px solid transparent;"
            + "    background-color:rgba(128, 100, 234, 0.15);"
            "}"
            + "QComboBox QAbstractItemView::item:focus{"
            + "    color:rgba(128, 100, 234, 1);"
            + "    border:none;"
            + "    background-color:rgba(128, 100, 234, 0.15);"
            + "}"
        )
        self.change_language_dropdown.setItemDelegate(QStyledItemDelegate())
        self.change_language_dropdown.view().window().setWindowFlags(
            Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint
        )
        self.change_language_dropdown.view().window().setAttribute(
            Qt.WA_TranslucentBackground
        )
        self.settings_item_language.addWidget(self.language_icon)
        self.settings_item_language.addWidget(self.language_label)
        self.settings_item_language.addWidget(
            self.change_language_dropdown, stretch=1
        )

        # Change dark mode button
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

        # Change folder button
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

    def connectSignals(self, controller):
        self.change_language_dropdown.currentIndexChanged.connect(
            controller.handleChangedLanguage
        )

    def lightMode(self):
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
        self.current_folder.setText(language.get("folder_empty"))

    def __addThemeForItem(self, item, theme: str):
        self.themeItems[item] = theme

    def __addButtonToList(self, item):
        self.buttonsWithDarkMode.append(item)

    def open(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
        # self.setVisible(not self.isVisible())
