from PyQt5.QtWidgets import QWidget

from app.components.base import Label, Factory, ActionButton
from app.components.dialogs import BaseDialog
from app.components.widgets import FlexBox


class SettingsDialog(BaseDialog):

    def __init__(self):
        super().__init__()
        super()._initComponent()

    def _createUI(self) -> None:
        super()._createUI()
        self.setFixedWidth(480)

        # ==================================== TITLE BAR ====================================
        self._dialogTitle = Label()
        self._dialogTitle.setFont(Factory.createFont(size=13, bold=True))
        self._dialogTitle.setClassName("text-black dark:text-white bg-none")
        self._dialogTitle.setText("Settings")

        self._titleBarLayout.setContentsMargins(24, 12, 12, 0)
        self._titleBarLayout.insertWidget(0, self._dialogTitle)

        self._btnClose.setClassName("bg-none hover:bg-gray-12 rounded-8")

        # ==================================== BODY ====================================
        self._body.setContentsMargins(0, 0, 0, 0)

        # ==================================== FOOTER ====================================
        self._footer = QWidget()
        self._body.addWidget(self._footer)

        self._footerLayout = FlexBox(self._footer)
        self._footerLayout.setSpacing(12)
        self._footerLayout.setContentsMargins(24, 0, 24, 12)

        self._cancelBtn = ActionButton()
        self._cancelBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=10))
        self._cancelBtn.setClassName("rounded-4 text-black bg-gray-12 hover:bg-gray-25 py-8 px-24")
        self._cancelBtn.setText("Cancel")

        self._saveBtn = ActionButton()
        self._saveBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=10))
        self._saveBtn.setClassName("rounded-4 text-white bg-primary-75 bg-primary py-8 px-24")
        self._saveBtn.setText("Save")

        self._footerLayout.addStretch(1)
        self._footerLayout.addWidget(self._cancelBtn)
        self._footerLayout.addWidget(self._saveBtn)
