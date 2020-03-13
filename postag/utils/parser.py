from ..core import treebank

def parser(chunks, open_mark='(', close_mark=')'):
    """
    Parses a tbank structure by tokenizing and evaluating interable chunks of an input
    """

    buffer = ''
    level_stack = []
    seek = 'begin_exp'
    tbank = treebank.Treebank()
    
    for chunk in chunks:
        for ch in chunk:
            if ch == '\n': continue
            if seek == 'end_or_new_exp':
                if ch == ' ': continue
                if ch == open_mark:
                    if len(level_stack) == 0:
                        level_stack.append(tbank.new_instance())
                    else:
                        level_stack.append(level_stack[-1].new_child())
                    seek = 'begin_exp'
                elif ch == close_mark:
                    if level_stack[0]:
                        level_stack.pop()
            elif seek == 'build_name':
                # After building a entity name (first appearence of SPACE)
                # the tokenizer must wait for a new expression or a value
                if ch == ' ':
                    if level_stack[0]:
                        level_stack[-1].class_name = buffer
                    buffer = ''
                    seek = 'exp_or_val'
                else:
                    buffer += ch
            elif seek == 'build_val':
                # After a closen paren is expected to keep closing a chain
                # or beginning a new expression 
                if ch == close_mark:
                    level_stack[-1].value = buffer
                    level_stack.pop()
                    buffer = ''
                    seek = 'end_or_new_exp'
                else:
                    buffer += ch
            elif seek == 'exp_or_val':
                if ch == ' ': continue
                if ch == open_mark:
                    if len(level_stack) == 0:
                        level_stack.append(tbank.new_instance())
                    else:
                        level_stack.append(level_stack[-1].new_child())
                    seek = 'begin_exp'
                else:
                    buffer += ch
                    seek = 'build_val'
            elif seek == 'begin_exp':
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
                    seek = 'build_name'

    return tbank