from .text.abstract_text import AbstractLabel
from .text.editable_label import EditableLabel
from .text.standard_label import StandardLabel


class LabelFactory:
    def getLabel(self, type: str) -> AbstractLabel:
        if type == "editable":
            return EditableLabel()
        return StandardLabel()
