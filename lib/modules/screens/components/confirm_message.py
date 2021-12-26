from typing import Optional

from constants.ui.qss import ColorBoxes, Colors
from constants.ui.qt import AppCursors
from modules.screens.components.font_builder import FontBuilder
from modules.screens.qss.qss_elements import Background
from modules.screens.themes.theme_builders import ActionButtonThemeBuilder, LabelThemeBuilder, ThemeData
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QGraphicsDropShadowEffect, QLabel, QVBoxLayout, QWidget
from utils.ui.color_utils import ColorUtils


class ConfirmMessage(QDialog):
    def __init__(
        self,
        header: str,
        msg: str,
        acceptText: str = "Confirm",
        rejectText: str = "Cancel",
        darkMode: bool = False,
        parent: Optional["QWidget"] = None,
    ):
        super().__init__(parent)
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
        labelThemeBuilder = LabelThemeBuilder()
        buttonThemeBuilder = ActionButtonThemeBuilder()
        labelTheme = (
            labelThemeBuilder.addLightModeTextColor(ColorBoxes.BLACK)
            .addDarkModeTextColor(ColorBoxes.WHITE)
            .addLightModeBackground(None)
            .addDarkModeBackground(None)
            .build(itemSize=40)
        )
        cursors = AppCursors()
        self.themeItems: dict[str, ThemeData] = {}

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.__addThemeForItem(
            self,
            ThemeData(lightMode="background:WHITE;border-radius:24px", darkMode="background:BLACK;border-radius:24px"),
        )
        # self.setGraphicsEffect(
        #     QGraphicsDropShadowEffect(
        #         blurRadius=50,
        #         color=ColorUtils.getQColorFromColor(Colors.PRIMARY.withAlpha(0.25)),
        #         xOffset=0,
        #         yOffset=3,
        #     )
        # )

        self.view = QWidget(self)
        self.view.setContentsMargins(24, 24, 24, 16)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        acceptBtn = self.buttonBox.button(QDialogButtonBox.Ok)
        acceptBtn.setFixedSize(144, 40)
        acceptBtn.setText(acceptText)
        acceptBtn.setFont(buttonFont)
        acceptBtn.setCursor(cursors.HAND)
        self.__addThemeForItem(
            acceptBtn,
            theme=(
                buttonThemeBuilder.addLightModeTextColor(ColorBoxes.WHITE)
                .addLightModeBackground(Background(borderRadius=8, color=ColorBoxes.PRIMARY_HOVERABLE))
                .build(itemSize=40)
            ),
        )
        rejectBtn = self.buttonBox.button(QDialogButtonBox.Cancel)
        rejectBtn.setFixedSize(144, 40)
        rejectBtn.setText(rejectText)
        rejectBtn.setFont(buttonFont)
        rejectBtn.setCursor(cursors.HAND)
        self.__addThemeForItem(
            rejectBtn,
            theme=(
                buttonThemeBuilder.addLightModeTextColor(ColorBoxes.PRIMARY)
                .addDarkModeTextColor(ColorBoxes.WHITE)
                .addLightModeBackground(Background(borderRadius=8, color=ColorBoxes.HOVERABLE_PRIMARY_25))
                .addDarkModeBackground(Background(borderRadius=8, color=ColorBoxes.HOVERABLE_WHITE_25))
                .build(itemSize=40)
            ),
        )

        self.viewLayout = QVBoxLayout(self.view)
        self.viewLayout.setSpacing(20)

        self.header = QLabel()
        self.header.setFont(fontBuilder.withSize(16).withWeight("bold").build())
        self.header.setText(header)
        self.header.setWordWrap(True)
        self.__addThemeForItem(self.header, theme=labelTheme)

        self.message = QLabel()
        self.message.setFont(fontBuilder.withSize(10).withWeight("normal").build())
        self.message.setText(msg)
        self.message.setWordWrap(True)
        self.__addThemeForItem(self.message, theme=labelTheme)

        self.viewLayout.addWidget(self.header)
        self.viewLayout.addWidget(self.message)
        self.viewLayout.addWidget(self.buttonBox)
        self.view.setFixedSize(self.view.sizeHint())

    def lightMode(self):
        for item in self.themeItems:
            lightModeStyleSheet = self.themeItems.get(item).lightMode
            if lightModeStyleSheet is None or lightModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(lightModeStyleSheet)

    def darkMode(self):
        for item in self.themeItems:
            darkModeStyleSheet = self.themeItems.get(item).darkMode
            if darkModeStyleSheet is None or darkModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(darkModeStyleSheet)

    def __addThemeForItem(self, item, theme: ThemeData) -> None:
        self.themeItems[item] = theme
