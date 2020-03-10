from enum import Enum

class POSEntityType(Enum):
    CC      = 'coord-conj'
    CD      = 'card-num'
    DT      = 'determ'
    EX      = 'exist-there'
    FW      = 'foreign-word'
    IN      = 'prepo/subord-conj'
    JJ      = 'adjective'
    JJR     = 'comp-adj'
    JJS     = 'super-adj'
    LS      = 'list-item-mark'
    MD      = 'modal'
    NN      = 'sg/mass-noun'
    NNS     = 'noun-plr'
    NNP     = 'prop-noun-sg'
    NNPS    = 'prop-noun-plu'
    PDT     = 'predet'
    POS     = 'poss-end'
    PRP     = 'pers-pronoun'
    PRPD    = 'possess'         # adapted PRP$
    RB      = 'adverb'
    RBR     = 'comp-adv'
    RBS     = 'super-adv'
    RP      = 'particle'
    SYM     = 'symbol'
    TO      = 'to'
    UH      = 'interject'
    VB      = 'verb-base-form'
    VBD     = 'verb-past-tense'
    VBG     = 'verb-gerund'
    VBN     = 'verb-past-part'
    VBP     = 'verb-non-3sg-pres'
    VBZ     = 'verb-3sg-pres'
    WDT     = 'wh-determ'
    WP      = 'wh-pronoun'
    WPD     = 'wh-possess'      # adapted WP$
    WRB     = 'wh-adv'
    DS      = 'dollar-sign'     # adapted $
    PS      = 'pound-sign'      # adapted #
    LQ      = 'left-quote'      # adapted "
    RQ      = 'right-quote'     # adapted "
    LPR     = 'left-paren'      # adapted (
    RPR     = 'right-paren'     # adapted )
    COM     = 'comma'           # adapted ,
    SEP     = 'sent-end-punc'   # adapted .
    SMP     = 'sent-mid-punc'   # adapted :
    S       = 'sentence'

class POSEntity:
    class_name = None
    value = None
    children = []

    def __init__():
        return

    def append_child(self, entity):
        return

    

class Treebank:
    structure = []

    def __init__(self):
        return
    
    def add_entity(self, entity_type):
        return 

    # (NP (DT an) (NNP Oct.) (CD 19) (NN review) )

    # @staticmethod
    # def parse_string(value):
    #     # (IN In)
