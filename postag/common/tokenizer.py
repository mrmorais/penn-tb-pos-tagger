from enum import Enum

class TokenType(Enum):
    ENT_NAME = 'entity-name'
    ENT_VALUE = 'entity-value'
    OPEN_PR = 'open-paren'
    CLOSE_PR = 'close-paren'

class SeekMode(Enum):
    BEGIN_EXP = 'begin-exp'
    BUILD_NAME = 'build-name'
    EXP_OR_VAL = 'exp-or-val'
    BUILD_VAL = 'build-val'
    END_OR_NEW_EXP = 'end-or-new'

class Tokenizer:
    # An Expression is:
    #   OPEN_PR ENT_NAME [EXPRESSION|ENT_VALUE] CLOSE_PR

    buffer = ''
    seek = SeekMode.BEGIN_EXP
    tokens = []

    def get_tokens(self):
        return self.tokens

    def digest_char(self, chr):
        if (chr == '\n'): return

        if self.seek == SeekMode.BEGIN_EXP:
            # At the beginning of an expression it seeks for a '(',
            # eventually can appear double '(' at begin, so it's only
            # safe to seek an entity name when somethin diferent than
            # '(' comes.
            if chr == ' ': return
            if chr == '(':
                self.tokens.append((TokenType.OPEN_PR, '('))
            else:
                self.buffer += chr
                self.seek = SeekMode.BUILD_NAME
        elif self.seek == SeekMode.BUILD_NAME:
            # After building a entity name (first appearence of SPACE)
            # the tokenizer must wait for a new expression or a value
            if chr == ' ':
                self.tokens.append((TokenType.ENT_NAME, self.buffer))
                self.buffer = ''
                self.seek = SeekMode.EXP_OR_VAL
            else:
                self.buffer += chr
        elif self.seek == SeekMode.EXP_OR_VAL:
            if chr == ' ': return
            if chr == '(':
                self.tokens.append((TokenType.OPEN_PR, '('))
                self.seek = SeekMode.BEGIN_EXP
            else:
                self.buffer += chr
                self.seek = SeekMode.BUILD_VAL
        elif self.seek == SeekMode.BUILD_VAL:
            # After a closen paren is expected to keep closing a chain
            # or beginning a new expression 
            if chr == ')':
                self.tokens.append((TokenType.ENT_VALUE, self.buffer))
                self.tokens.append((TokenType.CLOSE_PR, ')'))
                self.buffer = ''
                self.seek = SeekMode.END_OR_NEW_EXP
            else:
                self.buffer += chr
        elif self.seek == SeekMode.END_OR_NEW_EXP:
            if chr == ' ': return
            if chr == '(':
                self.tokens.append((TokenType.OPEN_PR, '('))
                self.seek = SeekMode.BEGIN_EXP
            elif chr == ')':
                self.tokens.append((TokenType.CLOSE_PR, ')'))