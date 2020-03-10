import re
from enum import Enum
import functools
import pickle
from .treebank import Treebank

class TokenType(Enum):
    W_SPC = 'white-space'
    ENT_NAME = 'entity-name'
    ENT_VALUE = 'entity-value'
    OPEN_PR = 'open-paren'
    CLOSE_PR = 'close-paren'
    INIT_EXP = 'init-expr'
    EXP_OR_VAL = 'exp-or-val'
    END_OR_INIT_EXP = 'end-or-init-exp'

class Tokenizer:
    # An Expression is:
    #   OPEN_PR ENT_NAME W_SPC [EXPRESSION|ENT_VALUE] CLOSE_PR

    buffer = ''
    seek = TokenType.OPEN_PR
    tokens = []

    def get_tokens(self):
        return self.tokens

    def digest_char(self, chr):
        if (chr == '\n'): return

        if self.seek == TokenType.OPEN_PR:
            if chr != '(': return
            self.tokens.append((TokenType.OPEN_PR, '('))
            self.seek = TokenType.INIT_EXP
        elif self.seek == TokenType.CLOSE_PR:
            if chr != ')': return
            self.tokens.append((TokenType.CLOSE_PR, ')'))
        elif self.seek == TokenType.INIT_EXP:
            if chr == ' ': return
            if chr == '(':
                self.tokens.append((TokenType.OPEN_PR, '('))
                self.seek = TokenType.INIT_EXP
            else:
                self.buffer += chr
                self.seek = TokenType.ENT_NAME
        elif self.seek == TokenType.ENT_NAME:
            if chr == ' ':
                self.tokens.append((TokenType.ENT_NAME, self.buffer))
                self.tokens.append((TokenType.W_SPC, ' '))
                self.buffer = ''
                self.seek = TokenType.EXP_OR_VAL
            else:
                self.buffer += chr
        elif self.seek == TokenType.EXP_OR_VAL:
            if chr == ' ': return
            if chr == '(':
                self.tokens.append((TokenType.OPEN_PR, '('))
                self.seek = TokenType.ENT_NAME
            else:
                self.buffer += chr
                self.seek = TokenType.ENT_VALUE
        elif self.seek == TokenType.ENT_VALUE:
            if chr == ')':
                self.tokens.append((TokenType.ENT_VALUE, self.buffer))
                self.tokens.append((TokenType.CLOSE_PR, ')'))
                self.buffer = ''
                self.seek = TokenType.END_OR_INIT_EXP
            else:
                self.buffer += chr
        elif self.seek == TokenType.END_OR_INIT_EXP:
            if chr == ' ': return
            if chr == '(':
                self.tokens.append((TokenType.OPEN_PR, '('))
                self.seek = TokenType.INIT_EXP
            elif chr == ')':
                self.tokens.append((TokenType.CLOSE_PR, ')'))



class PTBReader:
    """Reads the Penn Treebank structure and tokenize it"""

    def __init__(self, path):
        self.path = path

    # def linear_tags(self):
    #     with open(self.path, "r") as file:
    #         return re.findall("(\(+\w+ +\w+\))", file.read(100))

    def read(self):
        treeb = Treebank()
        tokenizer = Tokenizer()

        with open(self.path, "r") as file:
            f_read_ch = functools.partial(file.read, 1)

            for ch in iter(f_read_ch, ''):
                tokenizer.digest_char(ch)
        
        with open('tokenizer_dump', "wb") as file:
            pickle.dump(tokenizer.get_tokens(), file)
            print('done')

