from locale import LC_ALL, setlocale, strxfrm


class UnicodeString:
    setlocale(LC_ALL, "")

    @staticmethod
    def toLower(string: str) -> str:
        if string is None:
            return
        return strxfrm(string.lower())

    @staticmethod
    def toUpper(string: str) -> str:
        if string is None:
            return
        return strxfrm(string.upper())

    @staticmethod
    def compare(str1: str, str2: str) -> int:
        str1 = UnicodeString.toLower(str1)
        str2 = UnicodeString.toLower(str2)
        if str1 < str2:
            return -1
        if str1 > str2:
            return 1
        return 0


class Stringify:
    @staticmethod
    def floatToClockTime(time: float) -> str:
        time = int(time)
        mm = time // 60
        ss = time % 60
        return ":".join([str(mm).zfill(2), str(ss).zfill(2)])

    @staticmethod
    def clean_youtube_url(url: str):
        index = url.find("&list")
        if index != -1:
            url = url[:index]
        return url
