from enum import Enum
import pickle

from postag.utils.reader import PTBReader

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

    def __init__(self):
        self.class_name = None
        self.value = None
        self.children = []

    def new_child(self):
        child = POSEntity()
        self.children.append(child)
        return child

    def __str__(self):
        return "(type:%s;len_chldrn:%i;name:%s;value:%s)" % ("POSEntity", len(self.children), self.class_name, self.value)

class POSInstance:

    def __init__(self):
        self.children = []

    def new_child(self):
        child = POSEntity()
        self.children.append(child)
        return child

    def __str__(self):
        return "(type:%s;len_chldrn:%i)" % ("POSInstance", len(self.children))
    

class Treebank:
    def __init__(self):
        self.instances = []

    def load(self, path):
        """
        Loads a previously parsed ptb structure. In order to create a loadable 
        file use the read() and then save() methods.
        """
        ptbank_instances = pickle.load(open(path, "rb"))
        self.instances = ptbank_instances
        del ptbank_instances

    def save(self, path):
        """
        Saves the current structure of instances on a ptb file
        """
        pickle.dump(self.instances, open(path, "wb"))
        return path
    
    @staticmethod
    def read_file(path):
        """
        Reads and parses a raw ptb file.
        """
        return PTBReader(path).read()


    def new_instance(self):
        inst = POSInstance()
        self.instances.append(inst)
        return inst

    
    def __del__(self):
        del self.instances
        self.instances = []