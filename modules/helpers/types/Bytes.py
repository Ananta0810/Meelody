from typing import Union


class Bytes:
    @staticmethod
    def get_bytes_from_file(path_name: str) -> bytes:
        with open(path_name, "rb") as file:
            return bytearray(file.read())

    @staticmethod
    def decode(value: Union[bytes, None]) -> Union[str, None]:
        return None if value is None else value.decode('iso-8859-1')

    @staticmethod
    def encode(value: Union[str, None]) -> Union[bytes, None]:
        return None if value is None else value.encode('iso-8859-1')
