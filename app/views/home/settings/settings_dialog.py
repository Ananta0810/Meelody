from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout

from app.components.base import Label, Factory, ActionButton, DropDown
from app.components.windows import FramelessWindow
from app.helpers.stylesheets import Colors, Paddings
from app.resource.qt import Icons


class SettingsDialog(FramelessWindow):

    def __init__(self):
        super().__init__()
        super()._initComponent()

    def _createUI(self) -> None:
        super()._createUI()

        self.setFixedWidth(480)

        self.setWindowModality(Qt.ApplicationModal)
        self.setClassName("rounded-12 bg-white dark:bg-dark")

        # ==================================== TITLE BAR ====================================
        self._btnClose = Factory.createIconButton(Icons.MEDIUM, Paddings.RELATIVE_50)
        self._btnClose.setLightModeIcon(Icons.CLOSE.withColor(Colors.GRAY))
        self._btnClose.setClassName("bg-none hover:bg-gray-12 rounded-8")

        self._dialogTitle = Label()
        self._dialogTitle.setFont(Factory.createFont(family="Segoe UI Semibold", size=14, bold=True))
        self._dialogTitle.setClassName("text-black dark:text-white bg-none")
        self._dialogTitle.setText("Settings")

        self._titleBar = QHBoxLayout()
        self._titleBar.setContentsMargins(24, 12, 12, 0)

        self._titleBar.addWidget(self._dialogTitle)
        self._titleBar.addStretch(1)
        self._titleBar.addWidget(self._btnClose)

        # ==================================== BODY ====================================
        self._body = QVBoxLayout()
        self._body.setContentsMargins(24, 4, 24, 4)
        self._body.setAlignment(Qt.AlignVCenter)

        self._languageLayout = QHBoxLayout()
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
        self._languageDropdown.addItems(["English", "Vietnamese"])

        self._languageLayout.addLayout(self._languageLeftLayout)
        self._languageLayout.addWidget(self._languageDropdown, alignment=Qt.AlignRight | Qt.AlignCenter)

        self._body.addLayout(self._languageLayout)

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
