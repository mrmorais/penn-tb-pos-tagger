from postag.common.reader import PTBReader

example = """(S 
    (PP-LOC (IN In) 
      (NP 
        (NP (DT an) (NNP Oct.) (CD 19) (NN review) )
        (PP (IN of) 
          (NP (`` ``) 
            (NP-TTL (DT The) (NN Misanthrope) )
            ('' '') 
            (PP-LOC (IN at) 
              (NP 
                (NP (NNP Chicago) (POS 's) )
                (NNP Goodman) (NNP Theatre) ))))"""

tags = PTBReader(path='./data/traindata').read()
print(tags)