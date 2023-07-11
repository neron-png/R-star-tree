import json
import config
from record import Record 


class Block:

    def __init__(self, id: int):

        self.id = id

        self.slots = []

        self._ = ""
    
        # The '_' attribute is used to give each record (block slot) the same size;
        # so each block contains the same number of slots (filled with records)

        # # If the record is smaller than the fixed slot size, '_' fills with dump '0's
        # self._ = ""
        # while self.__size__() < config.RECORDSIZE:
        #     self._ += "0"

        # # If the record is bigger than the fixed slot size, the name attribute gets cut
        # while self.__size__() > config.RECORDSIZE and len(self.name) > 0:
        #     self.name = self.name[:-1]
        # else:
        #     # It is mandatory for each data element to contain a name, such as the default
        #     if len(self.name) == 0:
        #         self.name = config.DEFAULT_POINT_NAME

        #     # If the name attribute (or any other) exceeds the size limit, abort record
        #     if self.__size__() > config.RECORDSIZE:
        #         raise Exception("Record (node) " + self.id + " exceeds the slot size limit")
    
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
    