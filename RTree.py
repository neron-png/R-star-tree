from Block import Block

class RTree():

    def __init__(self):
        self.root = Block(block_id=0)
        self.currentBlock = self.root #This is a pointer!
        print(self.currentBlock)
        print(self.currentBlock.toBytes())


    def insert(self):
        pass