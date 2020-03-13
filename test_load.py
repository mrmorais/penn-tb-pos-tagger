import functools
import time
from postag.utils.tokenizer import Tokenizer

fle = open('data/traindata-TOP-sub', "r")
f_c = functools.partial(fle.read, 1)
it = iter(f_c, '')

# tk = Tokenizer()

def tokker(fle_pth):
    fle = open(fle_pth, "r")
    f_c = functools.partial(fle.read, 1)

    buffer = ''
    seek = 'begin_exp'

    for ch in iter(f_c, ''):
        if ch == '\n': continue
        if seek == 'begin_exp':
            # At the beginning of an expression it seeks for a '(',
            # eventually can appear double '(' at begin, so it's only
            # safe to seek an entity name when somethin diferent than
            # '(' comes.
            if ch == ' ': continue
            if ch == '(':
                # self.tokens.append((TokenType.OPEN_PR, '('))
                yield ('open_pr', '(')
            else:
                buffer += ch
                seek = 'build_name'
        elif seek == 'build_name':
            # After building a entity name (first appearence of SPACE)
            # the tokenizer must wait for a new expression or a value
            if ch == ' ':
                # self.tokens.append((TokenType.ENT_NAME, self.buffer))
                yield ('ent_name', buffer)
                buffer = ''
                seek = 'exp_or_val'
            else:
                buffer += ch
        elif seek == 'exp_or_val':
            if ch == ' ': continue
            if ch == '(':
                # self.tokens.append((TokenType.OPEN_PR, '('))
                seek = 'begin_exp'
                yield ('open_pr', '(')
            else:
                buffer += ch
                seek = 'build_val'
        elif seek == 'build_val':
            # After a closen paren is expected to keep closing a chain
            # or beginning a new expression 
            if ch == ')':
                # self.tokens.append((TokenType.ENT_VALUE, self.buffer))
                # self.tokens.append((TokenType.CLOSE_PR, ')'))
                yield ('ent_val', buffer)
                buffer = ''
                seek = 'end_or_new_exp'
            else:
                buffer += ch
        elif seek == 'end_or_new_exp':
            if ch == ' ': continue
            if ch == '(':
                # self.tokens.append((TokenType.OPEN_PR, '('))
                yield ('open_pr', '(')
                seek = 'begin_exp'
            elif ch == ')':
                # self.tokens.append((TokenType.CLOSE_PR, ')'))
                yield ('close_pr', ')')

g = tokker('data/traindata')
ct = 0

start = time.time()
for tk in g: ct+= 1
# list(g)
print(ct)
end = time.time()

print(end-start)

# n = map(all_to_a, it)
# b = list(n)
# print(b)
# print(len(tk.tokens))