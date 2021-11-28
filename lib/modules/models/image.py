from io import BytesIO

import PIL.Image

from .color import Color


class MyByteImage:
    _data: PIL.Image

    def __init__(self, _data: bytes):
        self._data = PIL.Image.open(BytesIO(_data))
        self._data.load()

    def get_size(self) -> tuple:
        if self.isBroken():
            return (0, 0)
        return self._data.size

    def isBroken(self) -> bool:
        try:
            self._data.verify()
            return False
        except:
            return True

    def crop(self, left, top, right, bottom) -> PIL.Image:
        image = self._data.copy()
        image = image.crop((left, top, right, bottom))
        return image

    def square(self) -> PIL.Image:
        if self.isBroken():
            return
        image: PIL.Image = self._data.copy()
        width, height = image.size

        if width == height:
            return

        if width > height:
            left = (width - height) // 2
            right = (width + height) // 2
            top = 0
            bottom = height
            width = height

        elif width < height:
            left = 0
            right = width
            top = (height - width) // 2
            bottom = (height + width) // 2
            height = width

        image = image.crop((left, top, right, bottom))
        return image

    def resize(self, width: int, height: int) -> PIL.Image:
        if self.isBroken():
            return
        image: PIL.Image = self._data.copy()
        image = self._data.resize((width, height), PIL.Image.ANTIALIAS)
        return image

    def getMainColor(self) -> Color:
        if self.isBroken():
            return None
        image: PIL.Image = self._data.copy()
        BLURRED_IMAGE_SIZE: int = 100

        image.thumbnail((BLURRED_IMAGE_SIZE, BLURRED_IMAGE_SIZE))

        paletted = image.convert("P", palette=PIL.Image.ADAPTIVE, colors=16)

        palette = paletted.getpalette()
        color_counts = sorted(paletted.getcolors(), reverse=True)
        palette_index = color_counts[0][1]
        dominant_color = palette[palette_index * 3 : palette_index * 3 + 3]
        return Color(
            red=dominant_color[0], green=dominant_color[1], blue=dominant_color[2]
        )

    def getContrastLevel(self) -> float:
        mainColor: Color = self.getMainColor()
        if mainColor is None:
            return None
        imageBrightness = (
            85 * mainColor.red + 280 * mainColor.green + 26 * mainColor.blue
        ) / 100000

        return imageBrightness

    @staticmethod
    def saveFile(data: bytes, file_path: str) -> bool:
        file = open(file_path, "wb")
        file.write(bytearray(data))
        file.close()
        return True
