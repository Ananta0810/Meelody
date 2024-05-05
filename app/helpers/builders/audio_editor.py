import os
import sys
from io import BytesIO

from pydub import AudioSegment

from app.helpers.base import SingletonMeta, Strings

basedir = os.path.dirname(sys.argv[0])
path = Strings.joinPath(basedir, "ffmpeg.exe")

AudioSegment.converter = path


class AudioEditor(metaclass=SingletonMeta):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def convertToMp3File(file: str, outFile, bitRate=128) -> None:
        sound = AudioSegment.from_file(file)
        sound.export(outFile, format="mp3", bitrate=f"{bitRate}k")

    @staticmethod
    def toMp3FileFromBytes(data: BytesIO, outFile, bitRate=128) -> None:
        data.seek(0)
        sound = AudioSegment.from_file(file=data)
        sound.export(outFile, format="mp3", bitrate=f"{bitRate}k")
