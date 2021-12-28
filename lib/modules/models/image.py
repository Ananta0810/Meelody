from io import BytesIO

import PIL.Image


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

    def getMainColor(self) -> list[int]:
        if self.isBroken():
            return None
        image: PIL.Image = self._data.copy()
        BLURRED_IMAGE_SIZE: int = 100

        image.thumbnail((BLURRED_IMAGE_SIZE, BLURRED_IMAGE_SIZE))

        paletted = image.convert("P", palette=PIL.Image.ADAPTIVE, colors=16)

        palette = paletted.getpalette()
        colorCount = sorted(paletted.getcolors(), reverse=True)
        palette_index = colorCount[0][1]
        mainColor = palette[palette_index * 3 : palette_index * 3 + 3]
        return mainColor

    def getContrastLevel(self) -> float:
        red, green, blue = self.getMainColor()
        imageBrightness = (85 * red + 280 * green + 26 * blue) / 100000
        return imageBrightness

    @staticmethod
    def saveFile(data: bytes, file_path: str) -> None:
        file = open(file_path, "wb")
        file.write(bytearray(data))
        file.close()
