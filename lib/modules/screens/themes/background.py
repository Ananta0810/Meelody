from abc import ABC, abstractmethod
from sys import path

path.append("./lib")

from constants.ui.qss import *


class StyleSheetContent(ABC):
    @abstractmethod
    def export(self) -> str:
        pass


class BackgroundStyleSheet(StyleSheetContent):
    def export(self, id, background):
        return (
            f"{id}"
            + "{"
            + f"  border:{background.borderStyleSheet()};"
            + f"  border-radius:{background.borderRadiusStyleSheet(0)};"
            + f"  background-color:{background.colorStyleSheet()};"
            + "}"
            + f"{id}:hover"
            + "{"
            + f"  border:{background.borderStyleSheet(active=True)};"
            + f"  background-color:{background.colorStyleSheet(active=True)};"
            + "}"
        )


class PushButton:
    def __init__(self, styleSheet: BackgroundStyleSheet):
        self.id = "QPushButton"
        self.styleSheet = styleSheet

    def export(self, background) -> str:
        return self.styleSheet.export(self.id, background)


class CheckedButton:
    def __init__(self, styleSheet: BackgroundStyleSheet):
        self.id = "QPushButton:checked"
        self.styleSheet = styleSheet

    def export(self, background) -> str:
        return self.styleSheet.export(self.id, background)


a = CheckedButton(BackgroundStyleSheet())
print(
    a.export(
        QSSBackground(
            borderRadius=0.5,
            color=ColorBoxes.HIDDEN_PRIMARY,
        )
    )
)
