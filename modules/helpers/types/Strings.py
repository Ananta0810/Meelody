import string
from locale import setlocale, LC_ALL, strxfrm


class Strings:
    setlocale(LC_ALL, "")

    @staticmethod
    def toLower(text: str) -> str:
        if text is None:
            return ''
        return strxfrm(text.lower())

    @staticmethod
    def toUpper(text: str) -> str:
        if text is None:
            return ''
        return strxfrm(text.upper())

    @staticmethod
    def compare(str1: str, str2: str) -> int:
        str1 = Strings.toLower(str1)
        str2 = Strings.toLower(str2)
        if str1 < str2:
            return -1
        if str1 > str2:
            return 1
        return 0

    @staticmethod
    def unindent(value: str):
        return '\n'.join(map(str.lstrip, [line for line in value.splitlines() if line != "\n"]))

    @staticmethod
    def unindent_multiple_lines(value: str):
        indent: int = (next(i for i, j in enumerate(value) if j not in string.whitespace) - 1) * ' '
        lines = [line.replace(indent, '') for line in value.splitlines() if line != ""]
        return '\n'.join(lines)

    @staticmethod
    def indent(value: str, level: int = 1):
        indent: str = '\n' + '    ' * level
        return indent.join(map(str.lstrip, value.splitlines()))

    @staticmethod
    def float_to_clock_time(time: float) -> str:
        time = int(time)
        mm = time // 60
        ss = time % 60
        return ":".join([str(mm).zfill(2), str(ss).zfill(2)])