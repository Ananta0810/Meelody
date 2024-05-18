import importlib
import os
import re
import sys
import traceback
import types
from importlib import util
from io import BytesIO

from app.utils.base import Strings
from app.utils.reflections import SingletonMeta


class AudioEditor(metaclass=SingletonMeta):

    def __init__(self) -> None:
        super().__init__()
        try:
            for moduleName in "pydub.utils", "pydub.audio_segment":
                spec = util.find_spec(moduleName, None)
                source = spec.loader.get_source(moduleName)
                if source is None:
                    continue
                print(source)
                snippet = "__import__('subprocess').STARTUPINFO(dwFlags=__import__('subprocess').STARTF_USESHOWWINDOW)"
                source, n = re.subn(r"(Popen)\((.+?)\)", rf"\1(\2, startupinfo={snippet})", source, flags=re.DOTALL)
                module = util.module_from_spec(spec)
                exec(compile(source, module.__spec__.origin, "exec"), module.__dict__)
                sys.modules[moduleName] = module
            module = importlib.reload(sys.modules["pydub"])
            for k, v in module.__dict__.items():
                if isinstance(v, types.ModuleType):
                    setattr(module, k, importlib.import_module(v.__name__))
        except:
            traceback.print_exc()

        from pydub import AudioSegment
        basedir = os.path.dirname(sys.argv[0])
        path = Strings.joinPath(basedir, "ffmpeg/ffmpeg.exe")
        AudioSegment.converter = path

    @staticmethod
    def convertToMp3File(file: str, outFile, bitRate=128) -> None:
        from pydub import AudioSegment
        sound = AudioSegment.from_file(file)
        sound.export(outFile, format="mp3", bitrate=f"{bitRate}k")

    @staticmethod
    def toMp3FileFromBytes(data: BytesIO, outFile, bitRate=128) -> None:
        data.seek(0)

        from pydub import AudioSegment
        sound = AudioSegment.from_file(file=data)
        sound.export(outFile, format="mp3", bitrate=f"{bitRate}k")
