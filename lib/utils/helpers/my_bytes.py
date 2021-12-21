from io import BytesIO


class MyBytes:
    @staticmethod
    def getBytesFromFile(file: str) -> bytes:
        with open(file, "rb") as image:
            return bytearray(image.read())

    # @staticmethod
    # def get_bytes_from_PIL_image(image) -> bytes:
    #     byte_array = BytesIO()
    #     image.save(byte_array, format="JPEG")
    #     return byte_array.getvalue()
