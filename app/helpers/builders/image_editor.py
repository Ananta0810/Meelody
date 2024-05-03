import io
from io import BytesIO

from PIL import Image, UnidentifiedImageError

from app.common.exceptions import ResourceException


class ImageEditor:

    def __init__(self, data: Image):
        self._data = data
        self._data.load()

    @staticmethod
    def of(data: bytes) -> 'ImageEditor':
        return ImageEditor(Image.open(BytesIO(data)))

    @staticmethod
    def ofFile(file: str) -> 'ImageEditor':
        try:
            return ImageEditor(Image.open(file))
        except (FileNotFoundError, UnidentifiedImageError, OSError):
            raise ResourceException.notFound()

    def getSize(self) -> tuple:
        if self.isBroken():
            return 0, 0
        return self._data.size

    def isBroken(self) -> bool:
        try:
            self._data.verify()
            return False
        except TypeError:
            return True
        except AttributeError:
            return False

    def crop(self, left, top, right, bottom) -> 'ImageEditor':
        image: Image = self._data.copy().crop((left, top, right, bottom))
        return ImageEditor(image)

    def square(self) -> 'ImageEditor':
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
        return ImageEditor(image)

    def resize(self, width: int, height: int) -> 'ImageEditor':
        if self.isBroken():
            return self
        image: Image = self._data.copy().resize((width, height), Image.ANTIALIAS)
        return ImageEditor(image)

    def toBytes(self) -> bytes:
        byteIO = io.BytesIO()
        self._data.save(byteIO, format='PNG')
        return byteIO.getvalue()
