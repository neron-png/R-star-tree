from RTreeNode import *
from Record import *
from storageHandler import *
from config import *

class RStarTree():
    from ._insert import insert
    from ._search import search_record
    from ._delete import delete_entry
    def __init__(self):
        self.root = RTreeNode(block_id=0)
        self.currentBlock = self.root #This is a pointer!
        print(self.currentBlock)
        print(self.currentBlock.toBytes())
