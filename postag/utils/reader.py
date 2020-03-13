import functools
import pickle
import time
import re
import os

from ..core import treebank
# from .tokenizer import Tokenizer
from .parser import parser

class PTBReader:
    """
    Reads the Penn Treebank structure and tokenize it
    """

    def __init__(self, path):
        self.path = path

    def read(self):
        ptbank = None

        with open(self.path, "r") as file:
            f_read_chunk = functools.partial(file.read, 1000)
            ptbank = parser(iter(f_read_chunk, ''))
        return ptbank