import string


class Strings:
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