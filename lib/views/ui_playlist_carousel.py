from sys import path

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

path.append("./lib")
from constants.ui.base import ApplicationImage
from constants.ui.qss import ColorBoxes, Colors, Paddings
from constants.ui.qt import AppAlignment, AppCursors, AppIcons
from modules.screens.components.factories import (
    IconButtonFactory,
    LabelFactory,
    SliderFactory,
)
from modules.screens.components.font_builder import FontBuilder
from modules.screens.qss.qss_elements import Background
from modules.screens.themes.theme_builders import ThemeData
from utils.helpers.my_string import Stringify
from utils.ui.application_utils import ApplicationUIUtils as AppUI
from widgets.hoverable_widget import HoverableWidget
from widgets.image_displayer import ImageDisplayer


class UiPlaylistCarousel(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.themeItems = {}
        self.buttonsWithDarkMode = []
        icons = AppIcons()
        cursors = AppCursors()

        iconButtonFormer = IconButtonFactory().getByType("default")
        labelFactory = LabelFactory()
        labelFormer = labelFactory.getByType("default")
        editableLabel = labelFactory.getByType("editable")
        labelThemeBuilder = editableLabel.getThemeBuilder()
        fontBuilder = FontBuilder()
        emphasizedFont = fontBuilder.withSize(16).withWeight("bold").build()
        # =================UI=================
        self.setMinimumSize(QSize(1368, 608))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.inner = QWidget()
        self.inner.setGeometry(QRect(0, 0, 1359, 340))
        self.inner.setStyleSheet("border:none")
        self.setWidget(self.inner)

        self.main_layout = QHBoxLayout(self.inner)
        self.main_layout.setAlignment(Qt.AlignLeft)
        self.main_layout.setSpacing(32)

        # =================Library=================
        self.library_card = HoverableWidget()
        self.library_card.setFixedWidth(256)
        self.library_cover = ImageDisplayer(self.library_card)
        self.library_cover.setGeometry(QRect(0, 0, 256, 320))
        self.library_cover.setCursor(cursors.HAND)
        self.library_label = labelFactory.getByType("default").render(
            font=emphasizedFont, parent=self.library_card
        )
        self.library_cover.setPixmap(
            self.__getPixmapForPlaylistCover(
                ApplicationImage.defaultPlaylistCover
            )
        )
        self.library_label.setFixedSize(160, 32)
        self.library_label.setText("Library")

        LABEL_LEFT_POSTION = 24
        LABEL_TOP_POSTION = self.__getPaddingPositionBotton(
            padding=16,
            parentHeight=self.library_cover.height(),
            itemHeight=self.library_label.height(),
        )
        self.library_label.move(LABEL_LEFT_POSTION, LABEL_TOP_POSTION)
        self.main_layout.addWidget(self.library_card)

        # =================Favourites=================
        self.favourite_card = HoverableWidget()
        self.favourite_card.setFixedWidth(256)
        self.favourite_cover = ImageDisplayer(self.favourite_card)
        self.favourite_cover.setGeometry(QRect(0, 0, 256, 320))
        self.favourite_cover.setCursor(cursors.HAND)
        self.favourite_label = labelFormer.render(
            font=emphasizedFont, parent=self.favourite_card
        )
        self.favourite_cover.setPixmap(
            self.__getPixmapForPlaylistCover(ApplicationImage.favouritesCover)
        )
        self.favourite_label.setFixedSize(160, 32)
        self.favourite_label.setText("Favourite")

        self.favourite_label.move(LABEL_LEFT_POSTION, LABEL_TOP_POSTION)

        self.main_layout.addWidget(self.favourite_card)

        # =================New playlist=================
        self.add_playlist_card = QWidget()
        # self.add_playlist_card.setFixedWidth(256)
        self.add_playlist_card.setFixedSize(256, 320)
        self.add_playlist_card.setObjectName("add_playlist_card")
        self.__addThemeForItem(
            self.add_playlist_card,
            theme=ThemeData(
                lightMode="#add_playlist_card{background:rgba(0,0,0,0.1);border-radius:24px}",
                darkMode="#add_playlist_card{background:rgba(255,255,255,0.25);border-radius:24px}",
            ),
        )
        self.add_playlist_btn = iconButtonFormer.render(
            padding=Paddings.RELATIVE_67,
            size=icons.SIZES.LARGE,
            lightModeIcon=AppUI.paintIcon(icons.ADD, Colors.PRIMARY),
            darkModeIcon=AppUI.paintIcon(icons.ADD, Colors.WHITE),
            parent=self.add_playlist_card,
        )
        self.add_playlist_btn.setCursor(cursors.HAND)
        self.add_playlist_btn.move(
            self.add_playlist_card.rect().center()
            - self.add_playlist_btn.rect().center()
        )
        self.__addButtonToList(self.add_playlist_btn)
        self.__addThemeForItem(
            self.add_playlist_btn,
            theme=(
                iconButtonFormer.getThemeBuilder()
                .addLightModeBackground(
                    Background(
                        borderRadius=0.5,
                        color=ColorBoxes.HIDDEN_PRIMARY,
                    )
                )
                .addDarkModeBackground(
                    Background(
                        borderRadius=0.5,
                        color=ColorBoxes.HIDDEN_WHITE,
                    )
                )
                .build(itemSize=icons.SIZES.LARGE.height())
            ),
        )

        self.main_layout.addWidget(self.add_playlist_card)

    def connectSignalsToController(self, controller):
        self.add_playlist_btn.clicked.connect(controller.handleAddNewPlaylist)

    def lightMode(self) -> None:
        for button in self.buttonsWithDarkMode:
            button.setDarkMode(False)
        for item in self.themeItems:
            lightModeStyleSheet = self.themeItems.get(item).lightMode
            if lightModeStyleSheet is None or lightModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(lightModeStyleSheet)

    def darkMode(self) -> None:
        for button in self.buttonsWithDarkMode:
            button.setDarkMode(True)
        for item in self.themeItems:
            darkModeStyleSheet = self.themeItems.get(item).darkMode
            if darkModeStyleSheet is None or darkModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(darkModeStyleSheet)

    def __addThemeForItem(self, item, theme: ThemeData) -> None:
        self.themeItems[item] = theme

    def __addButtonToList(self, item) -> None:
        self.buttonsWithDarkMode.append(item)

    def __getPaddingPositionBotton(self, padding, parentHeight, itemHeight):
        return parentHeight - itemHeight - padding

    def __getPixmapForPlaylistCover(self, coverAsByte: bytes) -> QPixmap:
        if coverAsByte is None:
            return None
        pixmap = AppUI.getEditedPixmapFromBytes(
            coverAsByte,
            width=self.library_cover.width(),
            height=self.library_cover.height(),
            cropCenter=False,
            radius=24,
        )
        return pixmap
