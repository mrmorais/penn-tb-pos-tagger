import functools
import pickle
import time
import re
import os

from ..core import treebank
from .tokenizer import Tokenizer
from .evaluator import eval

class PTBReader:
    """Reads the Penn Treebank structure and tokenize it"""

    def __init__(self, path):
        self.path = path

    def read(self):
        tokenizer = Tokenizer()

        with open(self.path, "r") as file:
            f_read_ch = functools.partial(file.read, 1)

            for ch in iter(f_read_ch, ''):
                tokenizer.digest_char(ch)

        ptbank = eval(tokenizer.get_tokens())
        return ptbank