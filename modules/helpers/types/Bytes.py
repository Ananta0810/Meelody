import io
from io import BytesIO

from PIL import Image


class Bytes:
    @staticmethod
    def get_bytes_from_file(path_name: str) -> bytes:
        with open(path_name, "rb") as file:
            return bytearray(file.read())

    @staticmethod
    def decode(value: bytes | None) -> str | None:
        return None if value is None else value.decode('iso-8859-1')

    @staticmethod
    def encode(value: str | None) -> bytes | None:
        return None if value is None else value.encode('iso-8859-1')


class BytesModifier:
    _data: Image

    def __init__(self, data: Image):
        self._data = data
        self._data.load()

    @staticmethod
    def of(data: bytes) -> 'BytesModifier':
        return BytesModifier(Image.open(BytesIO(data)))

    def get_size(self) -> tuple:
        if self.isBroken():
            return 0, 0
        return self._data.size

    def isBroken(self) -> bool:
        try:
            self._data.verify()
            return False
        except TypeError:
            return True

    def crop(self, left, top, right, bottom) -> 'BytesModifier':
        image: Image = self._data.copy().crop((left, top, right, bottom))
        return BytesModifier(image)

    def square(self) -> 'BytesModifier':
        if self.isBroken():
            return self
        width, height = self._data.size

        if width == height:
            return self

        left, top, right, bottom = 0, 0, 0, 0

        if width > height:
            left = (width - height) // 2
            right = (width + height) // 2
            top = 0
            bottom = height

        elif width < height:
            left = 0
            right = width
            top = (height - width) // 2
            bottom = (height + width) // 2

        image: Image = self._data.copy().crop((left, top, right, bottom))
        return BytesModifier(image)

    def resize(self, width: int, height: int) -> 'BytesModifier':
        if self.isBroken():
            return self
        image: Image = self._data.copy().resize((width, height), Image.ANTIALIAS)
        return BytesModifier(image)

    def to_bytes(self) -> bytes:
        byteIO = io.BytesIO()
        self._data.save(byteIO, format='PNG')
        return byteIO.getvalue()
