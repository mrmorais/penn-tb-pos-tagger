from .tokenizer import TokenType
from .treebank import Treebank

def eval(tokens):
    level_stack = []
    tbank = Treebank()

    for token in tokens:
        if len(level_stack) == 0 and token[0] == TokenType.OPEN_PR:
            level_stack.append(tbank.new_instance())
        else:
            if token[0] == TokenType.OPEN_PR:
                level_stack.append(level_stack[-1].new_child())
            if token[0] == TokenType.ENT_NAME:
                level_stack[-1].class_name = token[1]
            if token[0] == TokenType.ENT_VALUE:
                level_stack[-1].value = token[1]
            if token[0] == TokenType.CLOSE_PR:
                level_stack.pop()
    return tbank