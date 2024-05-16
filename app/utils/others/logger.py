from typing import final


class _ColorPrinter:
    DEFAULT = '\033[0m'
    # Styles
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    UNDERLINE_THICK = '\033[21m'
    HIGHLIGHTED = '\033[7m'
    HIGHLIGHTED_BLACK = '\033[40m'
    HIGHLIGHTED_RED = '\033[41m'
    HIGHLIGHTED_GREEN = '\033[42m'
    HIGHLIGHTED_YELLOW = '\033[43m'
    HIGHLIGHTED_BLUE = '\033[44m'
    HIGHLIGHTED_PURPLE = '\033[45m'
    HIGHLIGHTED_CYAN = '\033[46m'
    HIGHLIGHTED_GREY = '\033[47m'

    HIGHLIGHTED_GREY_LIGHT = '\033[100m'
    HIGHLIGHTED_RED_LIGHT = '\033[101m'
    HIGHLIGHTED_GREEN_LIGHT = '\033[102m'
    HIGHLIGHTED_YELLOW_LIGHT = '\033[103m'
    HIGHLIGHTED_BLUE_LIGHT = '\033[104m'
    HIGHLIGHTED_PURPLE_LIGHT = '\033[105m'
    HIGHLIGHTED_CYAN_LIGHT = '\033[106m'
    HIGHLIGHTED_WHITE_LIGHT = '\033[107m'

    STRIKE_THROUGH = '\033[9m'
    MARGIN_1 = '\033[51m'
    MARGIN_2 = '\033[52m'  # seems equal to MARGIN_1
    # colors
    BLACK = '\033[30m'
    RED_DARK = '\033[31m'
    GREEN_DARK = '\033[32m'
    YELLOW_DARK = '\033[33m'
    BLUE_DARK = '\033[34m'
    PURPLE_DARK = '\033[35m'
    CYAN_DARK = '\033[36m'
    GREY_DARK = '\033[37m'

    BLACK_LIGHT = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[96m'

    def __init__(self):
        self.__printOriginal = print  # old value to the original print function
        self.__currentColor = self.DEFAULT

    def print(self,
              *values: object, sep: str | None = None,
              end: str | None = None,
              file: str | None = None,
              flush: bool = False,
              color: str | None = None,
              defaultColor: str | None = None,
              ):
        if defaultColor:
            self.__currentColor = defaultColor

        default = self.__currentColor
        if color:
            values = (color, *values, default)  # wrap the content within a selected color an a default
        else:
            values = (*values, default)  # wrap the content within a selected color an a default
        self.__printOriginal(*values, end=end, file=file, flush=flush)


_colorPrinter = _ColorPrinter()


@final
class Logger:
    @staticmethod
    def error(message: any) -> None:
        _colorPrinter.print(f"Error::{message}", color=_ColorPrinter.RED)

    @staticmethod
    def warn(message: any) -> None:
        _colorPrinter.print(f"Warn::{message}", color=_ColorPrinter.YELLOW_DARK)

    @staticmethod
    def info(message: any) -> None:
        _colorPrinter.print(f"Info::{message}", color=_ColorPrinter.BLUE)
