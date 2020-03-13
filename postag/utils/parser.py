from enum import Enum
from ..core import treebank

class SeekMode(Enum):
    BEGIN_EXP = 'begin-exp'
    BUILD_NAME = 'build-name'
    EXP_OR_VAL = 'exp-or-val'
    BUILD_VAL = 'build-val'
    END_OR_NEW_EXP = 'end-or-new'

def parser(chunks, open_mark='(', close_mark=')'):
    """
    Parses a tbank structure by tokenizing and evaluating interable chunks of an input
    """

    buffer = ''
    level_stack = []
    seek = SeekMode.BEGIN_EXP
    tbank = treebank.Treebank()
    
    for chunk in chunks:
        for ch in chunk:
            if ch == '\n': continue
            if seek == SeekMode.END_OR_NEW_EXP:
                if ch == ' ': continue
                if ch == open_mark:
                    if len(level_stack) == 0:
                        level_stack.append(tbank.new_instance())
                    else:
                        level_stack.append(level_stack[-1].new_child())
                    seek = SeekMode.BEGIN_EXP
                elif ch == close_mark:
                    if level_stack[0]:
                        level_stack.pop()
            elif seek == SeekMode.BUILD_NAME:
                # After building a entity name (first appearence of SPACE)
                # the tokenizer must wait for a new expression or a value
                if ch == ' ':
                    if level_stack[0]:
                        level_stack[-1].class_name = buffer
                    buffer = ''
                    seek = SeekMode.EXP_OR_VAL
                else:
                    buffer += ch
            elif seek == SeekMode.BUILD_VAL:
                # After a closen paren is expected to keep closing a chain
                # or beginning a new expression 
                if ch == close_mark:
                    level_stack[-1].value = buffer
                    level_stack.pop()
                    buffer = ''
                    seek = SeekMode.END_OR_NEW_EXP
                else:
                    buffer += ch
            elif seek == SeekMode.EXP_OR_VAL:
                if ch == ' ': continue
                if ch == open_mark:
                    if len(level_stack) == 0:
                        level_stack.append(tbank.new_instance())
                    else:
                        level_stack.append(level_stack[-1].new_child())
                    seek = SeekMode.BEGIN_EXP
                else:
                    buffer += ch
                    seek = SeekMode.BUILD_VAL
            elif seek == SeekMode.BEGIN_EXP:
                # At the beginning of an expression it seeks for a '(',
                # eventually can appear double '(' at begin, so it's only
                # safe to seek an entity name when somethin diferent than
                # '(' comes.
                if ch == ' ': continue
                if ch == open_mark:
                    if len(level_stack) == 0:
                        level_stack.append(tbank.new_instance())
                    else:
                        level_stack.append(level_stack[-1].new_child())
                else:
                    buffer += ch
                    seek = SeekMode.BUILD_NAME

    return tbank