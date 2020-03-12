from enum import Enum
from ..core import treebank

class TokenType(Enum):
    ENT_NAME = 'entity-name'
    ENT_VALUE = 'entity-value'
    OPEN_PR = 'open-mark'
    CLOSE_PR = 'close-mark'

class SeekMode(Enum):
    BEGIN_EXP = 'begin-exp'
    BUILD_NAME = 'build-name'
    EXP_OR_VAL = 'exp-or-val'
    BUILD_VAL = 'build-val'
    END_OR_NEW_EXP = 'end-or-new'

def tokenizer(chunks, open_mark='(', close_mark=')'):
    buffer = ''
    level_stack = []
    seek = 'begin_exp'
    tbank = treebank.Treebank()
    
    for chunk in chunks:
        # print(chunk)
        for ch in chunk:
            if ch == '\n': continue
            if seek == 'end_or_new_exp':
                if ch == ' ': continue
                if ch == '(':
                    # self.tokens.append((TokenType.OPEN_PR, '('))
                    # yield ('open_pr', '(')
                    if len(level_stack) == 0:
                        level_stack.append(tbank.new_instance())
                    else:
                        level_stack.append(level_stack[-1].new_child())
                    seek = 'begin_exp'
                elif ch == ')':
                    # self.tokens.append((TokenType.CLOSE_PR, ')'))
                    # yield ('close_pr', ')')
                    if level_stack[0]:
                        level_stack.pop()
            elif seek == 'build_name':
                # After building a entity name (first appearence of SPACE)
                # the tokenizer must wait for a new expression or a value
                if ch == ' ':
                    # self.tokens.append((TokenType.ENT_NAME, self.buffer))
                    # yield ('ent_name', buffer)
                    if level_stack[0]:
                        level_stack[-1].class_name = buffer
                    buffer = ''
                    seek = 'exp_or_val'
                else:
                    buffer += ch
            elif seek == 'build_val':
                # After a closen paren is expected to keep closing a chain
                # or beginning a new expression 
                if ch == ')':
                    # self.tokens.append((TokenType.ENT_VALUE, self.buffer))
                    # self.tokens.append((TokenType.CLOSE_PR, ')'))
                    # yield ('ent_val', buffer)
                    level_stack[-1].value = buffer
                    # yield ('close_pr', ')')
                    # level_stack.pop()
                    buffer = ''
                    seek = 'end_or_new_exp'
                else:
                    buffer += ch
            elif seek == 'exp_or_val':
                if ch == ' ': continue
                if ch == '(':
                    # self.tokens.append((TokenType.OPEN_PR, '('))
                    if len(level_stack) == 0:
                        level_stack.append(tbank.new_instance())
                    seek = 'begin_exp'
                    # yield ('open_pr', '(')
                else:
                    buffer += ch
                    seek = 'build_val'
            elif seek == 'begin_exp':
                # At the beginning of an expression it seeks for a '(',
                # eventually can appear double '(' at begin, so it's only
                # safe to seek an entity name when somethin diferent than
                # '(' comes.
                if ch == ' ': continue
                if ch == '(':
                    # self.tokens.append((TokenType.OPEN_PR, '('))
                    # yield ('open_pr', '(')
                    if len(level_stack) == 0:
                        level_stack.append(tbank.new_instance())
                    else:
                        level_stack.append(level_stack[-1].new_child())
                else:
                    buffer += ch
                    seek = 'build_name'

    return tbank

    # for chunk in chunks:
    #     # print(chunk)
    #     for ch in chunk:
    #         if ch == '\n': continue
    #         if seek == SeekMode.BEGIN_EXP:
    #             # At the beginning of an expression it seeks for a '(',
    #             # eventually can appear double '(' at begin, so it's only
    #             # safe to seek an entity name when somethin diferent than
    #             # '(' comes.
    #             if ch == ' ': continue
    #             if ch == open_mark:
    #                 yield (TokenType.OPEN_PR, open_mark)
    #             else:
    #                 buffer += ch
    #                 seek = SeekMode.BUILD_NAME
    #         elif seek == SeekMode.BUILD_NAME:
    #             # After building a entity name (first appearence of SPACE)
    #             # the tokenizer must wait for a new expression or a value
    #             if ch == ' ':
    #                 yield (TokenType.ENT_NAME, buffer)
    #                 seek = SeekMode.EXP_OR_VAL
    #                 buffer = ''
    #             else:
    #                 buffer += ch
    #         elif seek == SeekMode.EXP_OR_VAL:
    #             if ch == ' ': continue
    #             if ch == open_mark:
    #                 yield (TokenType.OPEN_PR, open_mark)
    #                 seek = SeekMode.BEGIN_EXP
    #             else:
    #                 buffer += ch
    #                 seek = SeekMode.BUILD_VAL
    #         elif seek == SeekMode.BUILD_VAL:
    #             # After a closen paren is expected to keep closing a chain
    #             # or beginning a new expression 
    #             if ch == close_mark:
    #                 yield (TokenType.ENT_VALUE, buffer)
    #                 yield (TokenType.CLOSE_PR, close_mark)
    #                 seek = SeekMode.END_OR_NEW_EXP
    #                 buffer = ''
    #             else:
    #                 buffer += ch
    #         elif seek == SeekMode.END_OR_NEW_EXP:
    #             if ch == ' ': continue
    #             if ch == open_mark:
    #                 yield (TokenType.OPEN_PR, open_mark)
    #                 seek = SeekMode.BEGIN_EXP
    #             elif ch == close_mark:
    #                 yield (TokenType.CLOSE_PR, close_mark)