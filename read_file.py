#!/usr/bin/python

from postag.common.reader import PTBReader
import sys

ptb = PTBReader(path=sys.argv[1]).read()