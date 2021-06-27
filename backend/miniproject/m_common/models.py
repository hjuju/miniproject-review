from django.db import models

from abc import *
from dataclasses import dataclass
import numpy as np
from PIL import Image
import nltk
from konlpy.tag import Okt; t = Okt()
from konlpy.corpus import kobill


@dataclass
class FileDTO(object):

    context: str
    textfile: str
    imgfile: str

    @property
    def context(self) -> str: return self._context

    @context.setter
    def context(self, context): self._context = context

    @property
    def textfile(self) -> str: return self._textfile

    @textfile.setter
    def textfile(self, textfile): self._textfile = textfile

    @property
    def imgfile(self) -> str: return self._imgfile

    @imgfile.setter
    def imgfile(self, imgfile): self._imgfile = imgfile


class ReaderBase(metaclass=ABCMeta):

    @abstractmethod
    def textread(self):
        pass

    def imgread(self):
        pass

    @abstractmethod
    def text(self):
        pass

    @abstractmethod
    def img(self):
        pass

    @abstractmethod
    def doc_text(self):
        pass


class Reader(ReaderBase):

    def textread(self, file) -> str:
        return file.context + file.textfile

    def imgread(self, file) -> str:
        return file.context + file.imgfile

    def text(self, file) -> object:
        return open(f'{self.textread(file)}').read()

    def img(self, file) -> object:
        return np.array(Image.open(f'{self.imgread(file)}'))

    def doc_text(self, text) -> object:
        return kobill.open(self.textread(text)).read()




