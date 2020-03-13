from enum import Enum
import pickle

from postag.utils.reader import PTBReader

class POSEntity:
    def __init__(self):
        self.class_name = None
        self.value = None
        self.children = []

    def new_child(self):
        """
        Creates a new child in the chain and return it
        """
        child = POSEntity()
        self.children.append(child)
        return child

    def __str__(self):
        return self.string_format()

    def string_format(self, depth=0):
        """
        Human-readable structure representation
        """

        space_str = "\n" + depth*"  "
        if self.value == None:
            return "("+ self.class_name +" "+ space_str.join(map(lambda x: x.string_format(depth+1), self.children)) +")"
        else:
            return "("+ self.class_name +" "+ self.value +")"

class POSInstance:

    def __init__(self):
        self.children = []

    def new_child(self):
        """
        Creates a new child in the chain and return it
        """

        child = POSEntity()
        self.children.append(child)
        return child

    def __str__(self):
        return self.string_format()

    def string_format(self, depth=0):
        """
        Human-readable structure representation
        """

        space_str = "\n" + depth*"  "
        return "("+ space_str.join(map(lambda x: x.string_format(depth+1),self.children)) +")"
    

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
        """
        Appends a new instance into the intances set
        """
        inst = POSInstance()
        self.instances.append(inst)
        return inst

    
    def __del__(self):
        del self.instances
        self.instances = []