import json
import config
from Record import Record 


class Block:

    def __init__(self, id: int):

        # Initialize a Block object, containing an id, a list of slots (=records) 
        # and a dump attribute for filling the empty space of the block
        self.id = id
        self.slots = []
        self._ = ""
        
    def append(self, record: Record):
        self.slots.append(record)

    def occupied(self) -> int:
        return len(self.slots)

    def fill_dump(self):
        while self.__size__() < config.BLOCKSIZE:
            self._ += '0'

    def __size__(self):
        return len(self.to_json())        

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=None, separators= (',', ':')).encode('utf-8')
    