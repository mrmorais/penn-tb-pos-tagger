import functools
import pickle
import time
import re
import os

from .treebank import Treebank
from .tokenizer import Tokenizer
from .evaluator import eval

class PTBReader:
    """Reads the Penn Treebank structure and tokenize it"""

    def __init__(self, path):
        self.path = path

    def create_dumps_dir(self):
        dirs = ['data', 'dumps']
        
        for idx, val in enumerate(dirs):
            path = '/'.join(dirs[:(idx + 1)])
            try:
                os.stat(path)
            except:
                os.mkdir(path)            

    def read(self):
        tokenizer = Tokenizer()

        self.create_dumps_dir()

        print('reading file...')
        tk_start = time.time()
        with open(self.path, "r") as file:
            f_read_ch = functools.partial(file.read, 1)

            for ch in iter(f_read_ch, ''):
                tokenizer.digest_char(ch)
        tk_end = time.time()

        print('done; tokenizer took ' + str(tk_end - tk_start) + ' seconds.\n')
        print('creating dump for tokens...')
        
        tk_dump_name = 'data/dumps/token_dump_' + str(int(tk_end))
        with open(tk_dump_name, "wb") as file:
            pickle.dump(tokenizer.get_tokens(), file)
        
        print('done. Evaluating structure...\n')

        el_start = time.time()
        ptbank = eval(tokenizer.get_tokens())
        el_end = time.time()

        print('done. eval took ' + str(el_end - el_start) + ' seconds.')
        print(ptbank.instances)
        print('read ' + str(len(ptbank.instances)) + ' instaces.')
        print('creating dump for ptbank...')

        pt_dump_nm = 'data/dumps/ptbank_inst_dump_' + str(int(tk_end))
        with open(pt_dump_nm, "wb") as file:
            pickle.dump(ptbank.instances, file)

        print('done.\n\nGenerated ptbank saved at: ' + pt_dump_nm)

        return ptbank


