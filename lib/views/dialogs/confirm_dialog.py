from typing import Optional

from constants.ui.qss import Backgrounds, ColorBoxes
from constants.ui.qt import AppCursors
from modules.screens.components.font_builder import FontBuilder
from modules.screens.themes.theme_builders import TextThemeBuilder, TextThemeBuilder, ThemeData
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QGraphicsDropShadowEffect, QLabel, QVBoxLayout, QWidget
from views.view import View


class ConfirmDialog(QDialog, View):
    def __init__(
        self,
        header: str,
        msg: str,
        acceptText: str = "Confirm",
        rejectText: str = "Cancel",
        darkMode: bool = False,
        parent: Optional["QWidget"] = None,
    ):
        super(ConfirmDialog, self).__init__(parent)
        self.setupUi(header, msg, acceptText, rejectText)
        if darkMode:
            self.darkMode()
        else:
            self.lightMode()

    def setupUi(
        self,
        header: str,
        msg: str,
        acceptText: str,
        rejectText: str,
    ):
        fontBuilder = FontBuilder()
        buttonFont = fontBuilder.withSize(10).withWeight("bold").build()
        buttonThemeBuilder = TextThemeBuilder()
        labelTheme = (
            TextThemeBuilder()
            .addLightModeTextColor(ColorBoxes.BLACK)
            .addDarkModeTextColor(ColorBoxes.WHITE)
            .addLightModeBackground(None)
            .addDarkModeBackground(None)
            .build(itemSize=40)
        )
        cursors = AppCursors()
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.view = QWidget(self)
        self.view.setContentsMargins(24, 24, 24, 16)
        # self.setGraphicsEffect(
        #     QGraphicsDropShadowEffect(
        #         blurRadius=50,
        #         color=ColorUtils.getQColorFromColor(Colors.PRIMARY.withAlpha(0.25)),
        #         xOffset=0,
        #         yOffset=3,
        #     )
        # )
        self._addThemeForItem(
            self.view,
            ThemeData(lightMode="background:WHITE;border-radius:24px", darkMode="background:BLACK;border-radius:24px"),
        )
        self.viewLayout = QVBoxLayout(self.view)
        self.viewLayout.setSpacing(20)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        acceptBtn = self.buttonBox.button(QDialogButtonBox.Ok)
        acceptBtn.setFixedSize(144, 40)
        acceptBtn.setText(acceptText)
        acceptBtn.setFont(buttonFont)
        acceptBtn.setCursor(cursors.HAND)
        self._addThemeForItem(
            acceptBtn,
            theme=(
                buttonThemeBuilder.addLightModeTextColor(ColorBoxes.WHITE)
                .addLightModeBackground(Backgrounds.ROUNDED_PRIMARY)
                .build()
            ),
        )
        rejectBtn = self.buttonBox.button(QDialogButtonBox.Cancel)
        rejectBtn.setFixedSize(144, 40)
        rejectBtn.setText(rejectText)
        rejectBtn.setFont(buttonFont)
        rejectBtn.setCursor(cursors.HAND)
        self._addThemeForItem(
            rejectBtn,
            theme=(
                buttonThemeBuilder.addLightModeTextColor(ColorBoxes.PRIMARY)
                .addDarkModeTextColor(ColorBoxes.WHITE)
                .addLightModeBackground(Backgrounds.ROUNDED_PRIMARY_25)
                .addDarkModeBackground(Backgrounds.ROUNDED_WHITE_25)
                .build()
            ),
        )

        self.header = QLabel()
        self.header.setFont(fontBuilder.withSize(16).withWeight("bold").build())
        self.header.setText(header)
        self.header.setWordWrap(True)
        self._addThemeForItem(self.header, theme=labelTheme)

        self.message = QLabel()
        self.message.setFont(fontBuilder.withSize(10).withWeight("normal").build())
        self.message.setText(msg)
        self.message.setWordWrap(True)
        self._addThemeForItem(self.message, theme=labelTheme)

        self.viewLayout.addWidget(self.header)
        self.viewLayout.addWidget(self.message)
        self.viewLayout.addWidget(self.buttonBox)
        self.view.setFixedSize(self.view.sizeHint())
