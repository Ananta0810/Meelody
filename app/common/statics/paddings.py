from typing import final

from app.helpers.stylesheets.padding import Padding


@final
class Paddings:
    DEFAULT = Padding(0.00)
    RELATIVE_25 = Padding(0.25)
    RELATIVE_33 = Padding(0.33)
    RELATIVE_50 = Padding(0.5)
    RELATIVE_67 = Padding(0.67)
    RELATIVE_75 = Padding(0.75)
    RELATIVE_100 = Padding(1.00)

    ABSOLUTE_SMALL = Padding(4)
    ABSOLUTE_MEDIUM = Padding(12)

    LABEL_SMALL = Padding(1.25, 0.625, isRelative=True)
    LABEL_MEDIUM = Padding(1.25, 0.625, isRelative=True)
    LABEL_LARGE = Padding(1.5, 1, isRelative=True)
