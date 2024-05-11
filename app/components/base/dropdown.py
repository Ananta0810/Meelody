from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QWidget, QStyledItemDelegate

from app.components.base import Component


class DropDown(QComboBox, Component):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setItemDelegate(QStyledItemDelegate())
        self.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.view().window().setAttribute(Qt.WA_TranslucentBackground)

        styleSheet = (
            "QComboBox {"
            + f"    padding: 2px;"
            + f"    color: black;"
            + f"    border: none;"
            + f"    border-radius: 4px;"
            + f"    background-color: rgb(255, 255, 255);"
            + "}"
            + "QComboBox:hover, QPushButton:hover{"
            + f"    border-color: #4032ff"
            + "}"
            + "QComboBox QAbstractItemView"
            + "{"
            + "    margin-top: 4px;"
            + f"    padding:  2px;"
            + f"    border: none;"
            + f"    border-radius: 4px;;"
            + f"    background-color: rgb(255, 255, 255);"
            + "}"
            + "QComboBox::drop-down {"
            + "    border:none;"
            + "    background-color:TRANSPARENT;"
            + f"    min-width: 4px;"
            + " }"
            + "QComboBox::down-arrow{"
            + f"    right: 4px;"
            + f"    width: 4px;"
            + f"    height: 4px;"
            # + f"    image: url('{dropDownArrowImage}');"
            + "}"
            + " /* Menu */"
            + "QComboBox QAbstractItemView::item{"
            + "    min-height: 32px;"
            + f"    padding: 4px;"
            + f"    border-radius: 4px;"
            + f"    border: none;"
            + f"    background-color: rgb(255, 255, 255);"
            + f"    color: black;"
              "}"
            + "QComboBox QAbstractItemView::item:hover,QComboBox QAbstractItemView::item:focus{"
            + f"    border: none;"
            + f"    border-radius: 4px;"
            + f"    background-color: rgb(255, 255, 255);"
            + f"    color: black;"
              "}"
            + "QComboBox:editable {"
            + "    background-color:TRANSPARENT;"
            + "    border:none;"
            + "}"
            + "QComboBox QAbstractItemView{outline:0px;}"
            + "QComboBox::indicator{"
            + "    background-color:TRANSPARENT;"
            + "    selection-background-color:TRANSPARENT;"
            + "    color:TRANSPARENT;"
            + "    selection-color:TRANSPARENT;"
            + "}"
        )

        self.setStyleSheet(styleSheet)
