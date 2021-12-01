from sys import path

from PyQt5.QtWidgets import QLineEdit

from .abstract_text import AbstractLabel

path.append("./lib")
from modules.screens.qss.qss_elements import QSSBackground, QSSFont, QSSPadding


class StandardLabel(AbstractLabel):
    def render(
        self,
        font: QSSFont,
        padding: QSSPadding = None,
        background: QSSBackground = None,
        parent=None,
    ) -> QLineEdit:
        label = QLineEdit(parent)
        label.setFont(font.font)

        label.setReadOnly(True)
        # self.lineEdit.selectionChanged.connect(lambda: self.lineEdit.setSelection(0, 0))
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
        return label
