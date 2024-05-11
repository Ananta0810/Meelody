from typing import Optional

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from app.common.models import ThemeMode
from app.common.others import appCenter
from app.components.base import Label, Factory, ActionButton, DropDown, Cover, CoverProps
from app.components.events import ClickObserver
from app.components.widgets import StyleWidget
from app.components.windows import FramelessWindow
from app.helpers.stylesheets import Colors, Paddings
from app.helpers.stylesheets.translators import ClassNameTranslator
from app.resource.qt import Icons, Images, Cursors


class SettingsDialog(FramelessWindow):

    def __init__(self):
        super().__init__()
        super()._initComponent()

        self.__theme: ThemeMode = ThemeMode.SYSTEM
        self.__selectTheme(ThemeMode.SYSTEM)

    def _createUI(self) -> None:
        super()._createUI()

        self.setWindowModality(Qt.ApplicationModal)
        self.setClassName("rounded-12 bg-white dark:bg-dark")

        # ==================================== TITLE BAR ====================================
        self._closeBtn = Factory.createIconButton(Icons.MEDIUM, Paddings.RELATIVE_50)
        self._closeBtn.setLightModeIcon(Icons.CLOSE.withColor(Colors.GRAY))
        self._closeBtn.setClassName("bg-none hover:bg-gray-12 rounded-8")

        self._dialogTitle = Label()
        self._dialogTitle.setFont(Factory.createFont(family="Segoe UI Semibold", size=14, bold=True))
        self._dialogTitle.setClassName("text-black dark:text-white bg-none")
        self._dialogTitle.setText("Settings")

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
        self._languageTitleLabel.setFont(Factory.createFont(family="Segoe UI Semibold", size=11, bold=True))
        self._languageTitleLabel.setClassName("text-black dark:text-white")
        self._languageTitleLabel.setText("Language")

        self._languageDescriptionLabel = Label()
        self._languageDescriptionLabel.setFont(Factory.createFont(size=10))
        self._languageDescriptionLabel.setClassName("text-gray")
        self._languageDescriptionLabel.setText("Select language of the application")
        self._languageDescriptionLabel.setWordWrap(True)
        self._languageDescriptionLabel.setMinimumWidth(self._languageDescriptionLabel.sizeHint().width())

        self._languageLeftLayout.addWidget(self._languageTitleLabel)
        self._languageLeftLayout.addWidget(self._languageDescriptionLabel)

        self._languageDropdown = DropDown()
        self._languageDropdown.setMinimumWidth(200)
        self._languageDropdown.addItems(["English", "Vietnamese"])

        self._languageLayout.addLayout(self._languageLeftLayout)
        self._languageLayout.addWidget(self._languageDropdown, alignment=Qt.AlignRight | Qt.AlignCenter)

        self._themeSection = StyleWidget()
        self._themeSection.setClassName("border-b border-gray-25")
        self._themeSection.setContentsMargins(0, 16, 0, 16)

        self._themeLayout = QVBoxLayout(self._themeSection)
        self._themeLayout.setSpacing(8)
        self._themeLayout.setContentsMargins(0, 0, 0, 0)

        self._themeTitleLabel = Label()
        self._themeTitleLabel.setFont(Factory.createFont(family="Segoe UI Semibold", size=11, bold=True))
        self._themeTitleLabel.setClassName("text-black dark:text-white")
        self._themeTitleLabel.setText("Theme")

        self._themeDescriptionLabel = Label()
        self._themeDescriptionLabel.setFont(Factory.createFont(size=10))
        self._themeDescriptionLabel.setClassName("text-gray")
        self._themeDescriptionLabel.setText("Select your application theme")
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
        self._systemModeBtn.setDefaultCover(CoverProps.fromBytes(Images.SYSTEM_MODE, width=156, height=90, radius=6))
        self._systemModeBtn.setClassName("rounded-8 border-2 border-transparent active:rounded-8 active:border-2 active:border-primary")

        self._systemModeLabel = Label()
        self._systemModeLabel.setFont(Factory.createFont(family="Segoe UI Semibold", size=10, bold=True))
        self._systemModeLabel.setClassName("text-black dark:text-white")
        self._systemModeLabel.setText("System")

        self._systemModeLayout.addWidget(self._systemModeBtn)
        self._systemModeLayout.addWidget(self._systemModeLabel)

        # Light Mode
        self._lightModeLayout = QVBoxLayout()
        self._lightModeLayout.setSpacing(4)
        self._lightModeLayout.setContentsMargins(0, 0, 0, 0)

        self._lightModeBtn = ThemeButton()
        self._lightModeBtn.setFixedWidth(160)
        self._lightModeBtn.setDefaultCover(CoverProps.fromBytes(Images.LIGHT_MODE, width=156, height=90, radius=6))
        self._lightModeBtn.setClassName("rounded-8 border-2 border-transparent active:rounded-8 active:border-2 active:border-primary")

        self._lightModeLabel = Label()
        self._lightModeLabel.setFont(Factory.createFont(family="Segoe UI Semibold", size=10, bold=True))
        self._lightModeLabel.setClassName("text-black dark:text-white")
        self._lightModeLabel.setText("Light Mode")

        self._lightModeLayout.addWidget(self._lightModeBtn)
        self._lightModeLayout.addWidget(self._lightModeLabel)

        # Dark Mode
        self._darkModeLayout = QVBoxLayout()
        self._darkModeLayout.setSpacing(4)
        self._darkModeLayout.setContentsMargins(0, 0, 0, 0)

        self._darkModeBtn = ThemeButton()
        self._darkModeBtn.setFixedWidth(160)
        self._darkModeBtn.setDefaultCover(CoverProps.fromBytes(Images.DARK_MODE, width=156, height=90, radius=6))
        self._darkModeBtn.setClassName("rounded-8 border-2 border-transparent active:rounded-8 active:border-2 active:border-primary")

        self._darkModeLabel = Label()
        self._darkModeLabel.setFont(Factory.createFont(family="Segoe UI Semibold", size=10, bold=True))
        self._darkModeLabel.setClassName("text-black dark:text-white")
        self._darkModeLabel.setText("Dark Mode")

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
        self._footer = QHBoxLayout()
        self._footer.setSpacing(12)
        self._footer.setContentsMargins(24, 0, 24, 12)

        self._cancelBtn = ActionButton()
        self._cancelBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=10))
        self._cancelBtn.setClassName("rounded-4 text-black bg-gray-12 hover:bg-gray-25 py-8 px-24")
        self._cancelBtn.setText("Cancel")

        self._saveBtn = ActionButton()
        self._saveBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=10))
        self._saveBtn.setClassName("rounded-4 text-white bg-primary-75 bg-primary py-8 px-24")
        self._saveBtn.setText("Save")

        self._footer.addStretch(1)
        self._footer.addWidget(self._cancelBtn)
        self._footer.addWidget(self._saveBtn)

        super().addLayout(self._titleBar)
        super().addSpacing(12)
        super().addLayout(self._body)
        super().addSpacing(8)
        super().addLayout(self._footer)

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()

        self._systemModeBtn.selected.connect(lambda: self.__selectTheme(ThemeMode.SYSTEM))
        self._lightModeBtn.selected.connect(lambda: self.__selectTheme(ThemeMode.LIGHT))
        self._darkModeBtn.selected.connect(lambda: self.__selectTheme(ThemeMode.DARK))

        self._closeBtn.clicked.connect(lambda: self.close())
        self._cancelBtn.clicked.connect(lambda: self.close())
        self._saveBtn.clicked.connect(lambda: self.__saveChanges())

    def __selectTheme(self, theme: ThemeMode) -> None:
        self.__theme = theme

        self._systemModeBtn.setActive(theme == ThemeMode.SYSTEM)
        self._lightModeBtn.setActive(theme == ThemeMode.LIGHT)
        self._darkModeBtn.setActive(theme == ThemeMode.DARK)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.moveToCenter()

    def applyLightMode(self) -> None:
        super().applyLightMode()
        super().applyThemeToChildren()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        super().applyThemeToChildren()

    def show(self) -> None:
        self.applyTheme()
        self.moveToCenter()
        super().show()

    def __saveChanges(self) -> None:
        self._saveBtn.setCursor(Cursors.WAITING)
        appCenter.setTheme(self.__theme)
        self._saveBtn.setCursor(Cursors.HAND)


class ThemeButton(Cover):
    selected = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setCursor(Cursors.HAND)
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
