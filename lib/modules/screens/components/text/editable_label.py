from sys import path

from PyQt5.QtWidgets import QLineEdit

from .abstract_text import AbstractLabel

path.append("./lib")
from modules.screens.qss.qss_elements import QSSBackground, QSSFont, QSSPadding


class EditableLabel(AbstractLabel):
    def render(
        self,
        font: QSSFont,
        padding: QSSPadding = None,
        background: QSSBackground = None,
        alignment=None,
        parent=None,
    ) -> QLineEdit:
        label = QLineEdit(parent)
        if alignment is not None:
            label.setAlignment(alignment)
        label.setFont(font.font)
        styleSheet: str = (
            "QLineEdit{"
            + f"  color:{font.colorStyleSheet() if font is not None else None};"
            + f"  background:{background.colorStyleSheet() if background is not None else 'transparent'};"
            + f"  border-radius:{background.borderRadiusStyleSheet() if background is not None else None};"
            + f"  padding:{padding.toStylesheet() if padding is not None else 0}"
            + "}"
            + "QLineEdit::hover{"
            + f"  color:{font.colorStyleSheet(active=True) if font is not None else None};"
            + f"  background:{background.colorStyleSheet(active=True) if background is not None else 'transparent'}"
            + "}"
        )
        label.setStyleSheet(styleSheet)
        # label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        return label
