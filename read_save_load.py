from postag import Treebank
import time

# start = time.time()
ptb = Treebank.read_file('data/traindata')
# end = time.time()

# print(end-start, 'seconds.')
# print(len(ptb.instances))

# ptb.save('data/dumps/my_ptb_struct')

# my_new_ptb = Treebank()
# my_new_ptb.load('data/dumps/my_ptb_struct')

# print(len(my_new_ptb.instances))