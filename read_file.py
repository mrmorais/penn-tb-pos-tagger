from postag.common.reader import PTBReader

tags = PTBReader(path='./data/dev').read()
print(tags)