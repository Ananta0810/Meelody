import os.path
import sys
from io import BytesIO

import PIL.Image

from color import Color
from shapes.rectangle import Rectangle

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.common_types.my_bytes import MyBytes


class MyByteImage:
    data: PIL.Image

    def __init__(self, data: bytes):
        self.data = PIL.Image.open(BytesIO(data))
        self.data.load()

    def get_size(self) -> tuple:
        if self.is_broken():
            return (0, 0)
        return self.data.size

    def is_broken(self) -> bool:
        try:
            self.data.verify()
            return False
        except:
            return True

    def crop(self, rect: Rectangle) -> PIL.Image:
        image = self.data.copy()
        image = image.crop((rect.left, rect.top, rect.right, rect.bottom))
        return image

    def square(self) -> PIL.Image:
        if self.is_broken():
            return
        image: PIL.Image = self.data.copy()
        width, height = image.size  # Get dimensions

        if width == height:
            return

        # Crop the center of the image
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

    def resize(self, new_width: int, new_height: int) -> PIL.Image:
        if self.is_broken():
            return
        image: PIL.Image = self.data.copy()
        image = self.data.resize((new_width, new_height), PIL.Image.ANTIALIAS)
        return image

    def get_dominant_color(self) -> Color:
        if self.is_broken():
            return None
        image: PIL.Image = self.data.copy()
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

    def get_contrast_level(self) -> float:
        main_color: Color = self.get_dominant_color()
        if main_color is None:
            return None
        image_brightness = (
            85 * main_color.red + 280 * main_color.green + 26 * main_color.blue
        ) / 100000

        return image_brightness

    @staticmethod
    def save_file(data: bytes, file_path: str) -> bool:
        file = open(file_path, "wb")
        file.write(bytearray(data))
        file.close()
        return True
