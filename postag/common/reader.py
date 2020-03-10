import functools
import pickle
import time
import re

from .treebank import Treebank
from .tokenizer import Tokenizer

class PTBReader:
    """Reads the Penn Treebank structure and tokenize it"""

    def __init__(self, path):
        self.path = path

    def read(self):
        tokenizer = Tokenizer()

        start = time.time()
        with open(self.path, "r") as file:
            f_read_ch = functools.partial(file.read, 1)

            for ch in iter(f_read_ch, ''):
                tokenizer.digest_char(ch)
        end = time.time()
        
        dump_name = 'tokens_dump_' + str(int(end))
        with open(dump_name, "wb") as file:
            pickle.dump(tokenizer.get_tokens(), file)
            print('done in', (end-start))
            print(tokenizer.get_tokens()[:15])

