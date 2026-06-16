import sys
from dataclasses import dataclass
import shutil


@dataclass
class Archive:
    filename: str
    path_save: str

    def compress_files(self, expansion: str):
        shutil.make_archive(self.path_save, expansion, self.filename)

