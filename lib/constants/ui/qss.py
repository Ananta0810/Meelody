from modules.screens.qss.qss_elements import Background, Color, ColorBox, Padding

from .metaclass import SingletonConst


class Paddings(metaclass=SingletonConst):
    RELATIVE_25 = Padding(0.25)
    RELATIVE_33 = Padding(0.33)
    RELATIVE_50 = Padding(0.5)
    RELATIVE_67 = Padding(0.67)
    RELATIVE_75 = Padding(0.75)
    RELATIVE_100 = Padding(1)

    ABSOLUTE_SMALL = Padding(4)
    ABSOLUTE_MEDIUM = Padding(12)

    LABEL_SMALL = Padding(1.25, 0.625, relativeOnly=True)
    LABEL_MEDIUM = Padding(1.25, 0.625, relativeOnly=True)
    LABEL_LARGE = Padding(1.5, 1, relativeOnly=True)


class Colors(metaclass=SingletonConst):
    PRIMARY = Color(128, 64, 255)

    SUCCESS = Color(50, 216, 100)
    DANGER = Color(255, 80, 80)
    WARNING = Color(255, 170, 28)

    WHITE = Color(255, 255, 255)
    BLACK = Color(0, 0, 0)
    GRAY = Color(128, 128, 128)
    TRANSPARENT = Color(255, 255, 255, 0)


class ColorBoxes(metaclass=SingletonConst):
    TRANSPARENT = ColorBox(Colors.TRANSPARENT)

    # =========================Primary=========================
    PRIMARY = ColorBox(Colors.PRIMARY)
    PRIMARY_75 = ColorBox(Colors.PRIMARY.withAlpha(0.50))
    PRIMARY_50 = ColorBox(Colors.PRIMARY.withAlpha(0.33))
    PRIMARY_25 = ColorBox(Colors.PRIMARY.withAlpha(0.15))

    HOVERABLE_PRIMARY = ColorBox(
        normal=Colors.PRIMARY.withAlpha(0.83),
        active=Colors.PRIMARY,
    )
    HOVERABLE_PRIMARY_50 = ColorBox(
        normal=Colors.PRIMARY.withAlpha(0.33),
        active=Colors.PRIMARY.withAlpha(0.50),
    )
    HOVERABLE_PRIMARY_25 = ColorBox(
        normal=Colors.PRIMARY.withAlpha(0.15),
        active=Colors.PRIMARY.withAlpha(0.25),
    )
    HOVERABLE_HIDDEN_PRIMARY = ColorBox(
        normal=Colors.TRANSPARENT,
        active=Colors.PRIMARY.withAlpha(0.83),
    )
    HOVERABLE_HIDDEN_PRIMARY_50 = ColorBox(
        normal=Colors.TRANSPARENT,
        active=Colors.PRIMARY.withAlpha(0.33),
    )
    HOVERABLE_HIDDEN_PRIMARY_25 = ColorBox(
        normal=Colors.TRANSPARENT,
        active=Colors.PRIMARY.withAlpha(0.15),
    )

    # =========================Danger=========================
    DANGER = ColorBox(Colors.DANGER)
    DANGER_75 = ColorBox(Colors.DANGER.withAlpha(0.50))
    DANGER_50 = ColorBox(Colors.DANGER.withAlpha(0.33))
    DANGER_25 = ColorBox(Colors.DANGER.withAlpha(0.15))

    HOVERABLE_DANGER = ColorBox(
        normal=Colors.DANGER.withAlpha(0.83),
        active=Colors.DANGER,
    )
    HOVERABLE_DANGER_50 = ColorBox(
        normal=Colors.DANGER.withAlpha(0.33),
        active=Colors.DANGER.withAlpha(0.50),
    )
    HOVERABLE_DANGER_25 = ColorBox(
        normal=Colors.DANGER.withAlpha(0.15),
        active=Colors.DANGER.withAlpha(0.25),
    )

    HOVERABLE_HIDDEN_DANGER = ColorBox(
        normal=Colors.TRANSPARENT,
        active=Colors.DANGER.withAlpha(0.83),
    )
    HOVERABLE_HIDDEN_DANGER_50 = ColorBox(
        normal=Colors.TRANSPARENT,
        active=Colors.DANGER.withAlpha(0.33),
    )
    HOVERABLE_HIDDEN_DANGER_25 = ColorBox(
        normal=Colors.TRANSPARENT,
        active=Colors.DANGER.withAlpha(0.15),
    )

    # =========================White=========================
    WHITE = ColorBox(Colors.WHITE)
    WHITE_75 = ColorBox(Colors.WHITE.withAlpha(0.50))
    WHITE_50 = ColorBox(Colors.WHITE.withAlpha(0.33))
    WHITE_25 = ColorBox(Colors.WHITE.withAlpha(0.15))

    HOVERABLE_WHITE = ColorBox(
        normal=Colors.WHITE.withAlpha(0.83),
        active=Colors.WHITE,
    )
    HOVERABLE_WHITE_50 = ColorBox(
        normal=Colors.WHITE.withAlpha(0.33),
        active=Colors.WHITE.withAlpha(0.50),
    )
    HOVERABLE_WHITE_25 = ColorBox(
        normal=Colors.WHITE.withAlpha(0.15),
        active=Colors.WHITE.withAlpha(0.25),
    )

    HOVERABLE_HIDDEN_WHITE = ColorBox(
        normal=Colors.TRANSPARENT,
        active=Colors.WHITE.withAlpha(0.83),
    )
    HOVERABLE_HIDDEN_WHITE_50 = ColorBox(
        normal=Colors.TRANSPARENT,
        active=Colors.WHITE.withAlpha(0.33),
    )
    HOVERABLE_HIDDEN_WHITE_25 = ColorBox(
        normal=Colors.TRANSPARENT,
        active=Colors.WHITE.withAlpha(0.15),
    )

    # =========================Danger=========================
    BLACK = ColorBox(Colors.BLACK)
    BLACK_75 = ColorBox(Colors.BLACK.withAlpha(0.50))
    BLACK_50 = ColorBox(Colors.BLACK.withAlpha(0.33))
    BLACK_25 = ColorBox(Colors.BLACK.withAlpha(0.15))

    HOVERABLE_BLACK = ColorBox(
        normal=Colors.BLACK.withAlpha(0.83),
        active=Colors.BLACK,
    )
    HOVERABLE_BLACK_50 = ColorBox(
        normal=Colors.BLACK.withAlpha(0.33),
        active=Colors.BLACK.withAlpha(0.50),
    )
    HOVERABLE_BLACK_25 = ColorBox(
        normal=Colors.BLACK.withAlpha(0.15),
        active=Colors.BLACK.withAlpha(0.25),
    )

    HOVERABLE_HIDDEN_BLACK = ColorBox(
        normal=Colors.TRANSPARENT,
        active=Colors.BLACK.withAlpha(0.83),
    )
    HOVERABLE_HIDDEN_BLACK_50 = ColorBox(
        normal=Colors.TRANSPARENT,
        active=Colors.BLACK.withAlpha(0.33),
    )
    HOVERABLE_HIDDEN_BLACK_25 = ColorBox(
        normal=Colors.TRANSPARENT,
        active=Colors.BLACK.withAlpha(0.15),
    )

    # =========================Gray=========================
    GRAY = ColorBox(Colors.GRAY)
    GRAY_75 = ColorBox(Colors.GRAY.withAlpha(0.50))
    GRAY_50 = ColorBox(Colors.GRAY.withAlpha(0.33))
    GRAY_25 = ColorBox(Colors.GRAY.withAlpha(0.15))

    HOVERABLE_GRAY = ColorBox(
        normal=Colors.GRAY.withAlpha(0.83),
        active=Colors.GRAY,
    )
    HOVERABLE_GRAY_50 = ColorBox(
        normal=Colors.GRAY.withAlpha(0.33),
        active=Colors.GRAY.withAlpha(0.50),
    )
    HOVERABLE_GRAY_25 = ColorBox(
        normal=Colors.GRAY.withAlpha(0.15),
        active=Colors.GRAY.withAlpha(0.25),
    )

    HOVERABLE_HIDDEN_GRAY = ColorBox(
        normal=Colors.TRANSPARENT,
        active=Colors.GRAY.withAlpha(0.83),
    )
    HOVERABLE_HIDDEN_GRAY_50 = ColorBox(
        normal=Colors.TRANSPARENT,
        active=Colors.GRAY.withAlpha(0.33),
    )
    HOVERABLE_HIDDEN_GRAY_25 = ColorBox(
        normal=Colors.TRANSPARENT,
        active=Colors.GRAY.withAlpha(0.15),
    )


class Backgrounds(metaclass=SingletonConst):

    # =========================Primary=========================
    CIRCLE_PRIMARY = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_PRIMARY,
    )
    CIRCLE_PRIMARY_50 = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_PRIMARY_50,
    )
    CIRCLE_PRIMARY_25 = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_PRIMARY_25,
    )

    CIRCLE_HIDDEN_PRIMARY = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_HIDDEN_PRIMARY,
    )
    CIRCLE_HIDDEN_PRIMARY_50 = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_HIDDEN_PRIMARY_50,
    )
    CIRCLE_HIDDEN_PRIMARY_25 = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_HIDDEN_PRIMARY_25,
    )

    ROUNDED_PRIMARY = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_PRIMARY,
    )
    ROUNDED_PRIMARY_50 = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_PRIMARY_50,
    )
    ROUNDED_PRIMARY_25 = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_PRIMARY_25,
    )

    ROUNDED_HIDDEN_PRIMARY = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_HIDDEN_PRIMARY,
    )
    ROUNDED_HIDDEN_PRIMARY_50 = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_HIDDEN_PRIMARY_50,
    )
    ROUNDED_HIDDEN_PRIMARY_25 = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_HIDDEN_PRIMARY_25,
    )

    # =========================Danger=========================
    CIRCLE_DANGER = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_DANGER,
    )
    CIRCLE_DANGER_50 = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_DANGER_50,
    )
    CIRCLE_DANGER_25 = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_DANGER_25,
    )

    CIRCLE_HIDDEN_DANGER = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_HIDDEN_DANGER,
    )
    CIRCLE_HIDDEN_DANGER_50 = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_HIDDEN_DANGER_50,
    )
    CIRCLE_HIDDEN_DANGER_25 = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_HIDDEN_DANGER_25,
    )

    ROUNDED_DANGER = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_DANGER,
    )
    ROUNDED_DANGER_50 = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_DANGER_50,
    )
    ROUNDED_DANGER_25 = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_DANGER_25,
    )

    ROUNDED_HIDDEN_DANGER = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_HIDDEN_DANGER,
    )
    ROUNDED_HIDDEN_DANGER_50 = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_HIDDEN_DANGER_50,
    )
    ROUNDED_HIDDEN_DANGER_25 = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_HIDDEN_DANGER_25,
    )

    # =========================White=========================
    CIRCLE_WHITE = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_WHITE,
    )
    CIRCLE_WHITE_50 = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_WHITE_50,
    )
    CIRCLE_WHITE_25 = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_WHITE_25,
    )

    CIRCLE_HIDDEN_WHITE = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_HIDDEN_WHITE,
    )
    CIRCLE_HIDDEN_WHITE_50 = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_HIDDEN_WHITE_50,
    )
    CIRCLE_HIDDEN_WHITE_25 = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_HIDDEN_WHITE_25,
    )

    ROUNDED_WHITE = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_WHITE,
    )
    ROUNDED_WHITE_50 = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_WHITE_50,
    )
    ROUNDED_WHITE_25 = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_WHITE_25,
    )

    ROUNDED_HIDDEN_WHITE = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_HIDDEN_WHITE,
    )
    ROUNDED_HIDDEN_WHITE_50 = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_HIDDEN_WHITE_50,
    )
    ROUNDED_HIDDEN_WHITE_25 = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_HIDDEN_WHITE_25,
    )

    # =========================Black=========================
    CIRCLE_BLACK = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_BLACK,
    )
    CIRCLE_BLACK_50 = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_BLACK_50,
    )
    CIRCLE_BLACK_25 = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_BLACK_25,
    )

    CIRCLE_HIDDEN_BLACK = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_HIDDEN_BLACK,
    )
    CIRCLE_HIDDEN_BLACK_50 = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_HIDDEN_BLACK_50,
    )
    CIRCLE_HIDDEN_BLACK_25 = Background(
        borderRadius=0.5,
        color=ColorBoxes.HOVERABLE_HIDDEN_BLACK_25,
    )

    ROUNDED_BLACK = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_BLACK,
    )
    ROUNDED_BLACK_50 = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_BLACK_50,
    )
    ROUNDED_BLACK_25 = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_BLACK_25,
    )

    ROUNDED_HIDDEN_BLACK = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_HIDDEN_BLACK,
    )
    ROUNDED_HIDDEN_BLACK_50 = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_HIDDEN_BLACK_50,
    )
    ROUNDED_HIDDEN_BLACK_25 = Background(
        borderRadius=12,
        color=ColorBoxes.HOVERABLE_HIDDEN_BLACK_25,
    )
