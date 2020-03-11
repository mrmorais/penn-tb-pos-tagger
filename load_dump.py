#!/usr/bin/python
from postag.common.treebank import Treebank
import sys

Treebank().load(sys.argv[1])