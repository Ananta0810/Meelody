from typing import Optional

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from app.common.others import appCenter, translator
from app.common.statics.enums import ThemeMode
from app.common.statics.qt import Icons, Images, Cursors
from app.common.statics.styles import Colors
from app.common.statics.styles import Paddings
from app.components.animations import Fade
from app.components.base import FontFactory
from app.components.buttons import ButtonFactory, ActionButton
from app.components.dropdowns import DropDown
from app.components.events import ClickObserver
from app.components.images import Cover
from app.components.labels import Label
from app.components.widgets import StyleWidget
from app.components.windows import FramelessWindow
from app.helpers.stylesheets import ClassNameTranslator


class SettingsDialog(FramelessWindow):

    def __init__(self):
        self.__languages: dict = {
            "English": "en",
            "Tiếng Việt": "vi"
        }
        self.__theme: ThemeMode = appCenter.settings.theme

        super().__init__()
        super()._initComponent()

        self.__selectTheme(self.__theme)

        currentLanguageIndex = 0
        for index, language in enumerate(self.__languages.values()):
            if language == appCenter.settings.language:
                currentLanguageIndex = index

        self._languageDropdown.addItems(self.__languages.keys())
        self._languageDropdown.setCurrentIndex(currentLanguageIndex)

    def _createUI(self) -> None:
        super()._createUI()

        self.setWindowModality(Qt.ApplicationModal)
        self.setClassName("rounded-12 bg-white dark:bg-dark")

        # ==================================== TITLE BAR ====================================
        self._closeBtn = ButtonFactory.createIconButton(Icons.medium, Paddings.RELATIVE_50)
        self._closeBtn.setLightModeIcon(Icons.close.withColor(Colors.black))
        self._closeBtn.setDarkModeIcon(Icons.close.withColor(Colors.white))
        self._closeBtn.setClassName("rounded-8 bg-none hover:bg-gray-25 dark:hover:bg-white-20")

        self._dialogTitle = Label()
        self._dialogTitle.setFont(FontFactory.create(family="Segoe UI Semibold", size=14, bold=True))
        self._dialogTitle.setClassName("text-black dark:text-white bg-none")

        self._titleBar = QHBoxLayout()
        self._titleBar.setContentsMargins(24, 12, 12, 0)

        self._titleBar.addWidget(self._dialogTitle)
        self._titleBar.addStretch(1)
        self._titleBar.addWidget(self._closeBtn)

        # ==================================== BODY ====================================
        self._body = QVBoxLayout()
        self._body.setContentsMargins(24, 4, 24, 4)
        self._body.setAlignment(Qt.AlignVCenter)

        self._languageSection = StyleWidget()
        self._languageSection.setClassName("border-b border-gray-25")
        self._languageSection.setContentsMargins(0, 16, 0, 16)

        self._languageLayout = QHBoxLayout(self._languageSection)
        self._languageLayout.setSpacing(8)
        self._languageLayout.setContentsMargins(0, 0, 0, 0)

        self._languageLeftLayout = QVBoxLayout()
        self._languageLeftLayout.setSpacing(0)
        self._languageLeftLayout.setContentsMargins(0, 0, 0, 0)

        self._languageTitleLabel = Label()
        self._languageTitleLabel.setFont(FontFactory.create(family="Segoe UI Semibold", size=11, bold=True))
        self._languageTitleLabel.setClassName("text-black dark:text-white")

        self._languageDescriptionLabel = Label()
        self._languageDescriptionLabel.setFont(FontFactory.create(size=10))
        self._languageDescriptionLabel.setClassName("text-gray")
        self._languageDescriptionLabel.setWordWrap(True)
        self._languageDescriptionLabel.setMinimumWidth(self._languageDescriptionLabel.sizeHint().width())

        self._languageLeftLayout.addWidget(self._languageTitleLabel)
        self._languageLeftLayout.addWidget(self._languageDescriptionLabel)

        self._languageDropdown = DropDown()
        self._languageDropdown.setMinimumWidth(200)
        self._languageDropdown.setClassName(
            "dark:bg-black dark:hover:bg-white-[b12] dark:text-white dark:border dark:border-white-[b33]",
            "dark:dropdown/bg-white-[b12] dark:dropdown/border dark:dropdown/border-white-[b33]",
            "dark:item/hover:bg-white-8 dark:item/text-white"
        )

        self._languageLayout.addLayout(self._languageLeftLayout)
        self._languageLayout.addWidget(self._languageDropdown, alignment=Qt.AlignRight | Qt.AlignCenter)

        self._themeSection = QWidget()
        self._themeSection.setContentsMargins(0, 16, 0, 0)

        self._themeLayout = QVBoxLayout(self._themeSection)
        self._themeLayout.setSpacing(8)
        self._themeLayout.setContentsMargins(0, 0, 0, 0)

        self._themeTitleLabel = Label()
        self._themeTitleLabel.setFont(FontFactory.create(family="Segoe UI Semibold", size=11, bold=True))
        self._themeTitleLabel.setClassName("text-black dark:text-white")

        self._themeDescriptionLabel = Label()
        self._themeDescriptionLabel.setFont(FontFactory.create(size=10))
        self._themeDescriptionLabel.setClassName("text-gray")
        self._themeDescriptionLabel.setWordWrap(True)
        self._themeDescriptionLabel.setMinimumWidth(self._themeDescriptionLabel.sizeHint().width())

        self._themeTypesLayout = QHBoxLayout()
        self._themeTypesLayout.setSpacing(12)
        self._themeTypesLayout.setContentsMargins(0, 0, 0, 0)

        # System Mode
        self._systemModeLayout = QVBoxLayout()
        self._systemModeLayout.setSpacing(4)
        self._systemModeLayout.setContentsMargins(0, 0, 0, 0)

        self._systemModeBtn = ThemeButton()
        self._systemModeBtn.setFixedWidth(160)
        self._systemModeBtn.setCover(Cover.Props.fromBytes(Images.systemMode, width=156, height=90, radius=6))
        self._systemModeBtn.setClassName("rounded-8 border-2 border-transparent active:rounded-8 active:border-2 active:border-primary")

        self._systemModeLabel = Label()
        self._systemModeLabel.setFont(FontFactory.create(family="Segoe UI Semibold", size=10, bold=True))
        self._systemModeLabel.setClassName("text-black dark:text-white")

        self._systemModeLayout.addWidget(self._systemModeBtn)
        self._systemModeLayout.addWidget(self._systemModeLabel)

        # Light Mode
        self._lightModeLayout = QVBoxLayout()
        self._lightModeLayout.setSpacing(4)
        self._lightModeLayout.setContentsMargins(0, 0, 0, 0)

        self._lightModeBtn = ThemeButton()
        self._lightModeBtn.setFixedWidth(160)
        self._lightModeBtn.setCover(Cover.Props.fromBytes(Images.lightMode, width=156, height=90, radius=6))
        self._lightModeBtn.setClassName("rounded-8 border-2 border-transparent active:rounded-8 active:border-2 active:border-primary")

        self._lightModeLabel = Label()
        self._lightModeLabel.setFont(FontFactory.create(family="Segoe UI Semibold", size=10, bold=True))
        self._lightModeLabel.setClassName("text-black dark:text-white")

        self._lightModeLayout.addWidget(self._lightModeBtn)
        self._lightModeLayout.addWidget(self._lightModeLabel)

        # Dark Mode
        self._darkModeLayout = QVBoxLayout()
        self._darkModeLayout.setSpacing(4)
        self._darkModeLayout.setContentsMargins(0, 0, 0, 0)

        self._darkModeBtn = ThemeButton()
        self._darkModeBtn.setFixedWidth(160)
        self._darkModeBtn.setCover(Cover.Props.fromBytes(Images.darkMode, width=156, height=90, radius=6))
        self._darkModeBtn.setClassName("rounded-8 border-2 border-transparent active:rounded-8 active:border-2 active:border-primary")

        self._darkModeLabel = Label()
        self._darkModeLabel.setFont(FontFactory.create(family="Segoe UI Semibold", size=10, bold=True))
        self._darkModeLabel.setClassName("text-black dark:text-white")

        self._darkModeLayout.addWidget(self._darkModeBtn)
        self._darkModeLayout.addWidget(self._darkModeLabel)

        self._themeLayout.addWidget(self._themeTitleLabel)
        self._themeLayout.addWidget(self._themeDescriptionLabel)
        self._themeLayout.addLayout(self._themeTypesLayout)

        self._themeTypesLayout.addLayout(self._systemModeLayout)
        self._themeTypesLayout.addLayout(self._lightModeLayout)
        self._themeTypesLayout.addLayout(self._darkModeLayout)

        self._body.addWidget(self._languageSection)
        self._body.addWidget(self._themeSection)

        # ==================================== FOOTER ====================================
        self._footer = StyleWidget()
        self._footer.setClassName("border-t border-gray-25")

        self._footerLayout = QHBoxLayout(self._footer)
        self._footerLayout.setSpacing(12)
        self._footerLayout.setContentsMargins(24, 12, 24, 12)

        self._cancelBtn = ActionButton()
        self._cancelBtn.setFont(FontFactory.create(family="Segoe UI Semibold", size=10))
        self._cancelBtn.setClassName(
            "rounded-4 text-black bg-gray-12 hover:bg-gray-25 py-8 px-24",
            "dark:text-white dark:bg-white-20 dark:hover:bg-white-33"
        )

        self._saveBtn = ActionButton()
        self._saveBtn.setFont(FontFactory.create(family="Segoe UI Semibold", size=10))
        self._saveBtn.setClassName("rounded-4 text-white bg-primary-75 bg-primary py-8 px-24")

        self._footerLayout.addStretch(1)
        self._footerLayout.addWidget(self._cancelBtn)
        self._footerLayout.addWidget(self._saveBtn)

        super().addLayout(self._titleBar)
        super().addSpacing(12)
        super().addLayout(self._body)
        super().addSpacing(8)
        super().addWidget(self._footer)

        self._animation = Fade(self)

    def _translateUI(self) -> None:
        self._dialogTitle.setText(translator.translate("SETTINGS.LABEL"))
        self._languageTitleLabel.setText(translator.translate("SETTINGS.LANGUAGE_LABEL"))
        self._languageDescriptionLabel.setText(translator.translate("SETTINGS.LANGUAGE_DESCRIPTION"))
        self._themeTitleLabel.setText(translator.translate("SETTINGS.THEME_LABEL"))
        self._themeDescriptionLabel.setText(translator.translate("SETTINGS.THEME_DESCRIPTION"))
        self._systemModeLabel.setText(translator.translate("SETTINGS.SYSTEM_MODE"))
        self._lightModeLabel.setText(translator.translate("SETTINGS.LIGHT_MODE"))
        self._darkModeLabel.setText(translator.translate("SETTINGS.DARK_MODE"))
        self._cancelBtn.setText(translator.translate("SETTINGS.CANCEL_BTN"))
        self._saveBtn.setText(translator.translate("SETTINGS.SAVE_BTN"))

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()

        self._systemModeBtn.selected.connect(lambda: self.__selectTheme(ThemeMode.SYSTEM))
        self._lightModeBtn.selected.connect(lambda: self.__selectTheme(ThemeMode.LIGHT))
        self._darkModeBtn.selected.connect(lambda: self.__selectTheme(ThemeMode.DARK))

        self._closeBtn.clicked.connect(lambda: self.closeWithAnimation())
        self._cancelBtn.clicked.connect(lambda: self.closeWithAnimation())
        self._saveBtn.clicked.connect(lambda: self.__saveChanges())

    def __selectTheme(self, theme: ThemeMode) -> None:
        self.__theme = theme

        self._systemModeBtn.setActive(theme == ThemeMode.SYSTEM)
        self._lightModeBtn.setActive(theme == ThemeMode.LIGHT)
        self._darkModeBtn.setActive(theme == ThemeMode.DARK)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)

    def applyLightMode(self) -> None:
        super().applyLightMode()
        super().applyThemeToChildren()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        super().applyThemeToChildren()

    def show(self) -> None:
        self._translateUI()
        self.applyTheme()
        self.moveToCenter()
        self.setWindowOpacity(0)
        super().show()
        self._animation.fadeIn()

    def closeWithAnimation(self) -> None:
        self._animation.fadeOut(onFinished=lambda: self.close())

    def __saveChanges(self) -> None:
        self._saveBtn.setCursor(Cursors.waiting)

        appCenter.setTheme(self.__theme)

        lang = self.__languages[self._languageDropdown.currentText()]
        appCenter.settings.setLanguage(lang)
        translator.setLanguage(lang)

        self._saveBtn.setCursor(Cursors.pointer)
        self.closeWithAnimation()


class ThemeButton(Cover):
    selected = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setCursor(Cursors.pointer)
        self.__normalState = None
        self.__activeState = None

        ClickObserver(self).clicked.connect(lambda: self.selected.emit())

    def setActive(self, active: bool) -> None:
        if active:
            self.setStyleSheet(self.__activeState)
        else:
            self.setStyleSheet(self.__normalState)

    def setClassName(self, className: str) -> None:
        theme, _ = ClassNameTranslator.translateElements(className, self)
        self.__normalState = theme.getElement().state().toProps()
        self.__activeState = theme.getElement().state("active").toProps()
