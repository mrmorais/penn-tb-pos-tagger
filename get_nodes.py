from postag import Treebank
from time import time

tb = Treebank.read_file('data/dev-2')

nodes = tb.get_nodes(group_by_inst=True)
for n in nodes:
    print(n)