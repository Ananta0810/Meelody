from locale import LC_ALL, setlocale, strxfrm


class UnicodeString:
    setlocale(LC_ALL, "")

    @staticmethod
    def to_lower(string: str) -> str:
        if string is None:
            return
        return strxfrm(string.lower())

    @staticmethod
    def to_upper(string: str) -> str:
        if string is None:
            return
        return strxfrm(string.upper())

    @staticmethod
    def compare(str1: str, str2: str) -> int:
        str1 = UnicodeString.to_lower(str1)
        str2 = UnicodeString.to_lower(str2)
        if str1 < str2:
            return -1
        if str1 > str2:
            return 1
        return 0


class Stringify:
    @staticmethod
    def get_clock_time(time: float) -> str:
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
