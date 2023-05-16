import numpy as np
from RTreeNode import *
from Record import *
from node import *




class RTree():

    def __init__(self):
        self.root = RTreeNode(block_id=0)
        self.currentBlock = self.root #This is a pointer!
        print(self.currentBlock)
        print(self.currentBlock.toBytes())

    def insert(self):
        pass


    """ 
    Delete an index record with given coordinates
    """
    def delete_entry(self, p: Point) -> bool:

        # Get the point's coordinates list
        c = p.coordinates





        return True