from .tokenizer import TokenType
from ..core import treebank

def eval(tokens):
    level_stack = []
    tbank = treebank.Treebank()

    for token in tokens:
        if len(level_stack) == 0 and token[0] == 'open_pr':
            continue
            # level_stack.append(tbank.new_instance())
        else:
            if token[0] == 'open_pr':
                continue
                # level_stack.append(level_stack[-1].new_child())
            if token[0] == 'close_pr':
                continue
                # level_stack.pop()
            if token[0] == 'ent_name':
                continue
                # level_stack[-1].class_name = token[1]
            if token[0] == 'ent_val':
                continue
                # level_stack[-1].value = token[1]
    return tbank