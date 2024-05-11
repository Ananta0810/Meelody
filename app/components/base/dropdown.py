from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QWidget, QStyledItemDelegate

from app.resource.qt import Cursors


class DropDown(QComboBox):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setItemDelegate(QStyledItemDelegate())
        self.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.view().window().setAttribute(Qt.WA_TranslucentBackground)
        self.setCursor(Cursors.HAND)
        self.view().setCursor(Cursors.HAND)

        styleSheet = (
            """
            QComboBox {
                padding: 8px 16px;
                color: black;
                border: 1px solid rgb(230, 230, 230);
                border-radius: 4px;
                background-color: rgb(255, 255, 255);
            }
            QComboBox:hover, QPushButton:hover {
                background-color: rgb(248, 248, 248)
            }
            QComboBox::drop-down {
                border: none;
                background-color: transparent;
                min-width: 4px;
            }
            QComboBox::down-arrow {
                right: 8px;
                width: 8px;
                height: 8px;
                image: url('app/resource/images/icons/chevron-down.png');
            }
            QComboBox QAbstractItemView {
                margin-top: 4px;
                padding: 4px;
                border: 1px solid rgb(230, 230, 230);
                border-radius: 4px;
                background-color: rgb(255, 255, 255);
                outline: 0px;
            }
            QComboBox QAbstractItemView::item {
                padding: 4px 8px;
                border-radius: 4px;
                border: none;
                background-color: rgb(255, 255, 255);
                color: black;
            }
            QComboBox QAbstractItemView::item:hover,QComboBox QAbstractItemView::item:focus {
                background-color: rgb(240, 240, 240);
            }
             """
        )

        self.setStyleSheet(styleSheet)
