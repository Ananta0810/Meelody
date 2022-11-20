

class Bytes:
    @staticmethod
    def get_bytes_from_file(path_name: str) -> bytes:
        with open(path_name, "rb") as file:
            return bytearray(file.read())