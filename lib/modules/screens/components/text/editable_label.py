from sys import path

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLineEdit

from .abstract_text import AbstractLabel

path.append("./lib")
from modules.screens.qss.qss_elements import QSSBackground, ColorBox, QSSPadding
from widgets.placeholder_label import LabelWithPlaceholder


class EditableLabel(AbstractLabel):
    def render(
        self,
        font: QFont,
        color: ColorBox = None,
        padding: QSSPadding = None,
        background: QSSBackground = None,
        alignment=None,
        parent=None,
    ) -> QLineEdit:
        label = LabelWithPlaceholder(parent)
        if alignment is not None:
            label.setAlignment(alignment)
        label.setFont(font)
        styleSheet: str = (
            "QLineEdit{"
            + f"  padding:{padding.toStylesheet() if padding is not None else 0};"
            + f"  border:{background.borderStyleSheet() if background is not None else None};"
            + f"  border-radius:{background.borderRadiusStyleSheet() if background is not None else None};"
            + f"  color:{color.toStylesheet() if color is not None else None};"
            + f"  background:{background.colorStyleSheet() if background is not None else 'transparent'};"
            + "}"
            + "QLineEdit::hover{"
            + f"  border:{background.borderStyleSheet(active=True) if background is not None else None};"
            + f"  color:{color.toStylesheet(active=True) if color is not None else None};"
            + f"  background:{background.colorStyleSheet(active=True) if background is not None else 'transparent'};"
            + "}"
        )
        label.setStyleSheet(styleSheet)
        # self.lineEdit.selectionChanged.connect(lambda: self.lineEdit.setSelection(0, 0))
        # label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        return label
